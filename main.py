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

Window.size = (300, 500)

main_runes = ['domination','precision','inspiration','resolve','sorcery']

titles = {'domination': ['Keystones','Malice','Tracking','Hunter'],
          'precision': ['Keystones','Heroism','Legend','Combat'],
          'inspiration': ['Keystones','Contraptions','Tomorrow','Beyond'],
          'resolve': ['Keystones','Strength','Resistance','Vitality'],
          'sorcery': ['Keystones','Artifact','Excellence','Power']}

runes =  {'domination': {'Keystones': ['electrocute','predator','dark-harvest','hail-of-blades'],
                        'Malice': ['cheap-shot','taste-of-blood','sudden-impact'],
                        'Tracking': ['zombie-ward','ghost-poro','eyeball-collection'],
                        'Hunter': ['ravenous-hunter','ingenious-hunter','relentless-hunter','ultimate-hunter']},

         'precision': {'Keystones': ['press-the-attack','lethal-tempo','fleet-footwork','conqueror'],
                        'Heroism': ['overheal','triumph','presence-of-mind'],
                        'Legend': ['legend-alacrity','legend-tenacity','legend-bloodline'],
                        'Combat': ['coup-de-grace','cut-down','last-stand']},

         'inspiration': {'Keystones': ['glacial-augment','unsealed-spellbook','first-strike'],
                        'Contraptions': ['hextech-flashtraption','magical-footwear','perfect-timing'],
                        'Tomorrow': ['future\'s-market','minion-dematerializer','biscuit-delivery'],
                        'Beyond': ['cosmic-insight','approach-velocity','time-warp-tonic']},

         'resolve': {'Keystones': ['grasp-of-the-undying','aftershock','guardian'],
                        'Strength': ['demolish','font-of-life','shield-bash'],
                        'Resistance': ['conditioning','second-wind','bone-plating'],
                        'Vitality': ['overgrowth','revitalize','unflinching']},

         'sorcery': {'Keystones': ['summon-aery','arcane-comet','phase-rush'],
                        'Artifact': ['nullifying-orb','manaflow-band','nimbus-cloak'],
                        'Excellence': ['transcendence','celerity','absolute-focus'],
                        'Power': ['scorch','waterwalking','gathering-storm']}
         }
secondary_runes = {'domination': ['cheap-shot','taste-of-blood','sudden-impact', 'zombie-ward','ghost-poro','eyeball-collection',
                                  'ravenous-hunter','ingenious-hunter','relentless-hunter','ultimate-hunter'],
                   'precision': ['overheal','triumph','presence-of-mind','legend-alacrity','legend-tenacity','legend-bloodline',
                                 'coup-de-grace','cut-down','last-stand'],
                   'inspiration': ['hextech-flashtraption','magical-footwear','perfect-timing','future\'s-market','minion-dematerializer',
                                   'biscuit-delivery','cosmic-insight','approach-velocity','time-warp-tonic'],
                   'resolve': ['demolish','font-of-life','shield-bash','conditioning','second-wind','bone-plating','overgrowth','revitalize',
                               'unflinching'],
                   'sorcery': ['nullifying-orb','manaflow-band','nimbus-cloak','transcendence','celerity','absolute-focus','scorch','waterwalking',
                               'gathering-storm']
                   }


class RuneSaver(MDApp):
    def build(self):
        #Red, Pink, Purple, DeepPurple, Indigo, Blue, LightBlue, Cyan, Teal, Green, LightGreen, Lime, Yellow, Amber, Orange, DeepOrange, Brown, Gray, BlueGray
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Lime"
        global sm
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(Library('library'))
        sm.add_widget(ChampSelect('champ_select'))
        sm.add_widget(RunePage('rune_page'))
        # sm.add_widget(SearchPage('search_page'))

        return sm

class SearchPage(Screen): 
    pass 

        

class Library(Screen):
    # use list object to save runes
    def __init__(self, page_name):
        super().__init__(name=page_name)

        #Initializing Layouts
        self.box = MDBoxLayout(orientation='vertical')
        self.anchor_layout = AnchorLayout(anchor_x='right',
                                          anchor_y='bottom',
                                          padding=30)
        self.root = ScrollView(size_hint=(1, None),
                               size=(Window.width, Window.height-60))

        #Initializing Widgets
        self.toolbar = MDToolbar(title='My Runes')
        self.toolbar.right_action_items = [['magnify', self.search]]

        self.add_btn = MDFloatingActionButton(icon='plus')
        self.add_btn.bind(on_release=self.champ_select)

        self.my_runes = MDList(padding=[10, 0])
        self.saved_runes = SavedRunes('Saiby100').runes

        #Adding widgets to layouts
        for rune in self.saved_runes: 
            rune.icon.bind(on_release=partial(self.remove, rune))
            rune.list_item.bind(on_release=partial(self.view_rune, rune))
            self.my_runes.add_widget(rune)

        self.root.add_widget(self.my_runes)
        self.box.add_widget(self.toolbar)
        self.box.add_widget(self.root)
        self.anchor_layout.add_widget(self.add_btn)

        #Adding Layouts to Screen
        self.add_widget(self.box)
        self.add_widget(self.anchor_layout)

    def view_rune(self, rune, event): 
        self.rune = rune 
        sm.add_widget(ViewRune('view_page'))
        sm.current = 'view_page'

    def champ_select(self, event):
        sm.current = 'champ_select'

    def search(self, event):
        pass

    def remove(self, item, instance):
        self.my_runes.remove_widget(item)



