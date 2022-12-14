from kivymd.uix.list import OneLineAvatarIconListItem, OneLineListItem
from kivymd.uix.behaviors import HoverBehavior
from kivy.properties import StringProperty, ObjectProperty
from kivymd.uix.list import IconRightWidget, OneLineIconListItem
from kivymd.app import MDApp

class _CustomIconRightWidget(IconRightWidget):
    '''
        Icon that contains an instance variable pointing to the rune that it is on.
    '''
    rune = ObjectProperty()

class CustomOneLineListItem(OneLineListItem, HoverBehavior):
    '''
        These are the list items that appear when selecting account button.
    '''
    def on_enter(self):
        self.app = MDApp.get_running_app()
        self.text_color = self.app.theme_cls.primary_color

    def on_leave(self):
        self.text_color = self.app.theme_cls.text_color

class CustomIconAvatarListItem(OneLineAvatarIconListItem, HoverBehavior):
    '''
        This class represents the widgets used for the runes on
        the library page.
    '''
    text = StringProperty()
    source = StringProperty()

    def on_enter(self):
        self.app = MDApp.get_running_app()
        self.bg_color = self.app.theme_cls.bg_light

        self.right_icon = _CustomIconRightWidget(icon='dots-vertical',
                                                rune=self)
        self.right_icon.bind(on_release=self.open_drop_menu)

        self.add_widget(self.right_icon)
    
    def on_leave(self):
        self.bg_color = self.app.theme_cls.bg_normal
        self.children[0].remove_widget(self.right_icon)

class CustomIconListItem(OneLineIconListItem, HoverBehavior):
    '''
        A OneLineIconListItem with hoverbehaviour.
    '''
    icon = StringProperty()

    def on_enter(self):
        self.app = MDApp.get_running_app()
        self.text_color = self.app.theme_cls.primary_color

    def on_leave(self): 
        self.text_color = self.app.theme_cls.text_color

class NavItem(CustomIconListItem):
    '''
        Navigation items in navigation bar used on Home pages 
        (Profile, Rune Library, Match History).
    '''
    def on_enter(self):
        self.app = MDApp.get_running_app()
        if self.text_color != self.app.theme_cls.primary_color:
            self.text_color = self.app.theme_cls.primary_light

    def on_leave(self):
        if self.text_color != self.app.theme_cls.primary_color:
            self.text_color = self.app.theme_cls.text_color