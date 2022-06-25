import kivymd
from kivy.properties import Clock
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from Widgets import *
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, ScreenManagerException
from kivy.core.window import Window
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFloatingActionButton, MDFlatButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.toolbar import MDToolbar
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.stacklayout import MDStackLayout
from functools import partial
from kivymd.uix.list import MDList
from kivymd.uix.dialog import MDDialog
import atexit
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from kivymd.uix.tab import MDTabs
from Profile import Profile
from kivy.properties import ObjectProperty

profile = Profile()

class RuneSaver(MDApp):
    '''App manager.'''
    def build(self):
        # Red, Pink, Purple, DeepPurple, Indigo, Blue, LightBlue, Cyan, Teal, Green, LightGreen, Lime,
        # Yellow, Amber, Orange, DeepOrange, Brown, Gray, BlueGray
        global sm, saved_runes

        saved_runes = SavedRunes(profile.data())

        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        sm = ScreenManager(transition=FadeTransition())

        return sm

    def on_start(self):
        sm.add_widget(Library(name='library'))
        sm.add_widget(ChampSelect(name='champ_select'))
        sm.add_widget(BuildRune('rune_page'))

        sm.current = 'library'

class SplashScreen(Screen):
    '''Displays on app launch.'''
    def __init__(self, page_name):
        super().__init__(name=page_name)
        self.box = MDBoxLayout(orientation='vertical',
                               padding=50)

        self.img = Image(source='icons/splash-icon.png',
                         size_hint_x=None,
                         pos_hint={'center_x': .5})
        self.label = MDLabel(text='Rune Saver For League Of Legends',
                             halign='center')

        self.box.add_widget(self.img)
        self.box.add_widget((self.label))

        self.add_widget(self.box)

class Library(Screen):
    '''Page with user's saved runes.'''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # # Initializing Layouts
        menu_items = [{'text': title,
                       'viewclass': 'OneLineListItem',
                       'on_release': lambda x=title: self.drop_menu_button(x),
                       'height': dp(56)
                       } for title in ['Rename profile', 'Delete profile']
                      ]
        self.drop_menu = MDDropdownMenu(items=menu_items,
                                        width_mult=2.7)

        # Adding widgets to layouts
        for rune in saved_runes.runes:
            rune.bind_back(on_release=partial(self.delete_rune, rune))
            rune.bind_front(on_release=partial(self.view_rune, rune))

            self.ids.my_runes.add_widget(rune)

    def profile_name(self): 
        return profile.name

    def open_menu(self, button):
        self.drop_menu.caller = button
        self.drop_menu.open()

    def drop_menu_button(self, text_item):
        ''' Displays menu to delete or rename account'''
        self.profile_box = None
        if text_item == 'Delete profile':
            buttons = [MDFlatButton(text='No', on_release=lambda x: self.profile_box.dismiss()),
                       MDFlatButton(text='Yes', on_release=lambda x: self.delete_profile())]
            self.profile_box = MDDialog(text=f'Are you sure you want to delete \'{profile.name}\'?',
                                        buttons=buttons,
                                        padding=5)
            self.profile_box.open()
        else:
            self.profile_box = MDDialog(title='Profile name:',
                                           type='custom',
                                           content_cls=MDTextField(text=profile.name),
                                           buttons=[MDFlatButton(text='Rename',
                                                                 on_release=self.rename_profile)])
            self.profile_box.open()

        self.drop_menu.dismiss()

    def rename_profile(self, event):
        name = self.profile_box.content_cls.text

        if not profile.rename(name):
            Snackbar(text='Profile already exists with that name', duration=1).open()
            return

        self.toolbar.title = profile.name
        self.profile_box.dismiss()

    def delete_profile(self):
        if profile.delete():
            saved_runes.change_account(profile.data())

            self.my_runes.clear_widgets()

            for rune in saved_runes.runes:
                rune.bind_back(on_release=partial(self.delete_rune, rune))
                rune.bind_front(on_release=partial(self.view_rune, rune))

                self.my_runes.add_widget(rune)

        self.toolbar.title = profile.name
        self.profile_box.dismiss()

    def view_rune(self, rune, event):
        if rune.img.pos[0] == 16:
            self.rune = rune
            sm.add_widget(ViewRune(name='view_page'))
            sm.current = 'view_page'

    def champ_select(self):
        try: 
            sm.current = 'champ_select'
        except ScreenManagerException:
            sm.add_widget(ChampSelect('champ_select'))
            print(sm.get_screen('champ_select'))

    def delete_rune(self, rune, event):
        saved_runes.delete_rune(rune)
        self.my_runes.remove_widget(rune)

    def open_dialog_box(self, event):
        items = []
        for account in profile.profiles():
            item = IconListItem(account.strip('.csv'), 'account-circle')
            item.divider = None
            item.bind(on_release=partial(self.switch_profile, account.strip('.csv')))
            items.append(item)

        add_account_item = IconListItem('Add Profile', 'account-plus')
        add_account_item.divider = None
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

        self.my_runes.clear_widgets()

        for rune in saved_runes.runes:
            rune.bind_back(on_release=partial(self.delete_rune, rune))
            rune.bind_front(on_release=partial(self.view_rune, rune))

            self.my_runes.add_widget(rune)

        self.toolbar.title = profile.name
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

