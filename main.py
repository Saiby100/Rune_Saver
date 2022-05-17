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
import csv
from kivymd.uix.dialog import MDDialog
import atexit
import os
from kivymd.uix.snackbar import Snackbar

# Window.size = (300, 500)

accounts = os.listdir('accounts')

with open('Resources/config.txt', 'r') as file:
    current = file.readline()

class RuneSaver(MDApp):
    def build(self):
        # Red, Pink, Purple, DeepPurple, Indigo, Blue, LightBlue, Cyan, Teal, Green, LightGreen, Lime,
        # Yellow, Amber, Orange, DeepOrange, Brown, Gray, BlueGray
        global sm, file_runes

        file_runes = SavedRunes(current)

        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(Library('library'))
        sm.add_widget(ChampSelect('champ_select'))
        sm.add_widget(BuildRune('rune_page'))

        return sm

#Page with user's saved runes
class Library(Screen):
    # use list object to save runes
    def __init__(self, page_name):
        super().__init__(name=page_name)
        # Initializing Layouts
        self.box = MDBoxLayout(orientation='vertical')
        self.anchor_layout = AnchorLayout(anchor_x='right',
                                          anchor_y='bottom',
                                          padding=30)
        self.root = ScrollView()

        # Initializing Widgets
        self.toolbar = MDToolbar(title=f'{current}\'s Runes')
        self.toolbar.right_action_items = [['account', self.change_account]]
        self.add_btn = FloatingButton(icon='plus',
                                      tooltip_text='Add New Rune')
        self.add_btn.bind(on_release=self.champ_select)

        self.my_runes = MDList(padding=[10, 0])

        # Adding widgets to layouts
        for rune in file_runes.runes:
            rune.back_layer.children[0].bind(on_release=partial(self.delete_rune, rune))
            rune.front_layer.bind(on_release=partial(self.view_rune, rune))

            self.my_runes.add_widget(rune)

        self.root.add_widget(self.my_runes)
        self.box.add_widget(self.toolbar)
        self.box.add_widget(self.root)
        self.anchor_layout.add_widget(self.add_btn)

        # Adding Layouts to Screen
        self.add_widget(self.box)
        self.add_widget(self.anchor_layout)

    def view_rune(self, rune, event):
        if rune.list_item.icon.pos[0] == 16:
            self.rune = rune
            sm.add_widget(ViewRune('view_page'))
            sm.current = 'view_page'

    def champ_select(self, event):
        sm.current = 'champ_select'

    def delete_rune(self, rune, event):
        file_runes.delete_rune(rune)
        self.my_runes.remove_widget(rune)

    def change_account(self, event):
        items = []
        for account in accounts:
            item = ListItem(account.strip('.csv'), 'icons/user.png')
            item.divider = None
            item.bind(on_release=partial(self.switch, account.strip('.csv')))
            items.append(item)

        add_account_item = ListItem('Add account', 'icons/plus.png')
        add_account_item.divider = None
        add_account_item.bind(on_release=self.new_account)
        items.append(add_account_item)

        self.dialog_box = MDDialog(title='Choose Profile:',
                                   type='simple',
                                   items=items)

        self.dialog_box.open()

    def switch(self, account, event):
        global current
        if account == current:
            self.dialog_box.dismiss()
            return

        save()
        current = account
        with open('Resources/config.txt', 'w') as file:
            file.write(account)

        file_runes.change_account(account)
        self.my_runes.clear_widgets()
        self.root.clear_widgets()

        for rune in file_runes.runes:
            rune.back_layer.children[0].bind(on_release=partial(self.delete_rune, rune))
            rune.front_layer.bind(on_release=partial(self.view_rune, rune))

            self.my_runes.add_widget(rune)

        self.root.add_widget(self.my_runes)
        self.toolbar.title =f'{current}\'s Runes'

        self.dialog_box.dismiss()

    def new_account(self, event):
        if len(accounts) >= 4:
            Snackbar(text='Max Accounts Reached',
                     duration=1).open()
            return
        self.create_account_box = MDDialog(title='Profile name:',
                                           type='custom',
                                           content_cls=MDTextField(),
                                           buttons=[MDFlatButton(text='Create', on_release=self.create_account)])
        self.create_account_box.open()

    def create_account(self, event):
        try:
            global accounts
            file_name = self.create_account_box.content_cls.text
            open(f'accounts/{file_name}.csv', 'x')

            self.dialog_box.dismiss()
            self.create_account_box.dismiss()

            accounts = os.listdir('accounts')
            self.switch(file_name, None)
            Snackbar(text='Profile Successfully created!', duration=1).open()

        except (FileExistsError):
            Snackbar(text='Profile already exists', duration=1).open()

