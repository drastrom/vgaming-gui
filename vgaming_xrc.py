# This file was automatically generated by pywxrc.
# -*- coding: UTF-8 -*-

import wx
import wx.xrc as xrc

__res = None

def get_resources():
    """ This function provides access to the XML resources in this module."""
    global __res
    if __res == None:
        __init_resources()
    return __res




class xrcmainframe(wx.Frame):
#!XRCED:begin-block:xrcmainframe.PreCreate
    def PreCreate(self, pre):
        """ This function is called during the class's initialization.
        
        Override it for custom setup before the window is created usually to
        set additional window styles using SetWindowStyle() and SetExtraStyle().
        """
        pass
        
#!XRCED:end-block:xrcmainframe.PreCreate

    def __init__(self, parent):
        # Two stage creation (see http://wiki.wxpython.org/index.cgi/TwoStageCreation)
        pre = wx.PreFrame()
        self.PreCreate(pre)
        get_resources().LoadOnFrame(pre, parent, "mainframe")
        self.PostCreate(pre)

        # Define variables for the controls, bind event handlers
        self.ctlStatus = xrc.XRCCTRL(self, "ctlStatus")
        self.ctlInstanceId = xrc.XRCCTRL(self, "ctlInstanceId")
        self.ctlSpotId = xrc.XRCCTRL(self, "ctlSpotId")
        self.ctlPublicIP = xrc.XRCCTRL(self, "ctlPublicIP")
        self.ctlPassword = xrc.XRCCTRL(self, "ctlPassword")

        self.Bind(wx.EVT_MENU, self.OnMenu_wxID_EXIT, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnMenu_itmSettings, id=xrc.XRCID('itmSettings'))
        self.Bind(wx.EVT_MENU, self.OnMenu_itmRefresh, id=xrc.XRCID('itmRefresh'))
        self.Bind(wx.EVT_BUTTON, self.OnButton_btnStart, id=xrc.XRCID('btnStart'))
        self.Bind(wx.EVT_BUTTON, self.OnButton_btnStop, id=xrc.XRCID('btnStop'))
        self.Bind(wx.EVT_BUTTON, self.OnButton_btnRDP, id=xrc.XRCID('btnRDP'))
        self.Bind(wx.EVT_BUTTON, self.OnButton_btnDCV, id=xrc.XRCID('btnDCV'))

#!XRCED:begin-block:xrcmainframe.OnMenu_wxID_EXIT
    def OnMenu_wxID_EXIT(self, evt):
        # Replace with event handler code
        print "OnMenu_wxID_EXIT()"
#!XRCED:end-block:xrcmainframe.OnMenu_wxID_EXIT        

#!XRCED:begin-block:xrcmainframe.OnMenu_itmSettings
    def OnMenu_itmSettings(self, evt):
        # Replace with event handler code
        print "OnMenu_itmSettings()"
#!XRCED:end-block:xrcmainframe.OnMenu_itmSettings        

#!XRCED:begin-block:xrcmainframe.OnMenu_itmRefresh
    def OnMenu_itmRefresh(self, evt):
        # Replace with event handler code
        print "OnMenu_itmRefresh()"
#!XRCED:end-block:xrcmainframe.OnMenu_itmRefresh        

#!XRCED:begin-block:xrcmainframe.OnButton_btnStart
    def OnButton_btnStart(self, evt):
        # Replace with event handler code
        print "OnButton_btnStart()"
#!XRCED:end-block:xrcmainframe.OnButton_btnStart        

#!XRCED:begin-block:xrcmainframe.OnButton_btnStop
    def OnButton_btnStop(self, evt):
        # Replace with event handler code
        print "OnButton_btnStop()"
#!XRCED:end-block:xrcmainframe.OnButton_btnStop        

#!XRCED:begin-block:xrcmainframe.OnButton_btnRDP
    def OnButton_btnRDP(self, evt):
        # Replace with event handler code
        print "OnButton_btnRDP()"
