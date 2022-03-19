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
from kivymd.uix.behaviors import MagicBehavior
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDToolbar
from kivy.graphics import *
from kivymd.uix.card import MDCard
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.stacklayout import MDStackLayout
from functools import partial



Window.size = (400, 600)
Window.color = get_color_from_hex('#000000')

class Btn(MDFloatingActionButton, MagicBehavior):
    pass

class Card(MDCard, ButtonBehavior):
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
        stack_layout = MDStackLayout(md_bg_color=get_color_from_hex('#000000'))

        # with self.canvas:
        #     Color(rgba=get_color_from_hex('#000000'))
        #     Rectangle(size=Window.size)

        toolbar = MDToolbar(title='My Runes',
                            md_bg_color=get_color_from_hex('#000000')
                            )
        toolbar.right_action_items = [['menu', lambda x: print('search was pressed')]]


        add_btn = Btn(icon='plus',
                      md_bg_color=(get_color_from_hex('#00db63')),
                     )
        add_btn.on_press = add_btn.wobble()

        add_btn.bind(on_release=self.champ_select)

        stack_layout.add_widget(toolbar)
        anchor_l.add_widget(add_btn)

        self.add_widget(stack_layout)
        self.add_widget(anchor_l)

    def champ_select(self, event):
        sm.current = 'champ_select'

class ChampSelect(Screen):
    def __init__(self, page_name):
        super().__init__(name=page_name)

        with self.canvas:
            Color(rgba=get_color_from_hex('#000000'))
            Rectangle(size=Window.size)

        box = BoxLayout(orientation='vertical')
        root = ScrollView(size_hint=(1,None), size=(Window.width, Window.height-70))
        champ_grid = MDStackLayout(size_hint_y=None, spacing=10, padding=5, md_bg_color=get_color_from_hex('#000000'))
        champ_grid.bind(minimum_height=champ_grid.setter('height'))

        with open('images/champions.txt', 'r') as file:
            i = 0
            a = 1
            for champ in file.readlines():
                # if i == a: break
                champ = champ.strip('\n')
                source = 'images/'+champ+'.jpg'

                if os.path.isfile(source):
                    img = Image(source=source,
                                size_hint_y=.8,
                                allow_stretch=True,
                                keep_ratio=False)
                    card = Card(orientation='vertical',
                                   size_hint=(None, None),
                                   padding=5,
                                   radius=10,
                                   md_bg_color=get_color_from_hex('#2e2c28'),
                                   size=(90,90)
                                 )

                    card.add_widget(img)
                    card_callback = partial(self.animate_card, card)
                    card.bind(on_press=card_callback)



                    champ_grid.add_widget(card)
                i+=1

        toolbar = MDToolbar(title='Choose a champion',
                            md_bg_color=get_color_from_hex('#000000')
                            )
        root.add_widget(champ_grid)
        box.add_widget(toolbar)
        box.add_widget(root)
        self.add_widget(box)

    def rune_select(self, event):
        sm.current = 'rune_page'

    def animate_card(self, widget, event):
        widget.size=(100,100)



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
