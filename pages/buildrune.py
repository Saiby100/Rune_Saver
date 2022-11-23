from Widgets import Rune
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty
from utils import config

class BuildRune(Screen):
    '''
        This page is used for building/customizing runes.
    '''
    title = StringProperty('Place Holder')
    previous = ObjectProperty(None)
    rune = ObjectProperty(None)
    champion = StringProperty(None)
    edit = BooleanProperty(False)
    
    def go_back(self, event):
        '''
            This goes to the previous page that it was 
            called from (Library or ChampSelect).
        '''
        config.sm.current = self.previous
        
    def on_leave(self, *args):
        '''
            This resets the widgets on this page when
            leaving the page.
        '''
        self.edit = False
        self.ids.primary.reset()
        self.ids.secondary.reset()

    def save_rune(self, event):
        '''
            This saves the new/edited Rune and adds it
            to the Rune widgets on the libary page.
            Once saved, user is moved back to library page.
        '''
        try:
            rune_info = [self.champion.lower(), self.dialog_btn.content_cls.text]
            primary_attrs = self.ids.primary.drawer_titles()
            secondary_attrs = self.ids.secondary.drawer_titles()
            rune_info+=primary_attrs+secondary_attrs

        
            if not self.edit:
                rune = Rune(row=rune_info)
                i = config.saved_runes.add_new_rune(rune, 0, config.saved_runes.size-1)
                config.sm.get_screen('library').add_new_rune(rune, i)
            else:
                self.rune.edit(rune_info)

        except (ValueError, AttributeError): 
            Snackbar(text='Rune Incomplete', duration=1).open()
            return

        self.close_box()
        Snackbar(text='Rune Saved Successfully!', duration=1).open()
        config.sm.current = 'library'

    def show_save_box(self):
        '''
            This initializes and displays the dialog box
            for naming the new rune.
        '''
        save_btn = MDFlatButton(text='SAVE', on_release=self.save_rune)
        back_btn = MDFlatButton(text='CANCEL', on_release=self.close_box)

        self.dialog_btn = MDDialog(title='Rune Name:',
                                   type='custom',
                                   content_cls=MDTextField(text=self.ids.toolbar.title),
                                   buttons=[back_btn, save_btn])
        self.dialog_btn.open()

    def close_box(self, event=None):
        '''
            This closes the dialog box for naming a new rune.
        '''
        self.dialog_btn.dismiss()