from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from kivy.properties import StringProperty
from utils import config


class PlayerProfile(Screen):
    icon = StringProperty('icons/profileicon/none.png')
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

        if config.profile.player.hasdata:
            self.refresh_profile_page()

    def refresh_profile_page(self, local=True):
        '''
            This refreshes the profile page.
        '''
        if not local:
            if not config.profile.fetch_player_api_data(None):
                return

        self.icon = config.profile.player.icon_src()
        self.level = config.profile.player.level
        self.tier = config.profile.player.tier
        self.rank = config.profile.player.rank
        self.wins = config.profile.player.wins
        self.losses = config.profile.player.losses
        champ1 = config.profile.player.champ1[0]

        self.player_details = f'{config.profile.name}\nLevel: {self.level}'
        self.player_rank_details = f'{self.tier.capitalize()} {self.rank}\n{self.wins} Wins / {self.losses} Losses'
        self.player_rank_img = config.profile.player.rank_emblem()
        self.champ1 = config.profile.player.champ1_img()
        self.champ2 = config.profile.player.champ2_img()
        self.champ3 = config.profile.player.champ3_img()

        self.banner_src = f'icons/banners/{champ1.capitalize()}_0.jpg'

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
            self.refresh_profile_page(False)
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
            self.refresh_profile_page(False)
