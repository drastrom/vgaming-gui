#!/usr/bin/env python

from __future__ import print_function

import atexit
import base64
import botocore.session
from copy import deepcopy
import json
import os
import subprocess
import sys
import tempfile
import threading
import time
from traceback import format_exc
import vgaming_xrc, wx
import wx.lib.agw.genericmessagedialog

# Python3 compat fallbacks
try:
    from urllib.parse import unquote
except ImportError:
    from urllib import unquote

try:
    from typing import final
except (ImportError, NameError):
    def final(f):
        """ This is all typing.final really is... It's all about declaring to a
        type checker, not actually doing anything at runtime. """
        return f

try:
    iteritems = dict.iteritems
except AttributeError:
    iteritems = dict.items

_ = wx.GetTranslation

# Utility function
def make_ec2_client(settings):
    return botocore.session.get_session().create_client('ec2', region_name=settings["region"], **{'aws_'+key: value for key,value in iteritems(settings) if 'access_key' in key})


class GenericMessageDialog(wx.lib.agw.genericmessagedialog.GenericMessageDialog):
    def __init__(self, *args, **kwargs):
        super(GenericMessageDialog, self).__init__(*args, **kwargs)

    #WHY doesn't this work without this?!?
    def OnKeyDown(self, evt):
        if evt.GetKeyCode() == wx.WXK_RETURN:
            newevt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.GetDefaultItem().GetId())
            wx.PostEvent(self, newevt)
        else:
            super(GenericMessageDialog, self).OnKeyDown(evt)


class WaitDlg(vgaming_xrc.xrcdlgWait):
    def __init__(self, parent):
        super(WaitDlg, self).__init__(parent)

    def OnInit_dialog(self, evt):
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.timer.Start(50)

    def OnClose(self, evt):
        #wx.MessageBox('Cancelation is not implemented. Please keep waiting', 'Keep waiting', wx.OK | wx.ICON_WARNING)
        pass

    def OnTimer(self, evt):
        self.gauge.Pulse()

    def OnWindow_destroy(self, evt):
        self.timer.Stop()


class BaseThread(threading.Thread):
    def __init__(self, **kwargs):
        super(BaseThread, self).__init__(**kwargs)

    @final
    def run(self):
        """ Don't override this anymore, override process instead. """
        try:
            self.pre_process()
            self.process()
            self.on_success()
        except:
            self.on_error()
            raise
        finally:
            self.on_complete()

    def pre_process(self):
        pass

    def on_success(self):
        pass

    def on_error(self):
        pass

    def on_complete(self):
        pass

    def process(self):
        """ @see threading.Thread.run """
        super(BaseThread, self).run()


class SingletonThread(BaseThread):
    _singleton_instance = None
    _lock = None # type: threading.Lock
    # this lock is shared by all SingletonThread instances
    _meta_lock = threading.Lock()

    @classmethod
    def _get_lock(cls):
        if cls._lock is not None:
            return cls._lock
        else:
            with cls._meta_lock:
                if cls._lock is None:
                    cls._lock = threading.Lock()
                return cls._lock

    def __init__(self, **kwargs):
        super(SingletonThread, self).__init__(**kwargs)
        self.daemon = True

    def is_equivalent(self, *args, **kwargs):
        # type: (...) -> bool
        return False

    def raise_non_equivalence(self, *args, **kwargs):
        raise RuntimeError(_("Already-running thread is not equivalent to "
                             "thread we were asked to ensure was started"))

    @classmethod
    def ensure_started(cls, *args, **kwargs):
        with cls._get_lock():
            if (cls._singleton_instance is None or
                    not cls._singleton_instance.is_alive):
                cls._singleton_instance = cls(*args, **kwargs)
                cls._singleton_instance.start()
                print("Started", cls._singleton_instance)
            elif not cls._singleton_instance.is_equivalent(*args, **kwargs):
                cls._singleton_instance.raise_non_equivalence(*args, **kwargs)
            else:
                print("Already running", cls._singleton_instance)

            return cls._singleton_instance

    def on_complete(self):
        cls = type(self)
        with cls._get_lock():
            cls._singleton_instance = None
        super(SingletonThread, self).on_complete()


