#!/usr/bin/python

import kivy
import logging
import argparse
from autosportlabs.racecapture.views.channels.channelsview import ChannelsView
kivy.require('1.8.0')
from kivy.config import Config
Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '576')

from kivy.app import App, Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.garden.navigationdrawer import NavigationDrawer

from rcpserial import *
from channels import *
from utils import *
from autosportlabs.racecapture.views.configuration.rcp.configview import ConfigView
from autosportlabs.racecapture.menu.mainmenu import MainMenu

from toolbarview import ToolbarView

class RaceCaptureApp(App):
    #Central configuration object
    rcpConfig  = RcpConfig()
    
    #List of Channels
    channels = Channels()
    
    #RaceCapture serial I/O 
    rcpComms = RcpSerial()
    
    #Main Views
    configView = None
    channelsView = None
    
    #main navigation menu 
    mainNav = None
    
    #main content view
    mainView = None
    
    #collection of main views to be swapped into mainView 
    mainViews = {}
    
    def __init__(self, **kwargs):
        self.register_event_type('on_config_updated')
        self.register_event_type('on_channels_updated')
        super(RaceCaptureApp, self).__init__(**kwargs)
        self.processArgs()

    def processArgs(self):
        parser = argparse.ArgumentParser(description='Autosport Labs Race Capture App')
        parser.add_argument('-p','--port', help='Port', required=False)
        args = vars(parser.parse_args())
        self.rcpComms.setPort(args['port'])

        if not self.rcpComms.port:
            self.rcpComms.autoDetect()

    def _serial_warning(self):
        popup = Popup(title='Warning',
                      content=Label(text='You have not selected a serial port'),
                      size_hint=(None, None), size=(400, 400))
        popup.open()

    def on_main_menu_item(self, instance, value):
        self.mainNav.toggle_state()
        self.switchMainView(value)
        
    def on_main_menu(self, instance, *args):
        self.mainNav.toggle_state()
        
    def on_write_config(self, instance, *args):
        rcpConfig = self.rcpConfig
        rcpJson = rcpConfig.toJson()

        try:
            self.rcpComms.writeRcpCfg(rcpJson)
        except:
            logging.exception('')
            self._serial_warning()
    
        
    def on_read_config(self, instance, *args):
        try:
            if not self.channels.isLoaded():
                channelsList = self.rcpComms.getChannels()
                self.channels.fromJson(channelsList)
                self.notifyChannelsUpdated()
                
                
            config = self.rcpComms.getRcpCfg()
            self.rcpConfig.fromJson(config)
            self.dispatch('on_config_updated', self.rcpConfig)
        except:
            logging.exception('')
            self._serial_warning()

    def notifyChannelsUpdated(self):
        self.dispatch('on_channels_updated', self.channels)

    def on_config_updated(self, rcpConfig):
        self.configView.dispatch('on_config_updated', rcpConfig)

    def on_channels_updated(self, channels):
        for view in self.mainViews.itervalues():
            view.dispatch('on_channels_updated', channels)

    def switchMainView(self, viewKey):
        mainView = self.mainViews.get(viewKey)
        if mainView:
            self.mainView.clear_widgets()
            self.mainView.add_widget(mainView)

        
    def build(self):
        Builder.load_file('racecapture.kv')
        toolbar = kvFind(self.root, 'rcid', 'statusbar')
        toolbar.bind(on_main_menu=self.on_main_menu)    
        toolbar.bind(on_read_config=self.on_read_config)
        toolbar.bind(on_write_config=self.on_write_config)
        
        mainMenu = kvFind(self.root, 'rcid', 'mainMenu')
        mainMenu.bind(on_main_menu_item=self.on_main_menu_item)

        self.mainView = kvFind(self.root, 'rcid', 'main')
        
        self.mainNav = kvFind(self.root, 'rcid', 'mainNav')
        
        #reveal_below_anim
        #reveal_below_simple
        #slide_above_anim
        #slide_above_simple
        #fade_in
        self.mainNav.anim_type = 'slide_above_anim'

        
        self.configView = ConfigView(channels=self.channels)
        self.channelsView = ChannelsView(channels=self.channels)
        
        self.mainViews = {'config' : self.configView, 
                          'channels' : self.channelsView}
            
if __name__ == '__main__':

    RaceCaptureApp().run()
