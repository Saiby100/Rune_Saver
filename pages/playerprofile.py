from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.label import MDLabel
from utils import config

class PlayerProfile(Screen):
    '''TODO: Work on profile screen design'''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.api_key_box = MDDialog(title='Add Api Key:',
                                    type='custom',
                                    content_cls=MDTextField(hint_text='Api-Key'),
                                    buttons=[MDFlatButton(text='Add',
                                    on_release=self.validate_api_key)])

        if config.profile.player_data['level'] is not None: 
            self.refresh_profile_page()

    def refresh_profile_page(self):
        '''
            This refreshes the profile page.
        '''
        self.ids.box.clear_widgets()
            
        for key in config.profile.player_data.keys():
            self.ids.box.add_widget(MDLabel(text=f'{key.title()}: {str(config.profile.player_data[key])}',
                                            halign='center'))

    def validate_api_key(self, event):
        '''
            This checks if the entered api key is valid.
        '''
        if len(self.api_key_box.content_cls.text.strip()) == 0:
            return

        if not config.profile.key_is_valid(self.api_key_box.content_cls.text):
            Snackbar(text='Invalid Api Key', duration=1).open()
            return
        
        else:
            self.refresh_profile_page()
            self.api_key_box.content_cls.text = ''
            self.api_key_box.dismiss()
    
    def check_local_api_key(self):
        '''
            Checks if the local api key is valid
            Used in kv file
        '''
        if not config.profile.key_is_valid(None):
            self.api_key_box.open()
        else: 
            self.refresh_profile_page()