#!XRCED:end-block:xrcmainframe.OnButton_btnRDP        

#!XRCED:begin-block:xrcmainframe.OnButton_btnDCV
    def OnButton_btnDCV(self, evt):
        # Replace with event handler code
        print "OnButton_btnDCV()"
#!XRCED:end-block:xrcmainframe.OnButton_btnDCV        


class xrcdlgSettings(wx.Dialog):
#!XRCED:begin-block:xrcdlgSettings.PreCreate
    def PreCreate(self, pre):
        """ This function is called during the class's initialization.
        
        Override it for custom setup before the window is created usually to
        set additional window styles using SetWindowStyle() and SetExtraStyle().
        """
        pass
        
#!XRCED:end-block:xrcdlgSettings.PreCreate

    def __init__(self, parent):
        # Two stage creation (see http://wiki.wxpython.org/index.cgi/TwoStageCreation)
        pre = wx.PreDialog()
        self.PreCreate(pre)
        get_resources().LoadOnDialog(pre, parent, "dlgSettings")
        self.PostCreate(pre)

        # Define variables for the controls, bind event handlers
        self.ctlRegion = xrc.XRCCTRL(self, "ctlRegion")
        self.ctlAccessKey = xrc.XRCCTRL(self, "ctlAccessKey")
        self.ctlSecret = xrc.XRCCTRL(self, "ctlSecret")
        self.ctlLaunchTemplate = xrc.XRCCTRL(self, "ctlLaunchTemplate")
        self.ctlKeyFileURI = xrc.XRCCTRL(self, "ctlKeyFileURI")
        self.radioOSSLFile = xrc.XRCCTRL(self, "radioOSSLFile")
        self.radioOSSLPKCS11 = xrc.XRCCTRL(self, "radioOSSLPKCS11")
        self.radioGPGSCD = xrc.XRCCTRL(self, "radioGPGSCD")

        self.Bind(wx.EVT_BUTTON, self.OnButton_wxID_OK, id=xrc.XRCID('wxID_OK'))
        self.Bind(wx.EVT_BUTTON, self.OnButton_wxID_CANCEL, id=xrc.XRCID('wxID_CANCEL'))
        self.Bind(wx.EVT_BUTTON, self.OnButton_wxID_APPLY, id=xrc.XRCID('wxID_APPLY'))
        self.Bind(wx.EVT_INIT_DIALOG, self.OnInit_dialog)

#!XRCED:begin-block:xrcdlgSettings.OnButton_wxID_OK
    def OnButton_wxID_OK(self, evt):
        # Replace with event handler code
        print "OnButton_wxID_OK()"
#!XRCED:end-block:xrcdlgSettings.OnButton_wxID_OK        

#!XRCED:begin-block:xrcdlgSettings.OnButton_wxID_CANCEL
    def OnButton_wxID_CANCEL(self, evt):
        # Replace with event handler code
        print "OnButton_wxID_CANCEL()"
#!XRCED:end-block:xrcdlgSettings.OnButton_wxID_CANCEL        

#!XRCED:begin-block:xrcdlgSettings.OnButton_wxID_APPLY
    def OnButton_wxID_APPLY(self, evt):
        # Replace with event handler code
        print "OnButton_wxID_APPLY()"
#!XRCED:end-block:xrcdlgSettings.OnButton_wxID_APPLY        

#!XRCED:begin-block:xrcdlgSettings.OnInit_dialog
    def OnInit_dialog(self, evt):
        # Replace with event handler code
        print "OnInit_dialog()"
#!XRCED:end-block:xrcdlgSettings.OnInit_dialog        


class xrcdlgWait(wx.Dialog):
#!XRCED:begin-block:xrcdlgWait.PreCreate
    def PreCreate(self, pre):
        """ This function is called during the class's initialization.
        
        Override it for custom setup before the window is created usually to
        set additional window styles using SetWindowStyle() and SetExtraStyle().
        """
        pass
        
