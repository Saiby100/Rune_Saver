from kivy.uix.image import Image
from kivy.uix.stacklayout import StackLayout
from kivy.utils import get_color_from_hex
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivymd.uix.toolbar import MDToolbar


class TestCard(MDApp):
    def build(self):
        root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        # root.pos_hint = {'top':1}
        layout = StackLayout(size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        # layout.pos_hint = {'top':1}

        with open('images/champions.txt', 'r') as file:
            i = 0
            a = 10
            for champ in file.readlines():
                # if i == a: break
                champ = champ.strip('\n')
                source = 'images/'+champ+'.jpg'

                img = Image(source=source,
                            # size_hint_y=.8,
                            allow_stretch=True,
                            keep_ratio=False)
                card = MDCard(orientation='vertical',
                               size_hint=(None, None),
                               padding=5,
                               radius=10,
                               md_bg_color=get_color_from_hex('#2e2c28')
                             )

                card.add_widget(img)
                layout.add_widget(card)
                i+=1

        toolbar = MDToolbar(title='My Runes',
                            md_bg_color=get_color_from_hex('#000000')
                            )
        # root.add_widget(toolbar)
        root.add_widget(layout)



        return root

    # def on_start(self):
    #     styles = {
    #         "elevated": "#f6eeee", "filled": "#f4dedc", "outlined": "#f8f5f4"
    #     }
    #     for style in styles.keys():
    #
    #         card = MDCard(text=style.capitalize())
    #         card.line_color=(0.2,.2,.2,.8)
    #         card.mg_bg_color=get_color_from_hex(styles[style])
    #
    #         self.root.ids.box.add_widget(card)


TestCard().run()