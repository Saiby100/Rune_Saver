from kivy.uix.button import Button, ButtonBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.window import Window
from kivy.uix.anchorlayout import AnchorLayout
from kivy.utils import get_color_from_hex
from kivy.uix.stacklayout import StackLayout
import os
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDToolbar
from kivy.graphics import *
from kivymd.uix.card import MDCard
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior



Window.size = (400, 600)

class MD3Card(MDCard, RoundedRectangularElevationBehavior):
    pass

class ImageButton(ButtonBehavior, Image):
    pass

class RuneSaver(MDApp):
    def build(self):

        global sm
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(Library('library'))
        sm.add_widget(ChampSelect('champ_select'))
        sm.add_widget(RunePage('rune_page'))

        return sm

class Library(Screen):
    def __init__(self, page_name):
        super().__init__(name=page_name)
        anchor_l = AnchorLayout(anchor_x='right', anchor_y='bottom', padding=30)
        stack_layout = StackLayout()

        with self.canvas:
            Color(rgba=get_color_from_hex('#000000'))
            Rectangle(size=Window.size)

        toolbar = MDToolbar(title='My Runes',
                            md_bg_color=get_color_from_hex('#000000')
                            )
        toolbar.right_action_items = [['menu', lambda x: print('search was pressed')]]


        self.add_btn = MDFloatingActionButton(icon='plus',
                                              md_bg_color=(get_color_from_hex('#00db63')),
                                             )
        self.add_btn.bind(on_release=self.champ_select)

        stack_layout.add_widget(toolbar)
        anchor_l.add_widget(self.add_btn)

        self.add_widget(anchor_l)
        self.add_widget(stack_layout)

    def champ_select(self, event):
        sm.current = 'champ_select'

class ChampSelect(Screen):
    def __init__(self, page_name):
        super().__init__(name=page_name)

        with self.canvas:
            Color(rgba=get_color_from_hex('#000000'))
            Rectangle(size=Window.size)

        root = ScrollView(size_hint=(1,None), size=(Window.width, Window.height))
        champ_grid = GridLayout(cols=3, spacing=10, padding=10, size_hint_y=None)
        champ_grid.bind(minimum_height=champ_grid.setter('height'))

        with open('images/champions.txt', 'r') as file:
            for champ in file.readlines():
                champ = champ.strip('\n')
                source = 'images/'+champ+'.jpg'

                if os.path.isfile(source):
                    img = Image(source=source,
                                size_hint_y=.8,
                                allow_stretch=True,
                                keep_ratio=False)
                    card = MD3Card(orientation='vertical',
                                   size_hint=(None, None),
                                   padding=5,
                                   radius=10
                                 )

                    card.add_widget(img)
                    source=source.strip('images/')
                    source=source.strip('.jpg')

                    card.add_widget(MDLabel(text=source, size_hint_y=.2))

                    # img = ImageButton(source=source,
                    #                   size_hint_y=None
                    #                   )
                    # img.bind(on_release=self.rune_select)
                    champ_grid.add_widget(card)
        root.add_widget(champ_grid)
        self.add_widget(root)

    def rune_select(self, event):
        sm.current = 'rune_page'



class RunePage(Screen):
    def __init__(self, page_name):
        super().__init__(name=page_name)
        btn = Button(text='go back')
        btn.bind(on_release=self.go_back)
        self.add_widget(btn)


    def go_back(self, event):
        sm.current='champ_select'

if __name__ == '__main__':
    RuneSaver().run()