class ViewRune(Screen):
    def __init__(self, page_name):
        super().__init__(name=page_name)

        self.rune = sm.get_screen('library').rune

        #Initializing Layouts
        self.anchor_layout = AnchorLayout(anchor_x='right',
                                          anchor_y='bottom',
                                          padding=30)
        self.box = BoxLayout(orientation='vertical',
                             pos_hint={'top':1})
        self.root = ScrollView(size_hint=(1,None),
                               size=(Window.width, Window.height-64))
        self.grid = MDGridLayout(cols=2,
                                 size_hint_y=None,
                                 spacing=10,
                                 padding=10)
        self.grid.bind(minimum_height=self.grid.setter('height'))

        #Initializing Widgets
        self.toolbar = MDToolbar(title=self.rune.name.title())
        self.toolbar.right_action_items=[['icons/{}.png'.format(self.rune.champ)]]
        self.toolbar.left_action_items=[['arrow-left', self.go_back]]
        self.edit_btn = MDFloatingActionButton(icon='pencil')
        self.edit_btn.bind(on_release=partial(self.edit_rune, self.rune))

        for attribute in self.rune.attributes():
            self.grid.add_widget(RuneCard('Runes/{}.png'.format(attribute), attribute.title()))

        #Adding Widgets to Layouts
        self.anchor_layout.add_widget(self.edit_btn)
        self.root.add_widget(self.grid)
        self.box.add_widget(self.toolbar)
        self.box.add_widget(self.root)

        #Adding Layout to Screen
        self.add_widget(self.box)
        self.add_widget(self.anchor_layout)

    def go_back(self, event): 
        sm.remove_widget(sm.get_screen('view_page'))
        sm.current = 'library'

    def edit_rune(self, rune, event):
        screen = sm.get_screen('rune_page')
        screen.toolbar.title = rune.champ.title()
        screen.toolbar.right_action_items = [['icons/{}.png'.format(rune.champ)]]
        screen.edit(rune)
        screen.previous = self.name
        sm.current = 'rune_page'


class ChampSelect(Screen):
    def __init__(self, page_name):
        super().__init__(name=page_name)

        #Initializing Layouts
        self.box = BoxLayout(orientation='vertical',
                             pos_hint={'top':1})
        self.root = ScrollView(size_hint=(1,None),
                               size=(Window.width, Window.height-64))
        self.champ_grid = MDStackLayout(size_hint_y=None,
                                        spacing=10,
                                        padding=5)
        self.champ_grid.bind(minimum_height=self.champ_grid.setter('height'))

        #Initializing Cards
        with open('Resources/champions.txt', 'r') as file:
            for champ in file.readlines():
                champ = champ.strip('\n')
                source = 'images/{}.jpg'.format(champ)
                card = Card(source, champ.title())
                card.bind(on_release=partial(self.create_rune, champ))

                self.champ_grid.add_widget(card)

        #Initializing Widgets
        self.toolbar = MDToolbar(title='Select Champion')
        self.toolbar.right_action_items = [['magnify']]
        self.toolbar.left_action_items = [['arrow-left', self.go_back]]

        #Adding Widgets to Layouts
        self.root.add_widget(self.champ_grid)
        self.box.add_widget(self.toolbar)
        self.box.add_widget(self.root)

        #Adding Layouts to Screen
        self.add_widget(self.box)

    def create_rune(self, champ, event):
        self.champion = champ
        screen = sm.get_screen('rune_page')

        screen.toolbar.title = champ.title()
        screen.toolbar.right_action_items = [['icons/'+champ+'.png']]
        screen.previous = self.name
        screen.default_panels('precision', 'resolve')

        sm.current = 'rune_page'

    def go_back(self, event):
        sm.current = 'library'


