from kivy.uix.button import Button, ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.window import Window
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFloatingActionButton, MDIconButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.card import MDCard, MDCardSwipe, MDCardSwipeLayerBox, MDCardSwipeFrontBox
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.stacklayout import MDStackLayout
from functools import partial
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivymd.uix.list import OneLineAvatarListItem, ImageLeftWidget, MDList
import csv
from kivymd.font_definitions import theme_font_styles

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



class SwipeToDeleteItem(MDCardSwipe):
    def __init__(self, text, img_source):
        super().__init__()
        self.size_hint_y = None
        self.height = 55
        self.type_swipe = 'hand'
        self.icon = MDIconButton(icon='trash-can', pos_hint={'center_y': .5})

        self.front_layer = MDCardSwipeFrontBox()
        self.front_layer.add_widget(ListItem(text, img_source))

        self.back_layer = MDCardSwipeLayerBox()
        self.back_layer.add_widget(self.icon)

        self.add_widget(self.back_layer)
        self.add_widget(self.front_layer)

class Rune:
    def __init__(self, row):
        self.champ, self.main, self.key, self.slot1, self.slot2, self.slot3, self.secondary, self.slot_1, self.slot_2 = row

    def widget(self):
        return SwipeToDeleteItem('New rune', 'icons/'+self.champ+'.png')

class ExpansionPanel(MDExpansionPanel):
    def __init__(self, title, content):

        self.panel_cls = MDExpansionPanelOneLine(text=title)
        self.panel_cls.font_style = 'Body2'
        self.content = content
        self.main = False
        super().__init__()

    def change_icon(self, icon):
        self.icon = icon

class ListItem(OneLineAvatarListItem):
    def __init__(self, text, image_source):
        self.text = text
        img = ImageLeftWidget()
        img.source = image_source
        super().__init__()
        self.add_widget(img)

class Content(MDBoxLayout):
    def __init__(self, items_array):
        super().__init__()
        self.adaptive_height = True
        self.orientation = 'vertical'

        for item in items_array:
            self.add_widget(item)

class Card(MDCard, ButtonBehavior):
    def __init__(self, source):
        super().__init__()
        self.orientation = 'vertical'
        self.size_hint = (None, None)
        self.size = (90, 90)
        self.radius = [15]

        self.img = Image(source=source,
                         # size_hint=(None,None),
                         allow_stretch=True,
                         keep_ratio=False)

        self.add_widget(self.img)


class RuneSaver(MDApp):
    def build(self):
        #Red, Pink, Purple, DeepPurple, Indigo, Blue, LightBlue, Cyan, Teal, Green, LightGreen, Lime, Yellow, Amber, Orange, DeepOrange, Brown, Gray, BlueGray
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Lime"
        global sm
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(Library('library'))
        sm.add_widget(ChampSelect('champ_select'))

        return sm

class Library(Screen):
    # use list object to save runes
    def __init__(self, page_name):
        super().__init__(name=page_name)

        anchor_layout = AnchorLayout(anchor_x='right', anchor_y='bottom', padding=30)
        box = MDBoxLayout(orientation='vertical')
        root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height-60), scroll_timeout=100)
        self.my_runes = MDList(padding=[10, 0])
        self.saved_runes = []

        toolbar = MDToolbar(title='My Runes')
        toolbar.right_action_items = [['magnify', self.search]]

        add_btn = MDFloatingActionButton(icon='plus')
        add_btn.bind(on_release=self.champ_select)

        with open('accounts/Saiby100.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                rune = Rune(row)
                rune.widget().bind(on_release=partial(self.remove, rune.widget()))
                self.saved_runes.append(rune)
                self.my_runes.add_widget(rune.widget())

        swipe_card = SwipeToDeleteItem('This is a test', 'icons/quinn.png')
        swipe_card.icon.bind(on_release=partial(self.remove, swipe_card))


        root.add_widget(self.my_runes)
        box.add_widget(toolbar)
        box.add_widget(root)
        anchor_layout.add_widget(add_btn)

        self.add_widget(box)
        self.add_widget(anchor_layout)

    def champ_select(self, event):
        sm.current = 'champ_select'

    def search(self, event):
        pass

    def remove(self, item, instance):
        self.my_runes.remove_widget(item)





class ViewRune(Screen):
    def __init__(self, page_name):
        super().__init__(name=page_name)

class ChampSelect(Screen):
    def __init__(self, page_name):
        super().__init__(name=page_name)
        box = BoxLayout(orientation='vertical', pos_hint={'top':1})
        root = ScrollView(size_hint=(1,None), size=(Window.width, Window.height-64))
        champ_grid = MDStackLayout(size_hint_y=None, spacing=10, padding=5)
        champ_grid.bind(minimum_height=champ_grid.setter('height'))

        with open('Resources/champions.txt', 'r') as file:
            for champ in file.readlines():
                source = 'images/'+champ.strip('\n')+'.jpg'
                card = Card(source)
                card.bind(on_release=partial(self.create_rune, champ.strip('\n')))

                champ_grid.add_widget(card)

        toolbar = MDToolbar(title='Select Champion')
        toolbar.right_action_items = [['magnify']]
        toolbar.left_action_items = [['arrow-left', self.go_back]]

        root.add_widget(champ_grid)
        box.add_widget(toolbar)
        box.add_widget(root)

        self.add_widget(box)

    def rune_select(self, event):
        sm.current = 'rune_page'

    def create_rune(self, champ, event):
        self.champion = champ
        sm.add_widget(RunePage('rune_page'))
        sm.current = 'rune_page'

    def go_back(self, event):
        sm.current = 'library'


class RunePage(Screen):
    def __init__(self, page_name):
        super().__init__(name=page_name)
        stack_layout = MDStackLayout(size_hint_y=None, pos_hint={'top':1})
        stack_layout.size[1] = 64
        root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height - 64))

        self.grid = MDGridLayout(cols=1, padding=[10,0], size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))

        self.primary_panels = []
        self.secondary_panels = []

        champ = sm.get_screen('champ_select').champion
        toolbar = MDToolbar(title=champ.title())
        toolbar.left_action_items = [['arrow-left', self.go_back]]
        toolbar.right_action_items = [['icons/'+champ+'.png', partial(self.save, champ)]]

        panel = ExpansionPanel('Main Rune', self.create_content(main_runes))
        self.grid.add_widget(panel)
        self.primary_panels.append(panel)
        self.get_runes()

        panel = ExpansionPanel('Secondary Rune', self.create_content(main_runes))
        self.secondary_panels.append(panel)
        self.grid.add_widget(panel)
        self.get_secondary_runes()

        stack_layout.add_widget(toolbar)
        root.add_widget(self.grid)

        self.add_widget(root)
        self.add_widget(stack_layout)

    def go_back(self, event):
        sm.current='champ_select'
        sm.remove_widget(sm.get_screen('rune_page'))

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

    def save(self, champion, event):
        info = [champion]
        for panel in self.primary_panels:
            info.append(panel.panel_cls.text)
        for panel in self.secondary_panels:
            info.append(panel.panel_cls.text)

        with open('accounts/Saiby100.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow(info)



if __name__ == '__main__':
    RuneSaver().run()