#Page to view rune attributes for each saved rune
class ViewRune(Screen):
    def __init__(self, page_name):
        super().__init__(name=page_name)
        self.rune = sm.get_screen('library').rune

        # Initializing Layouts
        self.anchor_layout = AnchorLayout(anchor_x='right',
                                          anchor_y='bottom',
                                          padding=30)
        self.box = BoxLayout(orientation='vertical')
        self.grid = MDGridLayout(cols=2,
                                 spacing=5,
                                 padding=10)

        # Initializing Widgets
        self.toolbar = MDToolbar(title=self.rune.name)
        self.toolbar.right_action_items = [[f'icons/{self.rune.champ}.png']]
        self.toolbar.left_action_items = [['arrow-left', self.go_back]]
        self.edit_btn = MDFloatingActionButton(icon='pencil')
        self.edit_btn.bind(on_release=partial(self.edit_rune, self.rune))

        for attribute in self.rune.attributes():
            rune_card = RuneCard(f'Runes/{attribute}.png', attribute.title())
            rune_card.bind(on_release=partial(self.view_rune_attribute, attribute))
            self.grid.add_widget(rune_card)

        # Adding Widgets to Layouts
        self.anchor_layout.add_widget(self.edit_btn)
        self.box.add_widget(self.toolbar)
        self.box.add_widget(self.grid)

        # Adding Layout to Screen
        self.add_widget(self.box)
        self.add_widget(self.anchor_layout)

    def go_back(self, event):
        sm.remove_widget(self)
        sm.current = 'library'

    #Edit the chosen rune
    def edit_rune(self, rune, event):
        self.rune = rune
        screen = sm.get_screen('rune_page')
        screen.toolbar.title = rune.name
        screen.toolbar.right_action_items = [[f'icons/{rune.champ}.png']]

        array = rune.attributes()
        array.reverse()

        screen.set_up_panels(array)
        screen.previous = self.name
        sm.current = 'rune_page'

    def view_rune_attribute(self, rune_attribute, event):
        if (titles.keys().__contains__(rune_attribute)):
            return
        sm.add_widget(InfoPage(rune_attribute, 'rune_info'))
        sm.current = 'rune_info'

#Page to view rune effects
class InfoPage(Screen):
    def __init__(self, attribute, page_name):
        super().__init__(name=page_name)

        self.attribute = attribute

        #Initializing Layouts
        self.box = MDBoxLayout(orientation='vertical',
                               padding=10)
        self.box2 = MDBoxLayout(orientation='vertical',
                                pos_hint={'top': 1},
                                padding=[20, 15],
                                adaptive_height=True,
                                spacing=20)
        self.anchor_layout = AnchorLayout(anchor_x='left',
                                          anchor_y='top',
                                          padding=15)
        self.anchor_layout2 = AnchorLayout(anchor_x='center',
                                           anchor_y='center',
                                           padding=15)
        text = ""
        with open(f'rune_files/{self.attribute}.txt', 'r') as file:
            for line in file.readlines():
                text += line

        #Intializing and adding widgets to layouts
        self.card = MDCard(orientation='vertical',
                           padding='10dp',
                           radius='25dp')
        self.box2.add_widget(Image(source=f'Runes/{self.attribute}.png',
                                   size_hint_y=None,
                                   height=50))
        self.box2.add_widget(MDLabel(text=self.attribute.title(),
                                     halign='center',
                                     font_style='H6'))
        self.anchor_layout2.add_widget(MDLabel(text=text,
                                               halign='left',
                                               font_style='Subtitle2'))

        self.box.add_widget(self.card)
        self.anchor_layout.add_widget(FloatingButton(icon='arrow-left',
                                                     on_release=self.go_back))

        #Adding layouts to screen
        self.add_widget(self.box)
        self.add_widget(self.anchor_layout)
        self.add_widget(self.box2)
        self.add_widget(self.anchor_layout2)

    def go_back(self, event):
        sm.current = 'view_page'
        sm.remove_widget(self)

