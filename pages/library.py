from .playerprofile import PlayerProfile
from .champselect import ChampSelect
from .viewrune import ViewRune
from .matchhistory import MatchHistory
from widgets.listitems import CustomIconListItem
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextField
from functools import partial
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from utils import config
from kivymd.uix.button import MDRoundFlatIconButton


class Library(Screen):
    '''Page with user's saved runes.'''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        '''
            Initializing Layouts
        '''
        menu_items = [
            {
                'text': title,
                'viewclass': 'CustomOneLineListItem',
                'on_release': lambda x=title: self.drop_menu_button(x),
                'height': dp(56),
                'divider': None
            } for title in ['Switch profile', 'Rename profile', 'Delete profile']
        ]
        self.drop_menu = MDDropdownMenu(
            items=menu_items,
            width_mult=2.7
        )

        rune_menu_items = [
            {
                'text': title[0],
                'viewclass': 'CustomIconListItem',
                'on_release': lambda x=title[0]: self.select_drop_menu_option(x),
                'height': dp(45),
                'icon': title[1]
            } for title in [['edit', 'pencil'], ['delete', 'trash-can']]
        ]
        self.rune_drop_menu = MDDropdownMenu(
            items=rune_menu_items,
            width_mult=2.6
        )

        for rune in config.saved_runes.runes:
            self.ids.my_runes.add_widget(rune)

    def select_drop_menu_option(self, title):
        '''
            This opens the menu for selecting rune actions.
            This is called by 'dots-vertical' icon that appears on-hover for a rune
        '''
        rune = self.rune_drop_menu.caller.rune
        self.rune_drop_menu.dismiss()
        if title == 'edit':
            self.edit_rune(rune)
        else:
            self.delete_rune(rune)

    def make_rune_list(self, text='', search=False):
        '''TODO: Implement search bar'''
        '''Searching for a rune'''
        def add_rune(row):

            self.ids.my_runes.data.append(
                {
                    'viewclass': 'Rune',
                    'row': row
                }
            )

        self.ids.my_runes.data = []
        for rune in config.saved_runes.to_array():
            if search:
                if text in rune[1]:
                    add_rune(rune)
            else:
                add_rune(rune)

    def profile_name(self):
        '''
            Returns the current profile name.
            This is called from the kv file.
        '''
        return config.profile.name

    def drop_menu_button(self, title):
        ''' 
            Displays menu to delete or rename account
        '''
        self.profile_box = None

        if title == 'Delete profile':
            buttons = [
                MDFlatButton(
                    text='No', on_release=lambda x: self.profile_box.dismiss()),
                MDFlatButton(
                    text='Yes', on_release=lambda x: self.delete_profile())
            ]
            self.profile_box = MDDialog(
                text=f'Are you sure you want to delete \'{config.profile.name}\'?',
                buttons=buttons,
                padding=5
            )
            self.profile_box.open()

        elif title == 'Rename profile':
            self.profile_box = MDDialog(
                title='Profile name:',
                type='custom',
                content_cls=MDTextField(text=config.profile.name),
                buttons=[MDFlatButton(
                    text='Rename', on_release=self.rename_profile)]
            )
            self.profile_box.open()

        else:
            self.open_dialog_box()

        self.drop_menu.dismiss()

    def rename_profile(self, event):
        '''
            This renames the current profile.
        '''
        name = self.profile_box.content_cls.text

        if not config.profile.rename(name):
            # Rename unsuccessful
            Snackbar(
                text='A profile already exists with that name',
                duration=1
            ).open()
            return

        self.update_account_btn(config.profile.name)
        self.profile_box.dismiss()

    def delete_profile(self):
        '''
            This deletes the current profile.
        '''
        if config.profile.delete_profile():
            # Deletion successful
            config.saved_runes.change_account(config.profile.get_rune_data())

            self.ids.my_runes.clear_widgets()

            for rune in config.saved_runes.runes:
                self.ids.my_runes.add_widget(rune)

        self.update_account_btn(config.profile.name)
        config.sm.remove_widget(config.sm.get_screen('profile'))
        config.sm.add_widget(PlayerProfile(name='profile'))
        self.profile_box.dismiss()

    def view_rune(self, rune):
        '''
            This initializes a ViewRune page and adds it to screen manager (sm)
            This is called when a rune is selected in library.
        '''
        self.rune = rune
        config.sm.add_widget(ViewRune(name='view_page'))
        config.sm.current = 'view_page'

    def champ_select(self):
        '''
            This goes to champion select page.
            A ChampSelect page is initialzed when this is 
            first called.
        '''
        if not config.sm.has_screen('champ_select'):
            config.sm.add_widget(ChampSelect(name='champ_select'))

        config.sm.current = 'champ_select'

    def delete_rune(self, rune):
        '''
            Deletes a rune on library page.
        '''
        config.saved_runes.delete_rune(rune)
        self.ids.my_runes.remove_widget(rune)

    def open_dialog_box(self):
        '''
            Opens the box for switching accounts.
            This is called after selecting switch profile option.
        '''
        items = []
        for account in config.profile.get_all_profiles():
            item = CustomIconListItem(
                text=account.strip('.csv'),
                icon='account-circle'
            )

            item.bind(
                on_release=partial(self.switch_profile, account.strip('.csv'))
            )
            items.append(item)

        add_account_item = CustomIconListItem(
            text='Add Profile',
            icon='account-plus'
        )
        add_account_item.bind(on_release=self.get_profile_name)
        items.append(add_account_item)

        self.dialog_box = MDDialog(
            title='Choose Profile:',
            type='simple',
            items=items
        )
        self.dialog_box.open()

    def switch_profile(self, account, event):
        '''
            This saves all profile data and switches to the
            specified profile.
            This is called when user chose a profile to switch to,
            or after creating a new profile.
        '''
        if account == config.profile.name:
            self.dialog_box.dismiss()
            return

        config.profile.save(config.saved_runes.to_array())
        config.profile.set_current(account)
        config.saved_runes.change_account(config.profile.get_rune_data())

        self.ids.my_runes.clear_widgets()

        for rune in config.saved_runes.runes:
            self.ids.my_runes.add_widget(rune)

        self.update_account_btn(self.profile_name())
        config.sm.remove_widget(config.sm.get_screen('profile'))
        config.sm.remove_widget(config.sm.get_screen('match_history'))

        config.sm.add_widget(PlayerProfile(name='profile'))
        config.sm.add_widget(MatchHistory(name='match_history'))

        try:
            # Called after creating a new profile.
            self.dialog_box.dismiss()

        except AttributeError:
            # Called after selecting a profile.
            return

    def update_account_btn(self, name):
        self.ids.account_btn_layout.clear_widgets()

        new_button = MDRoundFlatIconButton(
            icon='account-circle',
            text=name
        )
        new_button.bind(on_release=self.open_account_options)

        self.ids.account_btn_layout.add_widget(new_button)

    def open_account_options(self, event):
        self.drop_menu.caller = event
        self.drop_menu.open()

    def get_profile_name(self, event):
        '''
            This opens the dialog box for creating a new account.
            This is called by create new account button.
        '''
        if len(config.profile.get_all_profiles()) >= 4:
            Snackbar(
                text='Max Accounts Reached',
                duration=1
            ).open()
            return
        self.create_account_box = MDDialog(
            title='Profile name:',
            type='custom',
            content_cls=MDTextField(),
            buttons=[MDFlatButton(
                text='Create', on_release=self.create_profile)]
        )
        self.create_account_box.open()

    def create_profile(self, event):
        '''
            This creates a new profile and switches to
            the new profile.
        '''
        profile_name = self.create_account_box.content_cls.text
        if not config.profile.create_new_profile(profile_name):
            Snackbar(
                text=f'\'{profile_name}\' already exists',
                duration=1
            ).open()
            return

        self.switch_profile(profile_name, None)
        Snackbar(text='Profile Successfully created!', duration=1).open()

        self.create_account_box.dismiss()
        self.dialog_box.dismiss()

    def edit_rune(self, rune):
        '''
            This sets up the rune page and moves to it.
        '''
        screen = config.sm.get_screen('rune_page')
        screen.ids.primary.preset(rune.attributes()[:5])
        screen.ids.secondary.preset(rune.attributes()[5:])

        screen.champion = rune.champ
        screen.title = rune.name
        screen.rune = rune
        screen.edit = True
        screen.previous = self.name
        config.sm.current = 'rune_page'

    def add_new_rune(self, rune, index):
        '''
            This adds the specified rune to the layout.
        '''
        i = config.saved_runes.size - 1 - index
        self.ids.my_runes.add_widget(rune, i)