class ViewRune(Screen):
    '''Page to view rune attributes for each saved rune.'''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rune = sm.get_screen('library').rune
        
        toolbar = self.ids.toolbar
        toolbar.title = self.rune.name
        toolbar.right_action_items = [[f'icons/champ_icons/{self.rune.champ}.png']]

        self.ids.edit_btn.on_release = self.edit_rune

        for attribute in self.rune.attributes():
            rune_card = RuneCard(f'icons/runes/{attribute}.png', attribute.title())
            rune_card.bind(on_release=partial(self.view_rune_attribute, attribute))
            self.ids.rune_grid.add_widget(rune_card)

    def go_back(self, event=None):
        sm.remove_widget(self)
        sm.current = 'library'

    #Edit the chosen rune
    def edit_rune(self, event=None):
        screen = sm.get_screen('rune_page')
        screen.toolbar.title = self.rune.name
        screen.toolbar.right_action_items = [[f'icons/champ_icons/{self.rune.champ}.png']]

        for i, attr in enumerate(self.rune.attributes()):
            if i < 5:
                screen.panel_manager.primary_panels[i].change_title(attr)
            else:
                screen.panel_manager.secondary_panels[i-5].change_title(attr)

        screen.previous = self.name
        sm.current = 'rune_page'

    def view_rune_attribute(self, rune_attribute, event):
        if rune_attribute in titles.keys():
            return

        screen = InfoPage(rune_attribute, name='rune_info')
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
                card = Card(source, champ.title())
                card.bind(on_release=partial(self.build_rune, champ))

                self.ids.champ_grid.add_widget(card)

    #Build a rune for the champion chosen
    def build_rune(self, champ, event):
        screen = sm.get_screen('rune_page')

        screen.champion = champ
        screen.ids.toolbar.title = champ.title()
        screen.ids.toolbar.right_action_items = [[f'icons/champ_icons/{champ}.png']]
        screen.previous = self.name

        sm.current = 'rune_page'

    def go_back(self, event):
        sm.current = 'library'

