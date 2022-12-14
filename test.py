from kivymd.app import MDApp
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.image import Image
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty, BooleanProperty
from kivymd.uix.label import MDLabel


class DetailsCard(MDCard):
    source = StringProperty()
    text = StringProperty()
    allow_img_stretch = BooleanProperty(False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        img = Image(source=self.source,
                    size_hint_x=.3,
                    allow_stretch=self.allow_img_stretch)

        lbl = MDLabel(text=self.text,
                      font_style='H5',
                      size_hint_x=.7)

        self.size_hint_y = None
        self.size_hint_x = None
        self.radius = '30dp'
        self.padding = 5
        self.spacing = 50

        self.add_widget(img)
        self.add_widget(lbl)


class MyApp(MDApp):

    def build(self):

        self.theme_cls.theme_style = 'Dark'
        grid = MDGridLayout(cols=1,
                            spacing=10,
                            padding=10)

        card = DetailsCard(orientation='horizontal',
                           text="Saiby100\nLevel: 97",
                           source="icons/profileicon/665.png",
                           width=400
                           )
        card2 = DetailsCard(orientation='horizontal',
                            text="Bronze II\n8 Wins / 19 Losses",
                            source="icons/tiers/Emblem_Bronze.png",
                            width=400,
                            allow_img_stretch=True
                            )

        grid.add_widget(card)
        grid.add_widget(card2)
        return grid


if __name__ == '__main__':
    MyApp().run()
