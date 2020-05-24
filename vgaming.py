#!/usr/bin/env python

import base64
import boto3, botocore
from copy import deepcopy
import itertools
import json
import os
import subprocess
import threading
import time
from traceback import format_exc
import vgaming_xrc, wx
import wx.lib.agw.genericmessagedialog

try:
    from typing import final
except (ImportError, NameError):
    def final(f):
        """ This is all typing.final really is... It's all about declaring to a
        type checker, not actually doing anything at runtime. """
        return f

_ = wx.GetTranslation

# Utility function
def make_boto3_session(settings):
        #return boto3.session.Session(aws_access_key_id=self.settings["access_key_id"], aws_secret_access_key=self.settings["secret_access_key"], region_name=self.settings["region"])
        return boto3.session.Session(region_name=settings["region"], **{'aws_'+key: value for key,value in settings.iteritems() if 'access_key' in key})


class GenericMessageDialog(wx.lib.agw.genericmessagedialog.GenericMessageDialog):
    def __init__(self, *args, **kwargs):
        super(GenericMessageDialog, self).__init__(*args, **kwargs)

    #WHY doesn't this work without this?!?
    def OnKeyDown(self, evt):
        if evt.GetKeyCode() == wx.WXK_RETURN:
            newevt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.DefaultItem.GetId())
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
            self.on_complete()
        except:
            self.on_error()
            raise

    def pre_process(self):
        pass

    def on_complete(self):
        pass

    def on_error(self):
        pass

    def process(self):
        """ @see threading.Thread.run """
        super(BaseThread, self).run()


class ErrorDlgThread(BaseThread):
    def __init__(self, parent, **kwargs):
        super(ErrorDlgThread, self).__init__(**kwargs)
        self.parent = parent

    def on_complete(self):
        del self.parent

    def on_error(self):
        exc_message = _("Exception in thread %s") % (self.name,)
        exc_string = format_exc()
        wx.CallAfter(self._show_error, exc_message, exc_string)

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
            self.dlg.ShowModal()
        self.join()

    def on_complete(self):
        wx.CallAfter(self.dlg.EndModal, wx.ID_OK)
        super(WaitDlgThread, self).on_complete()

    def on_error(self):
        wx.CallAfter(self.dlg.EndModal, wx.ID_ABORT)
        super(WaitDlgThread, self).on_error()


class DescribeInstancesThread(WaitDlgThread):
    def __init__(self, parent):
        super(DescribeInstancesThread, self).__init__(parent)
        # make a consistent copy
        self.settings = deepcopy(wx.GetApp().settings)

    def process(self):
        session = make_boto3_session(self.settings)
        ec2 = session.client('ec2')
        ret = ec2.describe_instances(Filters=[{'Name': 'tag:aws:ec2launchtemplate:id', 'Values': [self.settings["launch_template_id"]]}])
        print (ret)
        instances = sorted((instance for reservation in ret["Reservations"] for instance in reservation["Instances"]), key=lambda instance: instance["LaunchTime"])
        print (instances)
        #TODO do they tag the spot request or just the instances?
        ret = ec2.describe_spot_instance_requests(Filters=[{'Name': 'tag:aws:ec2launchtemplate:id', 'Values': [self.settings["launch_template_id"]]}])
        print (ret)
        ret = ec2.describe_launch_templates(LaunchTemplateIds=[self.settings["launch_template_id"]])
        print (ret)
        print (ret["LaunchTemplates"][0]["LaunchTemplateName"])
        if len(instances) > 0:
            instance = instances[-1]
            public_ip = instance.get("PublicIpAddress", "")
            wx.CallAfter(self._update_ui, parent, instance["State"]["Name"], instance["InstanceId"], instance["SpotInstanceRequestId"], public_ip)
            #if public_ip == "":
            #    WaitForPublicIPThread(self.parent, instance["InstanceId"]).start()
            #WaitForPasswordThread(self.parent, instance["InstanceId"]).start()

    def _update_ui(self, parent, state, instance_id, spot_instance_request_id, public_ip):
        parent.ctlStatus.SetValue(state)
        parent.ctlInstanceId.SetValue(instance_id)
        parent.ctlSpotId.SetValue(spot_instance_request_id)
        parent.ctlPublicIP.SetValue(public_ip)


