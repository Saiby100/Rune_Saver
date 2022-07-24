from kivy.properties import Clock
from Widgets import *
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextField
from functools import partial
from kivymd.uix.dialog import MDDialog
import atexit
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from Profile import Profile
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.recycleview import RecycleView
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout

Window.minimum_width, Window.minimum_height = (705, 500)
Window.size = (980, 670)

profile = Profile()

class RuneSaver(MDApp):
    '''App manager.'''
    def build(self):
        # 
        global sm, saved_runes

        saved_runes = SavedRunes(profile.data())
        '''Valid themes: 'Light' or 'Dark'.'''
        self.theme_cls.theme_style = "Dark"
        '''Valid Themes: Red, Pink, Purple, DeepPurple, Indigo, Blue,
           LightBlue, Cyan, Teal, Green, LightGreen, Lime, Yellow,
           Amber, Orange, DeepOrange, Brown, Gray, BlueGray'''
        self.theme_cls.primary_palette = "BlueGray"
        
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(SplashScreen(name='splash'))

        return sm

    def on_start(self):
        # Clock.schedule_once(self.add_screens, 2)
        self.add_screens(None)

    def add_screens(self, event):
        sm.add_widget(Library(name='library'))
        sm.add_widget(BuildRune(name='rune_page'))
        sm.add_widget(PlayerProfile(name='profile'))
        sm.add_widget(MatchHistory(name='match_history'))
        sm.current = 'library'
        sm.remove_widget(sm.get_screen('splash'))
    
    def change_screen(self, screen_name):
         if sm.current == screen_name: 
            return
         sm.current = screen_name


class SplashScreen(Screen):
    '''Displays on app launch.'''
    pass 

class PlayerProfile(Screen):
    '''TODO: Work on profile screen design'''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.api_key_box = MDDialog(title='Add Api Key:',
                                    type='custom',
                                    content_cls=MDTextField(hint_text='Api-Key'),
                                    buttons=[MDFlatButton(text='Add',
                                    on_release=self.validate_api_key)])

        if profile.player['level'] is not None: 
            self.refresh_player_info()

    def refresh_player_info(self):
        '''Refreshes the profile page'''
        self.ids.box.clear_widgets()
            
            # self.box = MDBoxLayout(orientation='vertical')
        for key in profile.player.keys():
            self.ids.box.add_widget(MDLabel(text=f'{key.title()}: {str(profile.player[key])}',
                                            halign='center'))

    def validate_api_key(self, event):
        '''Checks if the api key is valid'''
        if len(self.api_key_box.content_cls.text.strip()) == 0:
            return

        if not profile.add_key(self.api_key_box.content_cls.text):
            Snackbar(text='Invalid Api Key', duration=1).open()
            return
        
        else:
            self.refresh_player_info()
            self.api_key_box.dismiss()
    
    def check_local_api_key(self):
        '''Checks if the local api key is valid'''
        if not profile.add_key(None):
            self.api_key_box.open()
        else: 
            self.refresh_player_info()
        

class MatchHistory(Screen): 
    pass

