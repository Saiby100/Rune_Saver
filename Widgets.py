import csv 
from kivymd.uix.button import MDFlatButton, ButtonBehavior, MDIconButton
from kivymd.uix.card import MDCardSwipe, MDCardSwipeFrontBox, MDCardSwipeLayerBox, MDCard
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivy.uix.image import Image
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import ImageLeftWidget, OneLineAvatarListItem
from kivymd.uix.label import MDLabel

class FlatButton(MDFlatButton, ButtonBehavior): 
    pass

class SwipeToDeleteItem(MDCardSwipe):
    def __init__(self, text, img_source):
        super().__init__()
        self.size_hint_y = None
        self.height = 55
        self.icon = MDIconButton(icon='trash-can', pos_hint={'center_y': .5})
        self.list_item = ListItem(text, img_source)
        self.front_layer = MDCardSwipeFrontBox()
        self.front_layer.add_widget(self.list_item)

        self.back_layer = MDCardSwipeLayerBox()
        self.back_layer.add_widget(self.icon)
        

        self.add_widget(self.back_layer)
        self.add_widget(self.front_layer)

class Rune(SwipeToDeleteItem):
    def __init__(self, row):
        self.champ, self.name, self.main, self.key, self.slot1, self.slot2, self.slot3, self.secondary, self.slot_1, self.slot_2 = row
        super().__init__(self.name, 'icons/{}.png'.format(self.champ))


class SavedRunes: 
    def __init__(self, account_name):
        self.runes = []
        with open('accounts/{}.csv'.format(account_name), 'r') as file: 
            reader = csv.reader(file)
            for line in reader: 
                self.runes.append(Rune(line))
        

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
                         allow_stretch=True,
                         keep_ratio=False)

        self.add_widget(self.img)

class RuneCard(MDCard): 
    def __init__(self, src, text="Teemo", subtext="Teemo"): 
        super().__init__()
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.padding = '15dp'
        self.radius = '25dp'

        self.add_widget(Image(source=src, size=self.size))
        self.add_widget(MDLabel(text=text, halign='center', font_style='H6'))
        self.add_widget(MDLabel(text= subtext, halign='center'))