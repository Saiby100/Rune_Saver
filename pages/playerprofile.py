from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from kivy.uix.image import Image
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
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
        self.ids.profile_details_grid.clear_widgets()

        self.icon = config.profile.player_data['icon']
        self.icon_src = f'icons/profileicon/{self.icon}.png'
        self.level = config.profile.player_data['level']
        self.tier = config.profile.player_data['tier']
        self.rank = config.profile.player_data['rank']
        self.wins = config.profile.player_data['wins']
        self.losses = config.profile.player_data['losses']

        self.details_box = MDBoxLayout(orientation='vertical',
                                       size_hint_y=None)

        self.details_box.add_widget(MDLabel(text=config.profile.name,
                                            font_style='H5'))
        self.details_box.add_widget(MDLabel(text=f'Level: {self.level}',
                                            font_style='H5'))

        self.ids.profile_details_grid.add_widget(Image(source=self.icon_src))
        self.ids.profile_details_grid.add_widget(self.details_box)

        self.rank_details_box = MDBoxLayout(orientation='vertical',
                                            size_hint_y=None)

        self.rank_details_box.add_widget(MDLabel(text=self.tier,
                                                 font_style='H5'))
        self.rank_details_box.add_widget(MDLabel(text=f'Wins: {self.wins} / Losses: {self.losses}',
                                                 font_style='H5'))

        self.ids.rank_details_grid.add_widget(Image(source=f'icons/tiers/Emblem_{self.tier.upper()}.png'))
        self.ids.rank_details_grid.add_widget(self.rank_details_box)

        # self.name = config.profile.name
        # self.level = config.profile.player_data['level']
        # self.icon = config.profile.player_data['icon']
        # self.icon_src = f'icons/profileicon/{self.icon}.png'

        # self.tier = config.profile.player_data['tier']
        # self.rank = config.profile.player_data['rank']

        # self.wins = config.profile.player_data['wins']
        # self.losses = config.profile.player_data['losses']

        # self.ids.details_grid.add_widget(Image(source=self.icon_src))
        # self.ids.details_box.add_widget(MDLabel(text=self.name))
        # self.ids.details_box.add_widget(MDLabel(text=self.level))

        # for key in config.profile.player_data.keys():
        #     self.ids.box.add_widget(MDLabel(text=f'{key.title()}: {str(config.profile.player_data[key])}',
        #                                     halign='center'))

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