import csv
from kivymd.uix.button import MDFlatButton, ButtonBehavior, MDIconButton, MDFloatingActionButton
from kivymd.uix.card import MDCardSwipe, MDCardSwipeFrontBox, MDCardSwipeLayerBox, MDCard
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivy.uix.image import Image
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import ImageLeftWidget, OneLineAvatarListItem
from kivymd.uix.label import MDLabel
from kivymd.uix.tooltip import MDTooltip



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

class FloatingButton(MDFloatingActionButton, MDTooltip):
    pass

class SavedRunes: 
    def __init__(self, account_name):
        self.runes = []
        with open('accounts/{}.csv'.format(account_name), 'r') as file: 
            reader = csv.reader(file)
            for line in reader: 
                self.runes.append(Rune(line))

    def add_new_rune(self, new_rune):
        for i, rune in enumerate(self.runes): 
            if new_rune.champ <= rune.champ:
                self.runes.insert(i, new_rune)
                return
        self.runes.append(new_rune)

    def delete_rune(self, rune): 
        self.runes.remove(rune)

    def to_array(self):
        array = []
        for rune in self.runes:
            temp_arr = [rune.champ, rune.name]
            temp_arr.extend(rune.attributes())
            array.append(temp_arr)
        return array
        
class ExpansionPanel(MDExpansionPanel):
    def __init__(self, title, content=None):
        self.panel_cls = MDExpansionPanelOneLine(text=title)
        self.panel_cls.font_style = 'Body2'

        if content is not None:
            self.content = content
        super().__init__()

    def change_icon(self, icon):
        self.icon = icon

class ListItem(OneLineAvatarListItem):
    def __init__(self, text, image_source):
        self.text = text
        self.icon = ImageLeftWidget()
        self.icon.source = image_source
        super().__init__()
        self.add_widget(self.icon)

class Content(MDBoxLayout):
    def __init__(self, items_array):
        super().__init__()
        self.adaptive_height = True
        self.orientation = 'vertical'

        for item in items_array:
            self.add_widget(item)

class Card(MDCard):
    def __init__(self, src, txt):
        super().__init__()
        self.orientation = 'vertical'
        self.size_hint = (None, None)
        self.size = (90, 90)
        self.radius = '25dp'

        self.add_widget(Image(source=src,
                              allow_stretch=True,
                              keep_ratio=False,
                              size_hint=(None,None),
                              size=(90,70)))
        self.add_widget(MDLabel(text=txt, font_style='Caption', halign='center'))

class RuneCard(MDCard): 
    def __init__(self, src, text=None):
        super().__init__()
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.padding = '5dp'
        self.spacing = '5dp'
        self.radius = '25dp'

        self.add_widget(Image(source=src,
                              allow_stretch=True,
                              size_hint_y=None,
                              height=65))

        if text is not None:
            self.add_widget(MDLabel(text=text, halign='center', font_style='Caption'))

class Rune(SwipeToDeleteItem):
    def __init__(self, row):
        self.champ, self.name, self.main, self.key, self.slot1, self.slot2, self.slot3, self.secondary, self.slot_1, self.slot_2 = row
        super().__init__(self.name, 'icons/{}.png'.format(self.champ))

    def attributes(self):
        return [self.main, self.key, self.slot1, self.slot2, self.slot3, self.secondary, self.slot_1, self.slot_2]

    def edit(self, row):
        self.champ, self.name, self.main, self.key, self.slot1, self.slot2, self.slot3, self.secondary, self.slot_1, self.slot_2 = row
        self.list_item.text = self.name