#!XRCED:end-block:xrcdlgWait.PreCreate

    def __init__(self, parent):
        # Two stage creation (see http://wiki.wxpython.org/index.cgi/TwoStageCreation)
        pre = wx.PreDialog()
        self.PreCreate(pre)
        get_resources().LoadOnDialog(pre, parent, "dlgWait")
        self.PostCreate(pre)

        # Define variables for the controls, bind event handlers
        self.gauge = xrc.XRCCTRL(self, "gauge")

        self.Bind(wx.EVT_INIT_DIALOG, self.OnInit_dialog)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnWindow_destroy)

#!XRCED:begin-block:xrcdlgWait.OnInit_dialog
    def OnInit_dialog(self, evt):
        # Replace with event handler code
        print "OnInit_dialog()"
#!XRCED:end-block:xrcdlgWait.OnInit_dialog        

#!XRCED:begin-block:xrcdlgWait.OnClose
    def OnClose(self, evt):
        # Replace with event handler code
        print "OnClose()"
#!XRCED:end-block:xrcdlgWait.OnClose        

#!XRCED:begin-block:xrcdlgWait.OnWindow_destroy
    def OnWindow_destroy(self, evt):
        # Replace with event handler code
        print "OnWindow_destroy()"
#!XRCED:end-block:xrcdlgWait.OnWindow_destroy        


class xrcdlgSubnetPicker(wx.Dialog):
#!XRCED:begin-block:xrcdlgSubnetPicker.PreCreate
    def PreCreate(self, pre):
        """ This function is called during the class's initialization.
        
        Override it for custom setup before the window is created usually to
        set additional window styles using SetWindowStyle() and SetExtraStyle().
        """
        pass
        
#!XRCED:end-block:xrcdlgSubnetPicker.PreCreate

    def __init__(self, parent):
        # Two stage creation (see http://wiki.wxpython.org/index.cgi/TwoStageCreation)
        pre = wx.PreDialog()
        self.PreCreate(pre)
        get_resources().LoadOnDialog(pre, parent, "dlgSubnetPicker")
        self.PostCreate(pre)

        # Define variables for the controls, bind event handlers
        self.choiceSubnet = xrc.XRCCTRL(self, "choiceSubnet")
        self.wxID_OK = xrc.XRCCTRL(self, "wxID_OK")

        self.Bind(wx.EVT_CHOICE, self.OnChoice_choiceSubnet, self.choiceSubnet)
        self.Bind(wx.EVT_BUTTON, self.OnButton_wxID_OK, self.wxID_OK)
        self.Bind(wx.EVT_BUTTON, self.OnButton_wxID_CANCEL, id=xrc.XRCID('wxID_CANCEL'))
        self.Bind(wx.EVT_INIT_DIALOG, self.OnInit_dialog)

#!XRCED:begin-block:xrcdlgSubnetPicker.OnChoice_choiceSubnet
    def OnChoice_choiceSubnet(self, evt):
        # Replace with event handler code
        print "OnChoice_choiceSubnet()"
#!XRCED:end-block:xrcdlgSubnetPicker.OnChoice_choiceSubnet        

#!XRCED:begin-block:xrcdlgSubnetPicker.OnButton_wxID_OK
    def OnButton_wxID_OK(self, evt):
        # Replace with event handler code
        print "OnButton_wxID_OK()"
#!XRCED:end-block:xrcdlgSubnetPicker.OnButton_wxID_OK        

#!XRCED:begin-block:xrcdlgSubnetPicker.OnButton_wxID_CANCEL
    def OnButton_wxID_CANCEL(self, evt):
        # Replace with event handler code
        print "OnButton_wxID_CANCEL()"
#!XRCED:end-block:xrcdlgSubnetPicker.OnButton_wxID_CANCEL        

#!XRCED:begin-block:xrcdlgSubnetPicker.OnInit_dialog
    def OnInit_dialog(self, evt):
        # Replace with event handler code
        print "OnInit_dialog()"
#!XRCED:end-block:xrcdlgSubnetPicker.OnInit_dialog        