#Page to choose a champion
class ChampSelect(Screen):
    def __init__(self, page_name):
        super().__init__(name=page_name)

        # Initializing Layouts
        self.box = BoxLayout(orientation='vertical',
                             pos_hint={'top': 1})
        self.root = ScrollView()
        self.champ_grid = MDStackLayout(size_hint_y=None,
                                        spacing=10,
                                        padding=5)
        self.champ_grid.bind(minimum_height=self.champ_grid.setter('height'))

        # Initializing Champion Cards
        with open('Resources/champions.txt', 'r') as file:
            for champ in file.readlines():
                champ = champ.strip('\n')
                source = 'images/{}.png'.format(champ)
                card = Card(source, champ.title())
                card.bind(on_release=partial(self.build_rune, champ))

                self.champ_grid.add_widget(card)

        # Initializing Widgets
        self.toolbar = MDToolbar(title='Select Champion')
        self.toolbar.left_action_items = [['arrow-left', self.go_back]]

        # Adding Widgets to Layouts
        self.root.add_widget(self.champ_grid)
        self.box.add_widget(self.toolbar)
        self.box.add_widget(self.root)

        # Adding Layouts to Screen
        self.add_widget(self.box)

    #Build a rune for the champion chosen
    def build_rune(self, champ, event):
        screen = sm.get_screen('rune_page')

        screen.champion = champ
        screen.toolbar.title = champ.title()
        screen.toolbar.right_action_items = [[f'icons/{champ}.png']]
        screen.previous = self.name
        # screen.set_up_panels()

        sm.current = 'rune_page'

    def go_back(self, event):
        sm.current = 'library'

