import kivy
kivy.require('1.8.0')
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.app import Builder
from kivy.uix.accordion import Accordion, AccordionItem
from autosportlabs.widgets.separator import HSeparator
from utils import *
from rcpconfig import *
from channels import Channels, Channel

Builder.load_file('autosportlabs/racecapture/views/channels/channelsview.kv')

class ChannelView(BoxLayout):
    channel = None
    name = None
    def __init__(self, **kwargs):
        super(ChannelView, self).__init__(**kwargs)
        self.channel = kwargs.get('channel', None)
        self.name = kwargs.get('name', '')
        kvFind(self, 'rcid', 'name').text = self.channel.name + ' (System)' if self.channel.systemChannel else ''

class ChannelEditor(BoxLayout):
    channel = None
    def __init__(self, **kwargs):
        super(ChannelEditor, self).__init__(**kwargs)
        self.channel = kwargs.get('channel', None)

class ChannelsView(BoxLayout):
    channelsContainer = None
    channels = None
    def __init__(self, **kwargs):
        super(ChannelsView, self).__init__(**kwargs)
        self.register_event_type('on_channels_updated')
        self.channelsContainer = kvFind(self, 'rcid', 'channelsContainer')
     
    def on_channels_updated(self, channels):
        self.channelsContainer.clear_widgets()
        for channel in channels.items:
            self.channelsContainer.add_widget(ChannelView(channel=channel))
        kvFind(self, 'rcid', 'addChan').disabled = False
            

