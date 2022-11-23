from Widgets import Card
from kivy.uix.screenmanager import Screen
from utils import config

class ChampSelect(Screen):
    '''
        Page to choose a champion.
    '''
    def __init__(self, **kwargs):
        '''
            This initializes the superclass, and sets up the
            champion cards and adds them to the layout.
        '''
        super().__init__(**kwargs)

        # Initializing Champion Cards
        with open('resources/champions.txt', 'r') as file:
            for champ in file.readlines():
                champ = champ.strip('\n')
                source = f'icons/champ_images/{champ}.png'

                self.ids.champ_grid.add_widget(Card(source=source, 
                                                    text=champ.title()))

    def build_rune(self, champ):
        '''
            This sets up the BuildRune page and moves to it.
        '''
        screen = config.sm.get_screen('rune_page')

        screen.title = champ.title()
        screen.champion = champ
        screen.previous = self.name

        config.sm.current = 'rune_page'

    def go_back(self):
        config.sm.current = 'library'