class BuildRune(Screen):
    '''Page to build a rune.'''
    def __init__(self, page_name):
        super().__init__(name=page_name)
        self.previous = None
        self.champion = None

        # Initializing Layouts
        # self.tab_manager = MDTabs()
        # self.box = MDBoxLayout(orientation='vertical')
        # self.root = ScrollView()
        # self.anchor_layout = AnchorLayout(anchor_x='right',
        #                                   anchor_y='bottom',
        #                                   padding=30)
        # self.grid = MDGridLayout(cols=1,
        #                          padding=[10, 0],
        #                          size_hint_y=None)
        # self.grid.bind(minimum_height=self.grid.setter('height'))

        # #Initializing widgets
        # self.ids.toolbar = MDToolbar(title="Holder Text")
        # self.toolbar.left_action_items = [['arrow-left', self.go_back]]

        self.panel_manager = PanelManager(['Primary', 'Keystone', 'Slot 1', 'Slot 2', 'Slot 3'],
                                          ['Secondary', 'Slot 1', 'Slot 2'])
        for panel in self.panel_manager.primary_panels:
            self.ids.panel_grid.add_widget(panel)
        for panel in self.panel_manager.secondary_panels:
            self.ids.panel_grid.add_widget(panel)

        # self.save_btn = FloatingButton(icon='check', tooltip_text='Done')
        # self.save_btn.bind(on_release=self.show_save_box)

        # self.rune_tab = Tab(title='Rune')
        # self.build_tab = Tab(title='Build')

        # #Adding widgets to layout
        # self.root.add_widget(self.grid)
        # self.rune_tab.add_widget(self.root)

        # self.tab_manager.add_widget(self.rune_tab)
        # self.tab_manager.add_widget(self.build_tab)

        # self.box.add_widget(self.toolbar)
        # self.box.add_widget(self.tab_manager)
        # self.anchor_layout.add_widget(self.save_btn)

        # #Adding layouts to screen
        # self.add_widget(self.box)
        # self.add_widget(self.anchor_layout)

    def go_back(self, event):
        sm.current = self.previous
        if self.previous == 'view_page':
            self.panel_manager.reset_panels()

    #Displays the dialog box
    def show_save_box(self):
        save_btn = MDFlatButton(text='SAVE', on_release=self.save_rune)
        back_btn = MDFlatButton(text='CANCEL', on_release=self.close_box)

        self.dialog_btn = MDDialog(title='Rune Name:',
                                   type='custom',
                                   content_cls=MDTextField(text=self.ids.toolbar.title),
                                   buttons=[back_btn, save_btn])
        self.dialog_btn.open()

    #Saves the rune
    def save_rune(self, event=None):
        '''Saves the rune'''
        try:#If the viewpage exists (Rune needs to be edited)
            rune_screen = sm.get_screen('view_page')
            rune = rune_screen.rune
            rune_info = [rune.champ, self.dialog_btn.content_cls.text]

            for panel in self.panel_manager.primary_panels:
                rune_info.append(panel.text().lower())

            for panel in self.panel_manager.secondary_panels:
                rune_info.append(panel.text().lower())

            rune.edit(rune_info)

            screen = sm.get_screen('library')
            screen.my_runes.remove_widget(rune)
            screen.my_runes.add_widget(rune, len(screen.my_runes.children)-saved_runes.rune_index(rune))

            sm.remove_widget(rune_screen)

        except ScreenManagerException: #If the viewpage doesn't exist (Rune must be added)
            rune_info = [self.champion, self.dialog_btn.content_cls.text]

            for panel in self.panel_manager.primary_panels:
                rune_info.append(panel.text().lower())

            for panel in self.panel_manager.secondary_panels:
                rune_info.append(panel.text().lower())

            screen = sm.get_screen('library')

            rune = Rune(rune_info)
            rune.bind_front(on_release=partial(screen.view_rune, rune))
            rune.bind_back(on_release=partial(screen.delete_rune, rune))

            saved_runes.add_new_rune(rune)
            screen.my_runes.add_widget(rune, saved_runes.rune_index(rune))

        self.close_box()

        Snackbar(text='Rune Saved Successfully!', duration=1).open()
        sm.current = 'library'

    #Closes the dialog box
    def close_box(self, event=None):
        self.dialog_btn.dismiss()

if __name__ == '__main__':
    @atexit.register
    def save():
        profile.save(saved_runes.to_array())

    RuneSaver().run()