class Library(Screen):
    '''Page with user's saved runes.'''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # # Initializing Layouts
        menu_items = [{'text': title,
                       'viewclass': 'CustomOneLineListItem',
                       'on_release': lambda x=title: self.drop_menu_button(x),
                       'height': dp(56),
                       'divider': None
                       } for title in ['Switch Profile', 'Rename profile', 'Delete profile']
                      ]
        self.drop_menu = MDDropdownMenu(items=menu_items,
                                        width_mult=2.7)

        rune_menu_items = [{'text': title[0],
                            'viewclass': 'CustomIconListItem',
                            'on_release': lambda x=title[0]: self.select_drop_menu_option(x),
                            'height': dp(45),
                            'icon': title[1]
                            } for title in [['edit', 'pencil'], ['delete', 'trash-can']]
                          ]
        self.rune_drop_menu = MDDropdownMenu(items=rune_menu_items,
                                             width_mult=2.6)

        for rune in saved_runes.runes:
            self.ids.my_runes.add_widget(rune)

    def select_drop_menu_option(self, title):
        '''Called by 'dots-vertical' icon that appears on-hover for a rune'''
        rune = self.rune_drop_menu.caller.rune
        self.rune_drop_menu.dismiss()
        if title == 'edit': 
            self.edit_rune(rune)
        else:
            self.delete_rune(rune)

    '''TODO: Implement search bar'''
    def make_rune_list(self, text='', search=False):
        '''Searching for a rune'''
        def add_rune(row):

            self.ids.my_runes.data.append(
                {
                    'viewclass': 'Rune',
                    'row': row
                }
            )
        
        self.ids.my_runes.data = []
        for rune in saved_runes.to_array():
            if search:
                if text in rune[1]:
                    add_rune(rune)
            else:
                add_rune(rune)

    def profile_name(self): 
        return profile.name

    def drop_menu_button(self, title):
        ''' Displays menu to delete or rename account'''
        self.profile_box = None
        if title == 'Delete profile':
            buttons = [MDFlatButton(text='No', on_release=lambda x: self.profile_box.dismiss()),
                       MDFlatButton(text='Yes', on_release=lambda x: self.delete_profile())]
            self.profile_box = MDDialog(text=f'Are you sure you want to delete \'{profile.name}\'?',
                                        buttons=buttons,
                                        padding=5)
            self.profile_box.open()
        elif title == 'Rename profile':
            self.profile_box = MDDialog(title='Profile name:',
                                           type='custom',
                                           content_cls=MDTextField(text=profile.name),
                                           buttons=[MDFlatButton(text='Rename',
                                                                 on_release=self.rename_profile)])
            self.profile_box.open()

        else:
            self.open_dialog_box()

        self.drop_menu.dismiss()

    def rename_profile(self, event):
        name = self.profile_box.content_cls.text

        if not profile.rename(name):
            #Rename unsuccessful
            Snackbar(text='A profile already exists with that name', duration=1).open()
            return

        self.ids.account_btn.text = self.profile_name()
        self.profile_box.dismiss()

    def delete_profile(self):
        if profile.delete():
            #Deletion successful
            saved_runes.change_account(profile.data())

            self.ids.my_runes.clear_widgets()

            for rune in saved_runes.runes:
                self.ids.my_runes.add_widget(rune)

        self.ids.account_btn.text = self.profile_name()
        sm.remove_widget(sm.get_screen('profile'))
        sm.add_widget(PlayerProfile(name='profile'))
        self.profile_box.dismiss()

    def view_rune(self, rune):
        self.rune = rune
        sm.add_widget(ViewRune(name='view_page'))
        sm.current = 'view_page'

    def champ_select(self):
        '''Goes to champ select page'''
        if not sm.has_screen('champ_select'):
            sm.add_widget(ChampSelect(name='champ_select'))

        sm.current = 'champ_select'

    def delete_rune(self, rune):
        saved_runes.delete_rune(rune)
        self.ids.my_runes.remove_widget(rune)

    def open_dialog_box(self):
        '''Opens the box for switching accounts'''
        items = []
        for account in profile.profiles():
            item = CustomIconListItem(text=account.strip('.csv'), 
                                      icon='account-circle')

            item.bind(on_release=partial(self.switch_profile, account.strip('.csv')))
            items.append(item)

        add_account_item = CustomIconListItem(text='Add Profile', 
                                              icon='account-plus')
        add_account_item.bind(on_release=self.get_profile_name)
        items.append(add_account_item)

        self.dialog_box = MDDialog(title='Choose Profile:',
                                   type='simple',
                                   items=items)
        self.dialog_box.open()

    def switch_profile(self, account, event):
        if account == profile.name:
            self.dialog_box.dismiss()
            return
        profile.save(saved_runes.to_array())
        profile.set_current(account)
        saved_runes.change_account(profile.data())

        self.ids.my_runes.clear_widgets()

        for rune in saved_runes.runes:
            self.ids.my_runes.add_widget(rune)

        self.ids.account_btn.text = self.profile_name()
        sm.remove_widget(sm.get_screen('profile'))
        sm.add_widget(PlayerProfile(name='profile'))

        try:
            self.dialog_box.dismiss()
        except AttributeError:
            return

    def get_profile_name(self, event):
        if len(profile.profiles()) >= 4:
            Snackbar(text='Max Accounts Reached',
                     duration=1).open()
            return
        self.create_account_box = MDDialog(title='Profile name:',
                                           type='custom',
                                           content_cls=MDTextField(),
                                           buttons=[MDFlatButton(text='Create', on_release=self.create_profile)])
        self.create_account_box.open()

    def create_profile(self, event):
        file_name = self.create_account_box.content_cls.text
        if not profile.add_new(file_name):
            Snackbar(text=f'\'{file_name}\' already exists', duration=1).open()
            return
        #Profile already switches when add_new is called.
        self.switch_profile(file_name, None)
        Snackbar(text='Profile Successfully created!', duration=1).open()

        self.create_account_box.dismiss()
        self.dialog_box.dismiss()

    def edit_rune(self, rune):
        screen = sm.get_screen('rune_page')
        screen.ids.primary.preset(rune.attributes()[:5])
        screen.ids.secondary.preset(rune.attributes()[5:])

        screen.champion = rune.champ
        screen.title = rune.name
        screen.rune = rune
        screen.edit = True
        screen.previous = self.name
        sm.current = 'rune_page'

