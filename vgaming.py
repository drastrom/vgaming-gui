#!/usr/bin/env python

import boto3, botocore
import json
import threading
import time
import vgaming_xrc, wx

try:
    from typing import final
except (ImportError, NameError):
    def final(f):
        """ This is all typing.final really is... It's all about declaring to a
        type checker, not actually doing anything at runtime. """
        return f

# Utility function
def make_boto3_session(settings):
        return boto3.session.Session(region_name=settings["region"], **{'aws_'+key: value for key,value in settings.iteritems() if 'key' in key})

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

    def OnDestroy(self, evt):
        self.timer.Stop()

class WaitDlgThread(threading.Thread):
    def __init__(self, parent, **kwargs):
        super(WaitDlgThread, self).__init__(**kwargs)
        self.dlg = WaitDlg(parent)

    def start(self):
        with self.dlg:
            super(WaitDlgThread, self).start()
            self.dlg.ShowModal()
        self.join()

    @final
    def run(self):
        """ Don't override this anymore, override process instead. """
        try:
            self.process()
            wx.CallAfter(self.dlg.EndModal, wx.ID_OK)
        except:
            wx.CallAfter(self.dlg.EndModal, wx.ID_ABORT)
            raise

    def process(self):
        """ @see threading.Thread.run """
        super(WaitDlgThread, self).run()

class DescribeInstancesThread(WaitDlgThread):
    def __init__(self, parent):
        super(DescribeInstancesThread, self).__init__(parent)
        # make a consistent copy
        self.settings = dict(wx.GetApp().settings)

    def process(self):
        #session = boto3.session.Session(aws_access_key_id=self.settings["access_key_id"], aws_secret_access_key=self.settings["secret_access_key"], region_name=self.settings["region"])
        session = make_boto3_session(self.settings)
        ec2 = session.client('ec2')
        ret = ec2.describe_instances(Filters=[{'Name': 'tag:aws:ec2launchtemplate:id', 'Values': [self.settings["launch_template_id"]]}])
        print (ret)
        #TODO do they tag the spot request or just the instances?
        ret = ec2.describe_spot_instance_requests(Filters=[{'Name': 'tag:aws:ec2launchtemplate:id', 'Values': [self.settings["launch_template_id"]]}])
        print (ret)
        ret = ec2.describe_launch_templates(LaunchTemplateIds=[self.settings["launch_template_id"]])
        print (ret)
        print (ret["LaunchTemplates"][0]["LaunchTemplateName"])

class SettingsDlg(vgaming_xrc.xrcdlgSettings):
    def __init__(self, parent):
        super(SettingsDlg, self).__init__(parent)

    def OnInit_dialog(self, evt):
        app = wx.GetApp()
        self.ctlRegion.SetValue(app.settings.get("region", ""))
        self.ctlAccessKey.SetValue(app.settings.get("access_key_id", ""))
        self.ctlSecret.SetValue(app.settings.get("secret_access_key", ""))
        self.ctlLaunchTemplate.SetValue(app.settings.get("launch_template_id", ""))

    def Save(self):
        app = wx.GetApp()
        settings = dict(app.settings)
        settings["region"] = self.ctlRegion.GetValue()
        settings["access_key_id"] = self.ctlAccessKey.GetValue()
        settings["secret_access_key"] = self.ctlSecret.GetValue()
        settings["launch_template_id"] = self.ctlLaunchTemplate.GetValue()
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
        thread = DescribeInstancesThread(self)
        thread.start()

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