# ------------------------ Resource data ----------------------

def __init_resources():
    global __res
    __res = xrc.EmptyXmlResource()

    wx.FileSystem.AddHandler(wx.MemoryFSHandler())

    vgaming_xrc = '''\
<?xml version="1.0" ?><resource class="wxBoxSizer">
  <object class="wxFrame" name="mainframe">
    <object class="wxMenuBar" name="menuBar">
      <object class="wxMenu" name="mnuFile">
        <object class="wxMenuItem" name="wxID_EXIT">
          <label>E&amp;xit</label>
          <bitmap stock_id="wxART_QUIT"/>
          <XRCED>
            <events>EVT_MENU</events>
          </XRCED>
        </object>
        <label>&amp;File</label>
      </object>
      <object class="wxMenu" name="mnuEdit">
        <label>&amp;Edit</label>
        <object class="wxMenuItem" name="itmSettings">
          <label>&amp;Settings...</label>
          <bitmap stock_id="wxART_HELP_SETTINGS"/>
          <accel>Ctrl-E</accel>
          <XRCED>
            <events>EVT_MENU</events>
          </XRCED>
        </object>
      </object>
      <object class="wxMenu" name="mnuView">
        <label>&amp;View</label>
        <object class="wxMenuItem" name="itmRefresh">
          <label>&amp;Refresh</label>
          <accel>F5</accel>
          <XRCED>
            <events>EVT_MENU</events>
          </XRCED>
        </object>
      </object>
    </object>
    <object class="wxBoxSizer">
      <orient>wxVERTICAL</orient>
      <object class="sizeritem">
        <object class="wxFlexGridSizer">
          <object class="sizeritem">
            <object class="wxStaticText">
              <label>Status</label>
            </object>
            <flag>wxALIGN_RIGHT|wxALIGN_CENTRE_VERTICAL</flag>
          </object>
          <object class="sizeritem">
            <object class="wxTextCtrl" name="ctlStatus">
              <style>wxTE_READONLY</style>
              <XRCED>
                <assign_var>1</assign_var>
              </XRCED>
            </object>
            <flag>wxRIGHT|wxEXPAND</flag>
          </object>
          <object class="sizeritem">
            <object class="wxStaticText">
              <label>Instance ID</label>
            </object>
            <flag>wxALIGN_RIGHT|wxALIGN_CENTRE_VERTICAL</flag>
          </object>
          <object class="sizeritem">
            <object class="wxTextCtrl" name="ctlInstanceId">
              <style>wxTE_READONLY</style>
              <XRCED>
                <assign_var>1</assign_var>
              </XRCED>
            </object>
            <flag>wxRIGHT|wxEXPAND</flag>
          </object>
          <object class="sizeritem">
            <object class="wxStaticText">
              <label>Spot Request ID</label>
            </object>
            <flag>wxALIGN_RIGHT|wxALIGN_CENTRE_VERTICAL</flag>
          </object>
          <object class="sizeritem">
            <object class="wxTextCtrl" name="ctlSpotId">
              <style>wxTE_READONLY</style>
              <XRCED>
                <assign_var>1</assign_var>
              </XRCED>
            </object>
            <flag>wxRIGHT|wxEXPAND</flag>
          </object>
          <object class="sizeritem">
            <object class="wxStaticText">
              <label>Public IP</label>
            </object>
            <flag>wxALIGN_RIGHT|wxALIGN_CENTRE_VERTICAL</flag>
          </object>
          <object class="sizeritem">
            <object class="wxTextCtrl" name="ctlPublicIP">
              <style>wxTE_READONLY</style>
              <XRCED>
                <assign_var>1</assign_var>
              </XRCED>
            </object>
            <flag>wxRIGHT|wxEXPAND</flag>
          </object>
          <cols>2</cols>
          <vgap>4</vgap>
          <hgap>2</hgap>
          <growablecols>1</growablecols>
          <object class="sizeritem">
            <object class="wxStaticText">
              <label>Password</label>
            </object>
            <flag>wxALIGN_RIGHT|wxALIGN_CENTRE_VERTICAL</flag>
          </object>
          <object class="sizeritem">
            <object class="wxTextCtrl" name="ctlPassword">
              <style>wxTE_READONLY</style>
              <XRCED>
                <assign_var>1</assign_var>
              </XRCED>
            </object>
            <flag>wxRIGHT|wxEXPAND</flag>
          </object>
        </object>
        <flag>wxALL|wxEXPAND|wxGROW</flag>
        <border>7</border>
      </object>
      <object class="sizeritem">
        <object class="wxBoxSizer">
          <object class="sizeritem">
            <object class="wxButton" name="btnStart">
              <label>Start</label>
              <XRCED>
                <events>EVT_BUTTON</events>
              </XRCED>
            </object>
            <border>4</border>
          </object>
          <object class="sizeritem">
            <object class="wxButton" name="btnStop">
              <label>Stop</label>
              <XRCED>
                <events>EVT_BUTTON</events>
              </XRCED>
            </object>
            <flag>wxLEFT</flag>
            <border>4</border>
          </object>
          <object class="sizeritem">
            <object class="wxButton" name="btnRDP">
              <label>RDP</label>
              <XRCED>
                <events>EVT_BUTTON</events>
              </XRCED>
            </object>
            <flag>wxLEFT</flag>
            <border>4</border>
          </object>
          <object class="sizeritem">
            <object class="wxButton" name="btnDCV">
              <label>DCV</label>
              <XRCED>
                <events>EVT_BUTTON</events>
              </XRCED>
            </object>
            <flag>wxLEFT</flag>
            <border>4</border>
          </object>
          <orient>wxHORIZONTAL</orient>
        </object>
        <flag>wxBOTTOM|wxLEFT|wxRIGHT|wxALIGN_CENTRE|wxALIGN_BOTTOM</flag>
        <border>7</border>
      </object>
    </object>
    <title>vGaming</title>
    <style>wxCLIP_CHILDREN|wxDEFAULT_DIALOG_STYLE</style>
  </object>
  <object class="wxDialog" name="dlgSettings">
    <object class="wxBoxSizer">
      <orient>wxVERTICAL</orient>
      <object class="sizeritem">
        <object class="wxFlexGridSizer">
          <object class="sizeritem">
            <object class="wxStaticText">
              <label>Region</label>
            </object>
            <flag>wxALIGN_RIGHT|wxALIGN_CENTRE_VERTICAL</flag>
          </object>
          <object class="sizeritem">
            <object class="wxTextCtrl" name="ctlRegion">
              <XRCED>
                <assign_var>1</assign_var>
              </XRCED>
            </object>
            <flag>wxRIGHT|wxEXPAND</flag>
          </object>
          <object class="sizeritem">
            <object class="wxStaticText">
              <label>Access key ID</label>
            </object>
            <flag>wxALIGN_RIGHT|wxALIGN_CENTRE_VERTICAL</flag>
          </object>
          <object class="sizeritem">
            <object class="wxTextCtrl" name="ctlAccessKey">
              <XRCED>
                <assign_var>1</assign_var>
              </XRCED>
            </object>
            <flag>wxRIGHT|wxEXPAND</flag>
          </object>
          <object class="sizeritem">
            <object class="wxStaticText">
              <label>Secret access key</label>
            </object>
            <flag>wxALIGN_RIGHT|wxALIGN_CENTRE_VERTICAL</flag>
          </object>
          <object class="sizeritem">
            <object class="wxTextCtrl" name="ctlSecret">
              <XRCED>
                <assign_var>1</assign_var>
              </XRCED>
            </object>
            <flag>wxRIGHT|wxEXPAND</flag>
          </object>
          <object class="sizeritem">
            <object class="wxStaticText">
              <label>Launch template ID</label>
            </object>
            <flag>wxALIGN_RIGHT|wxALIGN_CENTRE_VERTICAL</flag>
          </object>
          <object class="sizeritem">
            <object class="wxTextCtrl" name="ctlLaunchTemplate">
              <XRCED>
                <assign_var>1</assign_var>
              </XRCED>
            </object>
            <flag>wxRIGHT|wxEXPAND</flag>
          </object>
          <cols>2</cols>
          <vgap>4</vgap>
          <hgap>2</hgap>
          <growablecols>1</growablecols>
          <growablerows/>
          <object class="sizeritem">
            <object class="wxStaticText">
              <label>Key File/URI</label>
            </object>
            <flag>wxALIGN_RIGHT|wxALIGN_CENTRE_VERTICAL</flag>
          </object>
          <object class="sizeritem">
            <object class="wxTextCtrl" name="ctlKeyFileURI">
              <XRCED>
                <assign_var>1</assign_var>
              </XRCED>
            </object>
            <flag>wxRIGHT|wxEXPAND</flag>
          </object>
        </object>
        <flag>wxALL|wxEXPAND|wxGROW</flag>
        <border>7</border>
      </object>
      <object class="sizeritem">
        <object class="wxStaticBoxSizer">
          <label>Password Decryption</label>
          <orient>wxHORIZONTAL</orient>
          <object class="sizeritem">
            <object class="wxRadioButton" name="radioOSSLFile">
              <label>OpenSSL &amp;File</label>
              <style>wxRB_GROUP</style>
              <XRCED>
                <assign_var>1</assign_var>
              </XRCED>
            </object>
          </object>
          <object class="sizeritem">
            <object class="wxRadioButton" name="radioOSSLPKCS11">
              <label>OpenSSL &amp;PKCS#11</label>
              <XRCED>
                <assign_var>1</assign_var>
              </XRCED>
            </object>
          </object>
          <object class="sizeritem">
            <object class="wxRadioButton" name="radioGPGSCD">
              <label>GnuPG &amp;SCDaemon</label>
              <XRCED>
                <assign_var>1</assign_var>
              </XRCED>
            </object>
          </object>
        </object>
        <flag>wxBOTTOM|wxLEFT|wxRIGHT|wxEXPAND</flag>
        <border>7</border>
      </object>
      <object class="sizeritem">
        <object class="wxStdDialogButtonSizer">
          <object class="button">
            <object class="wxButton" name="wxID_OK">
              <label>&amp;OK</label>
              <default>1</default>
              <XRCED>
                <events>EVT_BUTTON</events>
              </XRCED>
            </object>
          </object>
          <object class="button">
            <object class="wxButton" name="wxID_CANCEL">
              <label>&amp;Cancel</label>
              <XRCED>
                <events>EVT_BUTTON</events>
              </XRCED>
            </object>
          </object>
          <object class="button">
            <object class="wxButton" name="wxID_APPLY">
              <label>&amp;Apply</label>
              <XRCED>
                <events>EVT_BUTTON</events>
              </XRCED>
            </object>
          </object>
        </object>
        <flag>wxBOTTOM|wxLEFT|wxRIGHT|wxALIGN_CENTRE|wxALIGN_BOTTOM</flag>
        <border>7</border>
      </object>
    </object>
    <title>Settings</title>
    <style>wxCLIP_CHILDREN|wxDEFAULT_DIALOG_STYLE</style>
    <XRCED>
      <events>EVT_INIT_DIALOG</events>
    </XRCED>
  </object>
  <object class="wxDialog" name="dlgWait">
    <object class="wxBoxSizer">
      <orient>wxVERTICAL</orient>
      <object class="sizeritem">
        <object class="wxStaticText">
          <label>Please wait...</label>
        </object>
        <flag>wxTOP|wxLEFT|wxRIGHT|wxEXPAND</flag>
        <border>7</border>
      </object>
      <object class="sizeritem">
        <object class="wxGauge" name="gauge">
          <size>300,-1</size>
          <style>wxGA_HORIZONTAL|wxGA_SMOOTH</style>
          <XRCED>
            <assign_var>1</assign_var>
          </XRCED>
        </object>
        <flag>wxALL|wxEXPAND</flag>
        <border>7</border>
      </object>
    </object>
    <title>Please wait...</title>
    <centered>1</centered>
    <style>wxCLIP_CHILDREN|wxCAPTION|wxSTAY_ON_TOP|wxSYSTEM_MENU</style>
    <XRCED>
      <events>EVT_INIT_DIALOG|EVT_CLOSE|EVT_WINDOW_DESTROY</events>
    </XRCED>
  </object>
  <object class="wxDialog" name="dlgSubnetPicker">
    <object class="wxBoxSizer">
      <orient>wxVERTICAL</orient>
      <object class="sizeritem">
        <object class="wxStaticBoxSizer">
          <object class="sizeritem">
            <object class="wxChoice" name="choiceSubnet">
              <size>200,-1</size>
              <content>
                <item/>
              </content>
              <XRCED>
                <events>EVT_CHOICE</events>
                <assign_var>1</assign_var>
              </XRCED>
            </object>
            <flag>wxALL|wxEXPAND</flag>
            <border>7</border>
          </object>
          <label>Subnet</label>
          <orient>wxVERTICAL</orient>
        </object>
        <flag>wxTOP|wxLEFT|wxRIGHT|wxEXPAND|wxGROW</flag>
        <border>7</border>
      </object>
      <object class="sizeritem">
        <object class="wxStdDialogButtonSizer">
          <object class="button">
            <object class="wxButton" name="wxID_OK">
              <label>&amp;OK</label>
              <default>1</default>
              <enabled>0</enabled>
              <XRCED>
                <events>EVT_BUTTON</events>
                <assign_var>1</assign_var>
              </XRCED>
            </object>
          </object>
          <object class="button">
            <object class="wxButton" name="wxID_CANCEL">
              <label>&amp;Cancel</label>
              <XRCED>
                <events>EVT_BUTTON</events>
              </XRCED>
            </object>
          </object>
        </object>
        <flag>wxBOTTOM|wxLEFT|wxRIGHT|wxEXPAND|wxALIGN_CENTRE|wxALIGN_BOTTOM</flag>
        <border>7</border>
      </object>
    </object>
    <title>Select a subnet</title>
    <centered>1</centered>
    <style>wxCLIP_CHILDREN|wxDEFAULT_DIALOG_STYLE</style>
    <XRCED>
      <events>EVT_INIT_DIALOG</events>
    </XRCED>
  </object>
</resource>'''

    wx.MemoryFSHandler.AddFile('XRC/vgaming/vgaming_xrc', vgaming_xrc)
    __res.Load('memory:XRC/vgaming/vgaming_xrc')


# ----------------------- Gettext strings ---------------------

def __gettext_strings():
    # This is a dummy function that lists all the strings that are used in
    # the XRC file in the _("a string") format to be recognized by GNU
    # gettext utilities (specificaly the xgettext utility) and the
    # mki18n.py script.  For more information see:
    # http://wiki.wxpython.org/index.cgi/Internationalization 
    
    def _(str): pass
    
    _("E&xit")
    _("&File")
    _("&Edit")
    _("&Settings...")
    _("&View")
    _("&Refresh")
    _("Status")
    _("Instance ID")
    _("Spot Request ID")
    _("Public IP")
    _("Password")
    _("Start")
    _("Stop")
    _("RDP")
    _("DCV")
    _("vGaming")
    _("Region")
    _("Access key ID")
    _("Secret access key")
    _("Launch template ID")
    _("Key File/URI")
    _("Password Decryption")
    _("OpenSSL &File")
    _("OpenSSL &PKCS#11")
    _("GnuPG &SCDaemon")
    _("&OK")
    _("&Cancel")
    _("&Apply")
    _("Settings")
    _("Please wait...")
    _("Please wait...")
    _("Subnet")
    _("&OK")
    _("&Cancel")
    _("Select a subnet")