class ErrorDlgThread(BaseThread):
    def __init__(self, parent, **kwargs):
        super(ErrorDlgThread, self).__init__(**kwargs)
        self.parent = parent

    def on_success(self):
        del self.parent
        super(ErrorDlgThread, self).on_success()

    def on_error(self):
        exc_message = _("Exception in thread %s") % (self.name,)
        exc_string = format_exc()
        wx.CallAfter(self._show_error, exc_message, exc_string)
        super(ErrorDlgThread, self).on_error()

    def _show_error(self, exc_message, exc_string):
        with GenericMessageDialog(self.parent, exc_message, _("An error occurred"), wx.OK|wx.ICON_ERROR) as errdlg:
            errdlg.SetExtendedMessage(exc_string)
            errdlg.ShowModal()
        del self.parent


class WaitDlgThread(ErrorDlgThread):
    def __init__(self, parent, **kwargs):
        super(WaitDlgThread, self).__init__(parent, **kwargs)
        self.dlg = WaitDlg(parent)

    def start(self):
        with self.dlg:
            super(WaitDlgThread, self).start()
            ret = self.dlg.ShowModal()
        self.join()
        return ret

    def on_success(self):
        wx.CallAfter(self.dlg.EndModal, wx.ID_OK)
        super(WaitDlgThread, self).on_success()

    def on_error(self):
        wx.CallAfter(self.dlg.EndModal, wx.ID_ABORT)
        super(WaitDlgThread, self).on_error()


class SingletonWaiterThread(ErrorDlgThread, SingletonThread):
    def __init__(self, parent, settings, instance_id):
        super(SingletonWaiterThread, self).__init__(parent)
        self.settings = settings
        self.instance_id = instance_id

    def is_equivalent(self, parent, settings, instance_id):
        return self.instance_id == instance_id

    def raise_non_equivalence(self, parent, settings, instance_id):
        raise RuntimeError(_("Already-running thread has different "
                             "instance_id %s than we were called with (%s)") %
                           (self.instance_id, instance_id))


class DescribeInstancesThread(WaitDlgThread):
    _no_query_states = set(("shutting-down", "terminated", "stopping", "stopped"))

    def __init__(self, parent):
        super(DescribeInstancesThread, self).__init__(parent)
        # make a consistent copy
        self.settings = deepcopy(wx.GetApp().settings)

    def process(self):
        ec2 = make_ec2_client(self.settings)
        ret = ec2.describe_instances(Filters=[{'Name': 'tag:aws:ec2launchtemplate:id', 'Values': [self.settings["launch_template_id"]]}])
        print(ret)
        instances = sorted((instance for reservation in ret["Reservations"] for instance in reservation["Instances"]), key=lambda instance: instance["LaunchTime"])
        print(instances)
        # sanity check
        for instance in instances[:-1]:
            if instance["State"]["Name"] != "terminated":
                raise RuntimeError("Old instance(s) seem to still exist.  Better sort this out manually!")

        if len(instances) > 0:
            instance = instances[-1]
            public_ip = instance.get("PublicIpAddress", "")
            instance_id = instance["InstanceId"]
            instance_state = instance["State"]["Name"]
            wx.CallAfter(self._update_ui, self.parent, instance_state, instance_id, instance["SpotInstanceRequestId"], public_ip)
            if instance_state not in self._no_query_states:
                if public_ip == "":
                    WaitForPublicIPThread.ensure_started(self.parent, self.settings, instance_id)
                WaitForPasswordThread.ensure_started(self.parent, self.settings, instance_id)

    def _update_ui(self, parent, state, instance_id, spot_instance_request_id, public_ip):
        parent.ctlStatus.SetValue(state)
        parent.ctlInstanceId.SetValue(instance_id)
        parent.ctlSpotId.SetValue(spot_instance_request_id)
        parent.ctlPublicIP.SetValue(public_ip)