class WaitForPasswordThread(ErrorDlgThread):
    def __init__(self, parent, instance_id):
        super(WaitForPasswordThread, self).__init__(parent)
        self.instance_id = instance_id
        # make a consistent copy
        self.settings = deepcopy(wx.GetApp().settings)

    def process(self):
        session = make_boto3_session(self.settings)
        ec2 = session.client('ec2')
        waiter = ec2.get_waiter("password_data_available")
        waiter.wait(InstanceId=self.instance_id)
        # stupid waiter only gives you the last result on error, not success
        pwdata = ec2.get_password_data(InstanceId=self.instance_id)["PasswordData"]
        pwdata = base64.b64decode(pwdata)
        if self.settings["decryption_type"] == 0:
            x = subprocess.Popen(["openssl", "rsautl", "-decrypt", "-inkey", self.settings["decryption_key_file_uri"]], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ret = x.communicate(pwdata)
            print ret, x.returncode
            if x.returncode != 0:
                raise subprocess.CalledProcessError(x.returncode, "openssl", ret[1])
            password = ret[0]
        elif self.settings["decryption_type"] == 1:
            env = os.environ.copy()
            env["OPENSC_DRIVER"] = "openpgp"
            x = subprocess.Popen(["openssl", "rsautl", "-decrypt", "-keyform", "ENGINE", "-engine", "pkcs11", "-inkey", self.settings["decryption_key_file_uri"]], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
            ret = x.communicate(pwdata)
            print ret, x.returncode
            if x.returncode != 0:
                raise subprocess.CalledProcessError(x.returncode, "openssl", ret[1])
            password = ret[0]
        elif self.settings["decryption_type"] == 2:
            x = subprocess.Popen(["gpg-connect-agent", 'SCD SETDATA ' + base64.b16encode(pwdata), 'SCD PKDECRYPT ' + self.settings["decryption_key_file_uri"], '/bye'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ret = x.communicate()
            print ret, x.returncode
            if x.returncode != 0:
                raise subprocess.CalledProcessError(x.returncode, "gpg-connect-agent", ret[1])
            for line in ret[0].split("\n"):
                if line[:2] == "D ":
                    password = line[2:]
                elif line[:4] == "ERR ":
                    raise RuntimeError(line[4:])
        wx.CallAfter(self.parent.ctlPassword.SetValue, password)


class WaitForPublicIPThread(ErrorDlgThread):
    def __init__(self, parent, instance_id):
        super(WaitForPublicIPThread, self).__init__(parent)
        self.instance_id = instance_id
        # make a consistent copy
        self.settings = deepcopy(wx.GetApp().settings)

    def process(self):
        session = make_boto3_session(self.settings)
        ec2 = session.client('ec2')
        waiter = ec2.get_waiter("instance_running")
        waiter.wait(InstanceId=self.instance_id)
        # stupid waiter only gives you the last result on error, not success
        ret = ec2.describe_instances(InstanceIds=[self.instance_id])
        instance = ret["Reservations"][0]["Instances"][0]
        wx.CallAfter(self.parent.ctlPublicIP.SetValue, instance["PublicIpAddress"])


class StartInstanceThread(WaitDlgThread):
    def __init__(self, parent, subnet_id):
        super(StartInstanceThread, self).__init__(parent)
        self.subnet_id = subnet_id
        # make a consistent copy
        self.settings = deepcopy(wx.GetApp().settings)

    def process(self):
        session = make_boto3_session(self.settings)
        ec2 = session.client('ec2')
        ret = ec2.run_instances(LaunchTemplate={"LaunchTemplateId": self.settings["launch_template_id"]}, NetworkInterfaces=[{"DeviceIndex": 0, "SubnetId": self.subnet_id}])
        instance = ret["Instances"][0]
        wx.CallAfter(self._update_ui, parent, instance["State"]["Name"], instance["InstanceId"], instance["SpotInstanceRequestId"])
        WaitForPublicIPThread(self.parent, instance["InstanceId"]).start()
        WaitForPasswordThread(self.parent, instance["InstanceId"]).start()

    def _update_ui(self, parent, state, instance_id, spot_instance_request_id):
        parent.ctlStatus.SetValue(state)
        parent.ctlInstanceId.SetValue(instance_id)
        parent.ctlSpotId.SetValue(spot_instance_request_id)


class DescribeSubnetsThread(WaitDlgThread):
    def __init__(self, parent):
        super(DescribeSubnetsThread, self).__init__(parent)
        # make a consistent copy
        self.settings = deepcopy(wx.GetApp().settings)

    def process(self):
        session = make_boto3_session(self.settings)
        ec2 = session.client('ec2')
        ret = ec2.describe_subnets(Filters=[{"Name": "state", "Values": ["available"]}])
        self.subnets = {subnet["SubnetId"]: next((tag["Value"] for tag in subnet["Tags"] if tag["Key"] == "Name"), "") for subnet in ret["Subnets"]}
        print (self.subnets)


class PickSubnetDlg(vgaming_xrc.xrcdlgSubnetPicker):
    def __init__(self, parent, subnets):
        super(PickSubnetDlg, self).__init__(parent)
        self.subnets = subnets

    def OnInit_dialog(self, evt):
        self.choiceSubnet.Clear()
        for subnet_id, subnet_name in self.subnets.iteritems():
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
        self.decryptionTypeRadios = (self.radioOSSLFile, self.radioOSSLPKCS11, self.radioGPGSCD)
        app = wx.GetApp()
        self.ctlRegion.SetValue(app.settings.get("region", ""))
        self.ctlAccessKey.SetValue(app.settings.get("access_key_id", ""))
        self.ctlSecret.SetValue(app.settings.get("secret_access_key", ""))
        self.ctlLaunchTemplate.SetValue(app.settings.get("launch_template_id", ""))
        self.ctlKeyFileURI.SetValue(app.settings.get("decryption_key_file_uri", ""))
        decryption_type = app.settings.get("decryption_type", 0)
        self.decryptionTypeRadios[decryption_type if decryption_type >= 0 and decryption_type < len(self.decryptionTypeRadios) else 0].SetValue(True)

    def Save(self):
        app = wx.GetApp()
        settings = deepcopy(app.settings)
        settings["region"] = self.ctlRegion.GetValue()
        settings["access_key_id"] = self.ctlAccessKey.GetValue()
        settings["secret_access_key"] = self.ctlSecret.GetValue()
        settings["launch_template_id"] = self.ctlLaunchTemplate.GetValue()
        settings["decryption_key_file_uri"] = self.ctlKeyFileURI.GetValue()
        for i, radio in itertools.izip(itertools.count(), self.decryptionTypeRadios):
            if radio.GetValue():
                settings["decryption_type"] = i
                break
        app.SaveSettings(settings)

    def OnButton_wxID_OK(self, evt):
        print "cool"
        self.Save()
        self.EndModal(wx.ID_OK)

    def OnButton_wxID_CANCEL(self, evt):
        print "darn"
        # TODO if not saved, ask if they're sure
        self.EndModal(wx.ID_CANCEL)

    def OnButton_wxID_APPLY(self, evt):
        print "apply"
        self.Save()


class MainFrame(vgaming_xrc.xrcmainframe):
    def __init__(self, parent):
        super(MainFrame, self).__init__(parent)

    def OnButton_btnStart(self, evt):
        thread = DescribeSubnetsThread(self)
        thread.start()
        with PickSubnetDlg(self, thread.subnets) as picker:
            if picker.ShowModal() == wx.ID_OK:
                print picker.chosen_subnet
                #thread = StartInstanceThread(self, picker.chosen_subnet)
                #thread.start()

    def OnButton_btnStop(self, evt):
        # Replace with event handler code
        pass

    def OnButton_btnRDP(self, evt):
        # Replace with event handler code
        pass

    def OnButton_btnDCV(self, evt):
        # Replace with event handler code
        pass

    def OnMenu_wxID_EXIT(self, evt):
        self.Close()

    def OnMenu_itmSettings(self, evt):
        with SettingsDlg(self) as dlg:
            dlg.ShowModal()

    def OnMenu_itmRefresh(self, evt):
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
