from Widgets import *
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
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

# Window.size = (300, 500)

titles = {'domination': ['Keystones', 'Malice', 'Tracking', 'Hunter'],
          'precision': ['Keystones', 'Heroism', 'Legend', 'Combat'],
          'inspiration': ['Keystones', 'Contraptions', 'Tomorrow', 'Beyond'],
          'resolve': ['Keystones', 'Strength', 'Resistance', 'Vitality'],
          'sorcery': ['Keystones', 'Artifact', 'Excellence', 'Power']
          }

runes = {'domination': {'Keystones': ['electrocute', 'predator', 'dark-harvest', 'hail-of-blades'],
                        'Malice': ['cheap-shot', 'taste-of-blood', 'sudden-impact'],
                        'Tracking': ['zombie-ward', 'ghost-poro', 'eyeball-collection'],
                        'Hunter': ['treasure-hunter', 'ingenious-hunter', 'relentless-hunter', 'ultimate-hunter']},

         'precision': {'Keystones': ['press-the-attack', 'lethal-tempo', 'fleet-footwork', 'conqueror'],
                       'Heroism': ['overheal', 'triumph', 'presence-of-mind'],
                       'Legend': ['legend-alacrity', 'legend-tenacity', 'legend-bloodline'],
                       'Combat': ['coup-de-grace', 'cut-down', 'last-stand']},

         'inspiration': {'Keystones': ['glacial-augment', 'unsealed-spellbook', 'first-strike'],
                         'Contraptions': ['hextech-flashtraption', 'magical-footwear', 'perfect-timing'],
                         'Tomorrow': ['future\'s-market', 'minion-dematerializer', 'biscuit-delivery'],
                         'Beyond': ['cosmic-insight', 'approach-velocity', 'time-warp-tonic']},

         'resolve': {'Keystones': ['grasp-of-the-undying', 'aftershock', 'guardian'],
                     'Strength': ['demolish', 'font-of-life', 'shield-bash'],
                     'Resistance': ['conditioning', 'second-wind', 'bone-plating'],
                     'Vitality': ['overgrowth', 'revitalize', 'unflinching']},

         'sorcery': {'Keystones': ['summon-aery', 'arcane-comet', 'phase-rush'],
                     'Artifact': ['nullifying-orb', 'manaflow-band', 'nimbus-cloak'],
                     'Excellence': ['transcendence', 'celerity', 'absolute-focus'],
                     'Power': ['scorch', 'waterwalking', 'gathering-storm']}
         }

secondary_runes = {'domination': ['cheap-shot', 'taste-of-blood', 'sudden-impact', 'zombie-ward', 'ghost-poro',
                                  'eyeball-collection', 'treasure-hunter', 'ingenious-hunter', 'relentless-hunter',
                                  'ultimate-hunter'],
                   'precision': ['overheal', 'triumph', 'presence-of-mind', 'legend-alacrity', 'legend-tenacity',
                                 'legend-bloodline', 'coup-de-grace', 'cut-down', 'last-stand'],
                   'inspiration': ['hextech-flashtraption', 'magical-footwear', 'perfect-timing', 'future\'s-market',
                                   'minion-dematerializer', 'biscuit-delivery', 'cosmic-insight', 'approach-velocity',
                                   'time-warp-tonic'],
                   'resolve': ['demolish', 'font-of-life', 'shield-bash', 'conditioning', 'second-wind',
                               'bone-plating', 'overgrowth', 'revitalize', 'unflinching'],
                   'sorcery': ['nullifying-orb', 'manaflow-band', 'nimbus-cloak', 'transcendence', 'celerity',
                               'absolute-focus', 'scorch', 'waterwalking', 'gathering-storm']
                   }


class RuneSaver(MDApp):
    def build(self):
        # Red, Pink, Purple, DeepPurple, Indigo, Blue, LightBlue, Cyan, Teal, Green, LightGreen, Lime, Yellow, Amber, Orange, DeepOrange, Brown, Gray, BlueGray
        global sm, file_runes

        with open('Resources/config.txt', 'r') as file:
            file_runes = SavedRunes(file.readline())

        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(Library('library'))
        sm.add_widget(ChampSelect('champ_select'))
        sm.add_widget(BuildRune('rune_page'))

        return sm


class Library(Screen):
    # use list object to save runes
    def __init__(self, page_name):
        super().__init__(name=page_name)
        # Initializing Layouts
        self.box = MDBoxLayout(orientation='vertical')
        self.anchor_layout = AnchorLayout(anchor_x='right',
                                          anchor_y='bottom',
                                          padding=30)
        self.root = ScrollView(size_hint=(1, None),
                               size=(Window.width, Window.height - 60))

        # Initializing Widgets
        self.toolbar = MDToolbar(title='My Runes')
        self.toolbar.right_action_items = [['account']]
        self.add_btn = FloatingButton(icon='plus',
                                      tooltip_text='Add New Rune')
        self.add_btn.bind(on_release=self.champ_select)

        self.my_runes = MDList(padding=[10, 0])

        # Adding widgets to layouts
        for rune in file_runes.runes:
            rune.back_layer.children[0].bind(on_release=partial(self.delete_rune, rune))
            rune.front_layer.bind(on_release=partial(self.view_rune, rune))

            self.my_runes.add_widget(rune)

        # self.root.add_widget(self.selection_list)
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