class WaitForPasswordThread(SingletonWaiterThread):
    def __init__(self, parent, settings, instance_id):
        super(WaitForPasswordThread, self).__init__(parent, settings, instance_id)

    def process(self):
        ec2 = make_ec2_client(self.settings)
        waiter = ec2.get_waiter("password_data_available")
        waiter.wait(InstanceId=self.instance_id)
        # stupid waiter only gives you the last result on error, not success
        pwdata = ec2.get_password_data(InstanceId=self.instance_id)["PasswordData"]
        pwdata = base64.b64decode(pwdata)

        hide_console_win = {}
        try:
            # when running as a no-console windows app, calling a console app
            # pops up an annoying console window.  Suppress it
            hide_console_win['startupinfo'] = subprocess.STARTUPINFO()
            hide_console_win['startupinfo'].dwFlags |= subprocess.STARTF_USESHOWWINDOW
            hide_console_win['startupinfo'].wShowWindow = subprocess.SW_HIDE
        except (NameError, AttributeError):
            pass

        if self.settings["decryption_type"] == 0:
            x = subprocess.Popen(["openssl", "rsautl", "-decrypt", "-inkey", self.settings["decryption_key_file_uri"]], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ret = x.communicate(pwdata)
            print(ret, x.returncode)
            if x.returncode != 0:
                raise subprocess.CalledProcessError(x.returncode, "openssl", ret[1])
            password = ret[0]
        elif self.settings["decryption_type"] == 1:
            env = os.environ.copy()
            env["OPENSC_DRIVER"] = "openpgp"
            x = subprocess.Popen(["openssl", "rsautl", "-decrypt", "-keyform", "ENGINE", "-engine", "pkcs11", "-inkey", self.settings["decryption_key_file_uri"]], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
            ret = x.communicate(pwdata)
            print(ret, x.returncode)
            if x.returncode != 0:
                raise subprocess.CalledProcessError(x.returncode, "openssl", ret[1])
            password = ret[0]
        elif self.settings["decryption_type"] == 2:
            x = subprocess.Popen(["gpg-connect-agent", 'SCD SETDATA ' + base64.b16encode(pwdata), 'SCD PKDECRYPT ' + self.settings["decryption_key_file_uri"], '/bye'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, **hide_console_win)
            ret = x.communicate()
            print(ret, x.returncode)
            if x.returncode != 0:
                raise subprocess.CalledProcessError(x.returncode, "gpg-connect-agent", ret[1])
            for line in ret[0].split("\n"):
                if line[:2] == "D ":
                    password = unquote(line[2:])
                elif line[:4] == "ERR ":
                    raise RuntimeError(line[4:])
        wx.CallAfter(self.parent.ctlPassword.SetValue, password)


class WaitForPublicIPThread(SingletonWaiterThread):
    def __init__(self, parent, settings, instance_id):
        super(WaitForPublicIPThread, self).__init__(parent, settings, instance_id)

    def process(self):
        ec2 = make_ec2_client(self.settings)
        waiter = ec2.get_waiter("instance_running")
        waiter.wait(InstanceIds=[self.instance_id])
        # stupid waiter only gives you the last result on error, not success
        ret = ec2.describe_instances(InstanceIds=[self.instance_id])
        instance = ret["Reservations"][0]["Instances"][0]
        wx.CallAfter(self._update_ui, self.parent, instance["State"]["Name"], instance["PublicIpAddress"])

    def _update_ui(self, parent, state, public_ip):
        parent.ctlStatus.SetValue(state)
        parent.ctlPublicIP.SetValue(public_ip)


class WaitForTerminationThread(SingletonWaiterThread):
    def __init__(self, parent, settings, instance_id):
        super(WaitForTerminationThread, self).__init__(parent, settings, instance_id)

    def process(self):
        ec2 = make_ec2_client(self.settings)
        waiter = ec2.get_waiter("instance_terminated")
        waiter.wait(InstanceIds=[self.instance_id])
        # stupid waiter only gives you the last result on error, not success
        ret = ec2.describe_instances(InstanceIds=[self.instance_id])
        instance = ret["Reservations"][0]["Instances"][0]
        wx.CallAfter(self.parent.ctlStatus.SetValue, instance["State"]["Name"])


class StartInstanceThread(WaitDlgThread):
    def __init__(self, parent, subnet_id):
        super(StartInstanceThread, self).__init__(parent)
        self.subnet_id = subnet_id
        # make a consistent copy
        self.settings = deepcopy(wx.GetApp().settings)

    def process(self):
        ec2 = make_ec2_client(self.settings)
        ret = ec2.run_instances(MinCount=1, MaxCount=1, LaunchTemplate={"LaunchTemplateId": self.settings["launch_template_id"]}, NetworkInterfaces=[{"DeviceIndex": 0, "SubnetId": self.subnet_id}])
        instance = ret["Instances"][0]
        instance_id = instance["InstanceId"]
        wx.CallAfter(self._update_ui, self.parent, instance["State"]["Name"], instance_id, instance["SpotInstanceRequestId"])
        WaitForPublicIPThread.ensure_started(self.parent, self.settings, instance_id)
        WaitForPasswordThread.ensure_started(self.parent, self.settings, instance_id)

    def _update_ui(self, parent, state, instance_id, spot_instance_request_id):
        parent.ctlStatus.SetValue(state)
        parent.ctlInstanceId.SetValue(instance_id)
        parent.ctlSpotId.SetValue(spot_instance_request_id)


class TerminateInstanceThread(WaitDlgThread):
    def __init__(self, parent, instance_id, spot_instance_request_id):
        super(TerminateInstanceThread, self).__init__(parent)
        self.instance_id = instance_id
        self.spot_instance_request_id = spot_instance_request_id
        # make a consistent copy
        self.settings = deepcopy(wx.GetApp().settings)

    def process(self):
        ec2 = make_ec2_client(self.settings)
        ret = ec2.cancel_spot_instance_requests(SpotInstanceRequestIds=[self.spot_instance_request_id])
        print(ret)
        ret = ec2.terminate_instances(InstanceIds=[self.instance_id])
        print(ret)
        instance = ret["TerminatingInstances"][0]
        wx.CallAfter(self.parent.ctlStatus.SetValue, instance["CurrentState"]["Name"])
        WaitForTerminationThread.ensure_started(self.parent, self.settings, self.instance_id)


class DescribeSubnetsThread(WaitDlgThread):
    def __init__(self, parent):
        super(DescribeSubnetsThread, self).__init__(parent)
        # make a consistent copy
        self.settings = deepcopy(wx.GetApp().settings)

    def process(self):
        ec2 = make_ec2_client(self.settings)
        ret = ec2.describe_subnets(Filters=[{"Name": "state", "Values": ["available"]}])
        self.subnets = {subnet["SubnetId"]: "%s (%s)" % (next((tag["Value"] for tag in subnet["Tags"] if tag["Key"] == "Name"), ""), subnet["AvailabilityZone"]) for subnet in ret["Subnets"]}
        print(self.subnets)


class PickSubnetDlg(vgaming_xrc.xrcdlgSubnetPicker):
    def __init__(self, parent, subnets):
        super(PickSubnetDlg, self).__init__(parent)
        self.subnets = subnets

    def OnInit_dialog(self, evt):
        self.choiceSubnet.Clear()
        for subnet_id, subnet_name in iteritems(self.subnets):
            self.choiceSubnet.Append(subnet_name, subnet_id)

    def OnChoice_choiceSubnet(self, evt):
        self.wxID_OK.Enable(evt.Selection != wx.NOT_FOUND)

    def OnButton_wxID_OK(self, evt):
        selection = self.choiceSubnet.GetSelection()
        if selection != wx.NOT_FOUND:
            self.chosen_subnet = self.choiceSubnet.GetClientData(selection)
            self.EndModal(wx.ID_OK)

    def OnButton_wxID_CANCEL(self, evt):
        self.EndModal(wx.ID_CANCEL)


class SettingsDlg(vgaming_xrc.xrcdlgSettings):
    def __init__(self, parent):
        super(SettingsDlg, self).__init__(parent)

    def OnInit_dialog(self, evt):
        app = wx.GetApp()
        self.ctlRegion.SetValue(app.settings.get("region", ""))
        self.ctlAccessKey.SetValue(app.settings.get("access_key_id", ""))
        self.ctlSecret.SetValue(app.settings.get("secret_access_key", ""))
        self.ctlLaunchTemplate.SetValue(app.settings.get("launch_template_id", ""))
        self.ctlKeyFileURI.SetValue(app.settings.get("decryption_key_file_uri", ""))
        self.radioDecryption.SetSelection(app.settings.get("decryption_type", 0))

    def Save(self):
        app = wx.GetApp()
        settings = deepcopy(app.settings)
        settings["region"] = self.ctlRegion.GetValue()
        settings["access_key_id"] = self.ctlAccessKey.GetValue()
        settings["secret_access_key"] = self.ctlSecret.GetValue()
        settings["launch_template_id"] = self.ctlLaunchTemplate.GetValue()
        settings["decryption_key_file_uri"] = self.ctlKeyFileURI.GetValue()
        settings["decryption_type"] = self.radioDecryption.GetSelection()
        app.SaveSettings(settings)

    def OnButton_wxID_OK(self, evt):
        print("cool")
        self.Save()
        self.EndModal(wx.ID_OK)

    def OnButton_wxID_CANCEL(self, evt):
        print("darn")
        # TODO if not saved, ask if they're sure
        self.EndModal(wx.ID_CANCEL)

    def OnButton_wxID_APPLY(self, evt):
        print("apply")
        self.Save()


class MainFrame(vgaming_xrc.xrcmainframe):
    def __init__(self, parent):
        super(MainFrame, self).__init__(parent)
        if "region" in wx.GetApp().settings:
            wx.CallAfter(self.Refresh)

    def OnButton_btnStart(self, evt):
        thread = DescribeSubnetsThread(self)
        if thread.start() == wx.ID_OK:
            with PickSubnetDlg(self, thread.subnets) as picker:
                if picker.ShowModal() == wx.ID_OK:
                    print(picker.chosen_subnet)
                    thread = StartInstanceThread(self, picker.chosen_subnet)
                    thread.start()

    def OnButton_btnStop(self, evt):
        thread = TerminateInstanceThread(self, self.ctlInstanceId.GetValue(), self.ctlSpotId.GetValue())
        thread.start()

    def OnButton_btnRDP(self, evt):
        with tempfile.NamedTemporaryFile(suffix=".rdp", mode="wb", delete=False) as fp:
            atexit.register(os.unlink, fp.name)
            tmpfile = fp.name
            fp.write("""full address:s:%s\r
username:s:Administrator\r
password:s:%s\r
connect to console:i:1\r
administrative session:i:1\r
""" % (self.ctlPublicIP.GetValue(), self.ctlPassword.GetValue()))
        if sys.platform.startswith('win'):
            os.startfile(tmpfile)
        elif sys.platform in ('cygwin', 'msys'):
            subprocess.Popen(["start", tmpfile])
        elif sys.platform == "darwin":
            subprocess.Popen(["open", tmpfile])
        else:
            subprocess.Popen(["xfreerdp", tmpfile])

    def OnButton_btnDCV(self, evt):
        with tempfile.NamedTemporaryFile(suffix=".dcv", mode="w", delete=False) as fp:
            atexit.register(os.unlink, fp.name)
            tmpfile = fp.name
            fp.write("""[version]
format=1.0

[connect]
host=%s
user=Administrator
password=%s
""" % (self.ctlPublicIP.GetValue(), self.ctlPassword.GetValue()))
        subprocess.Popen(["dcvviewer", tmpfile])

    def OnMenu_wxID_EXIT(self, evt):
        self.Close()

    def OnMenu_wxID_PREFERENCES(self, evt):
        with SettingsDlg(self) as dlg:
            dlg.ShowModal()

    def OnMenu_wxID_REFRESH(self, evt):
        self.Refresh()

    def Refresh(self):
        thread = DescribeInstancesThread(self)
        thread.start()


class VGamingApp(wx.App):
    def __init__(self):
        super(VGamingApp, self).__init__()

    def SaveSettings(self, newsettings):
        with open("config.json", "w") as fp:
            json.dump(newsettings, fp, sort_keys=True, indent=4, separators=(',',': '))
        self.settings = newsettings

    def OnInit(self):
        self.SetAppName('vGaming')
        try:
            with open("config.json", "r") as fp:
                self.settings = json.load(fp)
        except:
            self.settings = {}
        self.mainframe = MainFrame(None)
        self.mainframe.Show()
        return True


app = VGamingApp()
if __name__ == "__main__":
    app.MainLoop()
