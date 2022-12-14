import os
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from kivy.properties import StringProperty
from utils import config


class PlayerProfile(Screen):
    icon_src = StringProperty('icons/profileicon/none.png')
    player_rank_img = StringProperty('icons/profileicon/none.png')
    player_details = StringProperty('None Found')
    player_rank_details = StringProperty('None Found')
    banner_src = StringProperty()
    champ1 = StringProperty('icons/profileicon/none.png')
    champ2 = StringProperty('icons/profileicon/none.png')
    champ3 = StringProperty('icons/profileicon/none.png')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.api_key_box = MDDialog(title='Add Api Key:',
                                    type='custom',
                                    content_cls=MDTextField(
                                        hint_text='Api-Key'),
                                    buttons=[MDFlatButton(text='Add',
                                                          on_release=self.validate_api_key)])

        if config.profile.player_data['level'] is not None:
            self.refresh_profile_page()

    def refresh_profile_page(self):
        '''
            This refreshes the profile page.
        '''
        if not config.profile.refresh_player_data():
            return

        self.icon = config.profile.player_data['icon']
        self.level = config.profile.player_data['level']
        self.tier = config.profile.player_data['tier']
        self.rank = config.profile.player_data['rank']
        self.wins = config.profile.player_data['wins']
        self.losses = config.profile.player_data['losses']
        champ1 = config.profile.player_data['champ1'][0]
        champ2 = config.profile.player_data['champ2'][0]
        champ3 = config.profile.player_data['champ3'][0]

        self.player_details = f'{config.profile.name}\nLevel: {self.level}'
        self.player_rank_details = f'{self.tier.capitalize()} {self.rank}\n{self.wins} Wins / {self.losses} Losses'
        self.icon_src = f'icons/profileicon/{self.icon}.png'
        self.player_rank_img = f'icons/tiers/Emblem_{self.tier.capitalize()}.png'
        self.champ1 = f'icons/champ_images/{champ1.lower()}.png'
        self.champ2 = f'icons/champ_images/{champ2.lower()}.png'
        self.champ3 = f'icons/champ_images/{champ3.lower()}.png'
        self.banner_src = f'icons/banners/{champ1.capitalize()}_0.jpg'

        if not os.path.isfile(self.icon_src):
            self.icon_src = 'icons/profileicon/none.png'
        if not os.path.isfile(self.champ1):
            self.champ1 = 'icons/profileicon/none.png'
        if not os.path.isfile(self.champ2):
            self.champ2 = 'icons/profileicon/none.png'
        if not os.path.isfile(self.champ3):
            self.champ3 = 'icons/profileicon/none.png'

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