#Page to build a rune
class BuildRune(Screen):
    def __init__(self, page_name):
        super().__init__(name=page_name)
        self.previous = None
        self.champion = None

        # Initializing Layouts
        self.box = MDBoxLayout(orientation='vertical')
        self.root = ScrollView()
        self.anchor_layout = AnchorLayout(anchor_x='right',
                                          anchor_y='bottom',
                                          padding=30)
        self.grid = MDGridLayout(cols=1,
                                 padding=[10, 0],
                                 size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))

        #Initializing widgets
        self.toolbar = MDToolbar(title="Holder Text")
        self.toolbar.left_action_items = [['arrow-left', self.go_back]]

        for i in range(8):
            self.grid.add_widget(ExpansionPanel('Holder Text'))
        self.set_up_panels()

        self.save_btn = FloatingButton(icon='check', tooltip_text='Done')
        self.save_btn.bind(on_release=self.show_save_box)

        #Adding widgets to layout
        self.root.add_widget(self.grid)
        self.box.add_widget(self.toolbar)
        self.box.add_widget(self.root)
        self.anchor_layout.add_widget(self.save_btn)

        #Adding layouts to screen
        self.add_widget(self.box)
        self.add_widget(self.anchor_layout)

    def go_back(self, event):
        sm.current = self.previous
        if self.previous == 'view_page':
            self.set_up_panels()

    # Creates a content widget containing all the runes specified in the array
    def create_content(self, array):
        items = []
        for value in array:
            value = value.strip('\n')
            item = ListItem(value.title(), f'Runes/{value}.png')
            item.bind(on_release=partial(self.update_panel, item, value))
            items.append(item)

        return Content(items)

    # All contents of the expansion panels below it must change
    def update_panel(self, item, text, event):
        main = []
        main.extend(runes.keys())
        if main.__contains__(text):
            panel_titles = []
            panel_titles.extend(runes[text].keys())
            if item.parent.parent == self.grid.children[7]:
                rune = [None, None, text, panel_titles[3], panel_titles[2], panel_titles[1], panel_titles[0], text]
                self.set_up_panels(rune, True, False)
            else:
                rune = ['slot 2', 'slot 1', text, None, None, None, None, text]
                self.set_up_panels(rune, False, True)

        item.parent.parent.panel_cls.text = text.title()

    #Displays the dialog box
    def show_save_box(self, event):
        save_btn = MDFlatButton(text='SAVE', on_release=self.save_rune)
        back_btn = MDFlatButton(text='CANCEL', on_release=self.close_box)

        self.dialog_btn = MDDialog(title='Rune Name:',
                                   type='custom',
                                   content_cls=MDTextField(text=self.toolbar.title),
                                   buttons=[back_btn, save_btn])
        self.dialog_btn.open()

    #Saves the rune
    def save_rune(self, event=None):
        try:
            rune_screen = sm.get_screen('view_page')
            rune = rune_screen.rune
            rune_info = [rune.champ, self.dialog_btn.content_cls.text]

            for i in range(len(self.grid.children) - 1, -1, -1):
                rune_info.append(self.grid.children[i].panel_cls.text.lower())

            screen = sm.get_screen('library')
            rune.edit(rune_info)

            screen.my_runes.children[screen.my_runes.children.index(rune)] = rune

            self.close_box()
            sm.remove_widget(rune_screen)
            sm.current = 'library'
            return

        except ScreenManagerException:
            rune_info = [self.champion, self.dialog_btn.content_cls.text]

        for i in range(len(self.grid.children) - 1, -1, -1):
            rune_info.append(self.grid.children[i].panel_cls.text.lower())

        screen = sm.get_screen('library')
        screen.my_runes.clear_widgets()

        rune = Rune(rune_info)
        rune.back_layer.children[0].bind(on_release=partial(screen.delete_rune, rune))
        rune.front_layer.bind(on_release=partial(screen.view_rune, rune))
        file_runes.add_new_rune(rune)

        for r in file_runes.runes:
            screen.my_runes.add_widget(r)

        self.close_box()

        Snackbar(text='Rune Saved Successfully!', duration=1).open()
        sm.current = 'library'

    #Creates titles and panel contents for expansion panels
    def set_up_panels(self, rune=None, primary_panels=True, secondary_panels=True):
        rune_name = []
        rune_name.extend(runes.keys())

        if rune is None:
            rune = ['slot 2', 'slot 1', 'secondary', 'slot 3', 'slot 2', 'slot 1', 'keystones', 'primary']
            main = titles['domination']
            main.append('domination')
            secondary = secondary_runes['sorcery']

        else:
            main = titles[rune[7]][0:4]
            main.reverse()
            main.append(rune[7])
            secondary = secondary_runes[rune[2]]

        for i in range(len(rune)):
            if i <= 1 and secondary_panels:
                # Secondary panels
                self.grid.children[i].panel_cls.text = rune[i].title()
                self.grid.children[i].content = self.create_content(secondary)

            elif i == 7 and primary_panels:
                self.grid.children[i].panel_cls.text = rune[i].title()
                self.grid.children[i].content = self.create_content(rune_name)

            elif i == 2 and secondary_panels:
                self.grid.children[i].panel_cls.text = rune[i].title()
                self.grid.children[i].content = self.create_content(rune_name)

            elif i >= 3 and i < 7 and primary_panels:
                # Primary panels
                self.grid.children[i].content = self.create_content(runes[main[4]][main[i - 3]])
                self.grid.children[i].panel_cls.text = rune[i].title()

    #Closes the dialog box
    def close_box(self, event=None):
        self.dialog_btn.dismiss()

if __name__ == '__main__':
    @atexit.register
    def save():
        with open(f'accounts/{current}.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(file_runes.to_array())

    RuneSaver().run()