class RunePage(Screen):
    def __init__(self, page_name):
        super().__init__(name=page_name)
        self.previous = None
        #Initializing Layouts
        self.stack_layout = MDStackLayout(size_hint_y=None,
                                          pos_hint={'top':1})
        self.stack_layout.size[1] = 64
        self.root = ScrollView(size_hint=(1, None),
                               size=(Window.width, Window.height - 64))
        self.anchor_layout = AnchorLayout(anchor_x='right',
                                          anchor_y='bottom',
                                          padding=30)
        self.grid = MDGridLayout(cols=1,
                                 padding=[10,0],
                                 size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))

        self.primary_panels = []
        self.secondary_panels = []
        self.dialog_btn = None 
            
        self.toolbar = MDToolbar(title="Holder Text")
        self.toolbar.left_action_items = [['arrow-left', self.go_back]]
        
        self.panel = ExpansionPanel('Main Rune',
                                    self.create_content(main_runes))
        self.grid.add_widget(self.panel)
        self.primary_panels.append(self.panel)
        self.get_runes()

        self.panel2 = ExpansionPanel('Secondary Rune',
                                     self.create_content(main_runes))
        self.secondary_panels.append(self.panel2)
        self.grid.add_widget(self.panel2)
        self.get_secondary_runes()

        self.save_btn = MDFloatingActionButton(icon='check')
        self.save_btn.bind(on_release=self.show_save_box)

        self.root.add_widget(self.grid)
        self.stack_layout.add_widget(self.toolbar)
        self.anchor_layout.add_widget(self.save_btn)
        
        self.add_widget(self.root)
        self.add_widget(self.stack_layout)
        self.add_widget(self.anchor_layout)

    def go_back(self, event):
        sm.current = self.previous

    def default_panels(self, prim, second):
        attributes = [prim]
        attributes.extend(titles[prim])
        attributes.extend([second, 'slot 1', 'slot 2'])
        attributes.reverse()

        secondary = secondary_runes[attributes[2]]

        for i in range(len(attributes)):
            self.grid.children[i].panel_cls.text = attributes[i].title()
            if i <= 1:
                # Secondary panels
                self.grid.children[i].content = self.create_content(secondary)
            elif i >= 3 and i < 7:
                # Primary panels
                self.grid.children[i].content = self.create_content(runes[attributes[7]][attributes[3 : 7][i - 3].title()])

    #Adds all panels given a main rune
    def get_runes(self, main='domination'):
        for title in titles[main]:
            panel = ExpansionPanel(title, self.create_content(runes[main][title]))
            self.primary_panels.append(panel)
            self.grid.add_widget(panel)

    def get_secondary_runes(self, main='sorcery'):
        all_runes = []
        for i in range(1, len(titles[main])):
            all_runes.extend(runes[main][titles[main][i]])

        self.secondary_panels.append(ExpansionPanel('Slot 1', self.create_content(all_runes)))
        self.grid.add_widget(self.secondary_panels[1])
        self.secondary_panels.append(ExpansionPanel('Slot 2', self.create_content(all_runes)))
        self.grid.add_widget(self.secondary_panels[2])

    #Creates a content widget containing all the runes specified in the array
    def create_content(self, array):
        items = []
        for value in array:
            value = value.strip('\n')
            item = ListItem(value.title(), 'Runes/'+value+'.png')
            item.bind(on_release=partial(self.update_panel, item, value))
            items.append(item)

        return Content(items)

    #All contents of the expansion panels below it must change
    def update_panel(self, item, text, event):

        if main_runes.__contains__(text) and not self.secondary_panels.__contains__(item.parent.parent):
            i = 3
            for child in self.grid.children:
                if child != item.parent.parent and not self.secondary_panels.__contains__(child):
                    child.content = self.create_content(runes[text][titles[text][i]])
                    child.panel_cls.text = titles[text][i]
                    i-=1

        elif main_runes.__contains__(text):
            all_runes = []
            for i in range(1, len(titles[text])):
                all_runes.extend(runes[text][titles[text][i]])
            i = 1
            slots = ['Slot 1', 'Slot 2']
            for child in self.grid.children:
                if child != item.parent.parent and not self.primary_panels.__contains__(child):
                    child.content = self.create_content(all_runes)
                    child.panel_cls.text = slots[i]
                    i-=1

        item.parent.parent.panel_cls.text = text.title()

    def show_save_box(self, event): 
        save_btn = MDFlatButton(text='SAVE', on_release=self.save)
        back_btn = FlatButton(text='CANCEL', on_release=self.back)
        
        self.dialog_btn = MDDialog(title='Rune Name:',
                                    type='custom',
                                    content_cls=MDTextField(),
                                    buttons=[back_btn, save_btn])
        self.dialog_btn.open()

    def save(self, event=None):
        info = [sm.get_screen('champ_select').champion, self.dialog_btn.content_cls.text]
        for panel in self.primary_panels:
            info.append(panel.panel_cls.text.lower())
        for panel in self.secondary_panels:
            info.append(panel.panel_cls.text.lower())
 
        with open('accounts/Saiby100.csv', 'a', newline="") as file:
            writer = csv.writer(file)
            writer.writerow(info)
        
        self.back()
        sm.remove_widget(sm.get_screen('library'))
        sm.add_widget(Library('library'))
        sm.current = 'library'

    def edit(self, rune):
        attributes = rune.attributes()
        attributes.reverse()
        main = []
        secondary = secondary_runes[rune.secondary]
        main.extend(runes[rune.main].keys())
        main.reverse()

        for i in range(len(attributes)):
            self.grid.children[i].panel_cls.text = attributes[i].title()
            if i <= 1:
                #Secondary panels
                self.grid.children[i].content = self.create_content(secondary)
            elif i >=3 and i < 7:
                #Primary panels
                self.grid.children[i].content = self.create_content(runes[rune.main][main[i-3]])

    def back(self, event=None):
        self.dialog_btn.dismiss()

if __name__ == '__main__':
    RuneSaver().run()
