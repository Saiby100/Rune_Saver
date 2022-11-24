from kivymd.uix.card import MDCard
from kivy.properties import StringProperty
from kivymd.uix.behaviors import HoverBehavior
from kivymd.app import MDApp

class ChampCard(MDCard, HoverBehavior):
    '''
        Card used on champ select page.
    '''
    text = StringProperty()
    source = StringProperty()

    def build_rune(self):
        #Refereces champ-select page
        screen = self.parent.parent.parent.parent 
        screen.build_rune(self.text)

    def on_enter(self):
        self.app = MDApp.get_running_app()
        self.md_bg_color = self.app.theme_cls.primary_dark
    
    def on_leave(self):
        self.md_bg_color = self.app.theme_cls.bg_light

class RuneCard(MDCard):
    '''
        Card used on view Rune Page.
    '''
    source = StringProperty()
    txt = StringProperty()

    def view_attribute(self):
        '''
            This fetches the text for the selected rune card
            and moves to the page for viewing the rune description.
        '''

        #References the ViewRune page
        screen = self.parent.parent.parent.parent.parent.parent.parent.parent
        screen.view_attribute(self.txt.lower())

class ItemCard(RuneCard):
    '''
        Card that will be used for creating builds (TODO).
    '''
    def __init__(self, src, text=None):
        super().__init__(src, text)
        self.size_hint = (None, None)