class SearchPage(Screen):
    def set_list_cards(self, text="", search=False):
        def add_card(card_name):
            self.rv.data.append({'viewclass'})


class ViewRune(Screen):
    def __init__(self, page_name):
        super().__init__(name=page_name)
        self.rune = sm.get_screen('library').rune

        # Initializing Layouts
        self.anchor_layout = AnchorLayout(anchor_x='right',
                                          anchor_y='bottom',
                                          padding=30)
        self.box = BoxLayout(orientation='vertical',
                             pos_hint={'top': 1})
        self.root = ScrollView(size_hint=(1, None),
                               size=(Window.width, Window.height - 64))
        self.grid = MDGridLayout(cols=2,
                                 size_hint_y=None,
                                 spacing=10,
                                 padding=10)
        self.grid.bind(minimum_height=self.grid.setter('height'))

        # Initializing Widgets
        self.toolbar = MDToolbar(title=self.rune.name)
        self.toolbar.right_action_items = [['icons/{}.png'.format(self.rune.champ)]]
        self.toolbar.left_action_items = [['arrow-left', self.go_back]]
        self.edit_btn = MDFloatingActionButton(icon='pencil')
        self.edit_btn.bind(on_release=partial(self.edit_rune, self.rune))

        for attribute in self.rune.attributes():
            self.grid.add_widget(RuneCard('Runes/{}.png'.format(attribute), attribute.title()))

        # Adding Widgets to Layouts
        self.anchor_layout.add_widget(self.edit_btn)
        self.root.add_widget(self.grid)
        self.box.add_widget(self.toolbar)
        self.box.add_widget(self.root)

        # Adding Layout to Screen
        self.add_widget(self.box)
        self.add_widget(self.anchor_layout)

    def go_back(self, event):
        sm.remove_widget(sm.get_screen('view_page'))
        sm.current = 'library'

    #Edit the chosen rune
    def edit_rune(self, rune, event):
        self.rune = rune
        screen = sm.get_screen('rune_page')
        screen.toolbar.title = rune.name.title()
        screen.toolbar.right_action_items = [['icons/{}.png'.format(rune.champ)]]
        screen.edit_mode = True

        array = rune.attributes()
        array.reverse()

        screen.set_up_panels(array)
        screen.previous = self.name
        sm.current = 'rune_page'


class ChampSelect(Screen):
    def __init__(self, page_name):
        super().__init__(name=page_name)

        # Initializing Layouts
        self.box = BoxLayout(orientation='vertical',
                             pos_hint={'top': 1})
        self.root = ScrollView(size_hint=(1, None),
                               size=(Window.width, Window.height - 64))
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
        self.champion = champ
        screen = sm.get_screen('rune_page')

        screen.toolbar.title = champ.title()
        screen.toolbar.right_action_items = [['icons/{}.png'.format(champ)]]
        screen.previous = self.name
        screen.set_up_panels()

        sm.current = 'rune_page'

    def go_back(self, event):
        sm.current = 'library'


class BuildRune(Screen):
    def __init__(self, page_name):
        super().__init__(name=page_name)
        self.previous = None

        # Initializing Layouts
        self.stack_layout = MDStackLayout(size_hint_y=None,
                                          pos_hint={'top': 1})
        self.stack_layout.size[1] = 64
        self.root = ScrollView(size_hint=(1, None),
                               size=(Window.width, Window.height - 64))
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
        self.stack_layout.add_widget(self.toolbar)
        self.anchor_layout.add_widget(self.save_btn)

        #Adding layouts to screen
        self.add_widget(self.root)
        self.add_widget(self.stack_layout)
        self.add_widget(self.anchor_layout)

    def go_back(self, event):
        sm.current = self.previous

    # Creates a content widget containing all the runes specified in the array
    def create_content(self, array):
        items = []
        for value in array:
            value = value.strip('\n')
            item = ListItem(value.title(), 'Runes/{}.png'.format(value))
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
        # item.parent.parent.close_panel(item.parent.parent, False)

    #Displays the dialog box
    def show_save_box(self, event):
        save_btn = MDFlatButton(text='SAVE', on_release=self.save)
        back_btn = FlatButton(text='CANCEL', on_release=self.close_box)

        self.dialog_btn = MDDialog(title='Rune Name:',
                                   type='custom',
                                   content_cls=MDTextField(),
                                   buttons=[back_btn, save_btn])
        self.dialog_btn.open()

    #Saves the rune
    def save(self, event=None):
        try:
            rune_info = [sm.get_screen('champ_select').champion, self.dialog_btn.content_cls.text]
        except AttributeError:
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

        for i in range(len(self.grid.children) - 1, -1, -1):
            rune_info.append(self.grid.children[i].panel_cls.text.lower())

        screen = sm.get_screen('library')
        screen.root.clear_widgets()
        screen.my_runes.clear_widgets()

        rune = Rune(rune_info)
        rune.back_layer.children[0].bind(on_release=partial(screen.delete_rune, rune))
        rune.front_layer.bind(on_release=partial(screen.view_rune, rune))
        file_runes.add_new_rune(rune)

        for r in file_runes.runes:
            screen.my_runes.add_widget(r)

        screen.root.add_widget(screen.my_runes)
        self.close_box()

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
    RuneSaver().run()

    @atexit.register
    def save():
        with open('accounts/{}.csv'.format('Saiby100'), 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(file_runes.to_array())