class ViewRune(Screen):
    '''Page to view rune attributes for each saved rune.'''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rune = sm.get_screen('library').rune
        
        toolbar = self.ids.toolbar
        toolbar.title = self.rune.name
        toolbar.right_action_items = [[f'icons/champ_icons/{self.rune.champ}.png']]

        for attribute in self.rune.attributes():
            rune_card = RuneCard(source=f'icons/runes/{attribute}.png', txt=attribute.title())
            self.ids.rune_grid.add_widget(rune_card)

    def go_back(self, event=None):
        sm.remove_widget(self)
        sm.current = 'library'

    #Edit the chosen rune
    def edit_rune(self):
        screen = sm.get_screen('rune_page')
        screen.ids.toolbar.title = self.rune.name
        screen.ids.toolbar.right_action_items = [[f'icons/champ_icons/{self.rune.champ}.png']]

        for i, attr in enumerate(self.rune.attributes()):
            if i < 5:
                screen.panel_manager.primary_panels[i].change_title(attr)
            else:
                screen.panel_manager.secondary_panels[i-5].change_title(attr)

        screen.previous = self.name
        sm.current = 'rune_page'

    def view_attribute(self, attribute, event=None):
        if attribute in titles.keys():
            return

        screen = InfoPage(attribute, name='rune_info')
        sm.add_widget(screen)
        sm.current = 'rune_info'

class InfoPage(Screen):
    '''Page to view rune effects.'''
    def __init__(self, attr, **kwargs):
        super().__init__(**kwargs)

        self.attribute = attr

        text = ""
        with open(f'rune_files/{self.attribute}.txt', 'r') as file:
            for line in file.readlines():
                text += line.strip()
                text += '\n'
        
        self.ids.rune_img.source = f'icons/runes/{self.attribute}.png'
        self.ids.attr_title.text = self.attribute.title()
        self.ids.attr_description.text = text

    def go_back(self):
        sm.current = 'view_page'
        sm.remove_widget(self)

class ChampSelect(Screen):
    '''Page to choose a champion.'''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Initializing Champion Cards
        with open('resources/champions.txt', 'r') as file:
            for champ in file.readlines():
                champ = champ.strip('\n')
                source = f'icons/champ_images/{champ}.png'

                self.ids.champ_grid.add_widget(Card(source=source, 
                                                    text=champ.title()))

    #Build a rune for the champion chosen
    def build_rune(self, champ):
        screen = sm.get_screen('rune_page')

        screen.title = champ.title()
        screen.champion = champ
        screen.previous = self.name

        sm.current = 'rune_page'

    def go_back(self):
        sm.current = 'library'

class BuildRune(Screen):
    title = StringProperty('Place Holder')
    previous = ObjectProperty(None)
    rune = ObjectProperty(None)
    champion = StringProperty(None)
    edit = BooleanProperty(False)
    
    def go_back(self, event):
        sm.current = self.previous
        
    def on_leave(self, *args):
        self.edit = False
        self.ids.primary.reset()
        self.ids.secondary.reset()

    def save_rune(self, event):
        '''Saves the Rune'''
        try:
            rune_info = [self.champion.lower(), self.dialog_btn.content_cls.text]
            primary_attrs = self.ids.primary.drawer_titles()
            secondary_attrs = self.ids.secondary.drawer_titles()
            rune_info+=primary_attrs+secondary_attrs

        
            if not self.edit:
                rune = Rune(row=rune_info)
                saved_runes.add_new_rune(rune)
                sm.get_screen('library').ids.my_runes.add_widget(rune)
            else:
                self.rune.edit(rune_info)
        except (ValueError, AttributeError): 
            Snackbar(text='Rune Incomplete', duration=1).open()
            return

        self.close_box()
        Snackbar(text='Rune Saved Successfully!', duration=1).open()
        sm.current = 'library'

    def show_save_box(self):
        save_btn = MDFlatButton(text='SAVE', on_release=self.save_rune)
        back_btn = MDFlatButton(text='CANCEL', on_release=self.close_box)

        self.dialog_btn = MDDialog(title='Rune Name:',
                                   type='custom',
                                   content_cls=MDTextField(text=self.ids.toolbar.title),
                                   buttons=[back_btn, save_btn])
        self.dialog_btn.open()

    def close_box(self, event=None):
        self.dialog_btn.dismiss()

if __name__ == '__main__':
    @atexit.register
    def save():
        profile.save(saved_runes.to_array())

    RuneSaver().run()