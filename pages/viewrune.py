from Widgets import titles, RuneCard
from .infopage import InfoPage
from utils import config
from kivy.uix.screenmanager import Screen

class ViewRune(Screen):
    '''
        Page to view rune attributes for each saved rune.
    '''
    def __init__(self, **kwargs):
        '''
            This initializes the superclass, and
            sets up the toolbar and page layout.
        '''
        super().__init__(**kwargs)
        self.rune = config.sm.get_screen('library').rune
        
        toolbar = self.ids.toolbar
        toolbar.title = self.rune.name
        toolbar.right_action_items = [[f'icons/champ_icons/{self.rune.champ}.png']]

        for attribute in self.rune.attributes():
            rune_card = RuneCard(source=f'icons/runes/{attribute}.png', txt=attribute.title())
            self.ids.rune_grid.add_widget(rune_card)

    def go_back(self, event=None):
        '''
            This removes itself from the screen manager,
            and moves back to the library page.
        '''
        config.sm.current = 'library'
        config.sm.remove_widget(self)

    def view_attribute(self, attribute, event=None):
        '''
            This initializes an InfoPage to view the rune description.
        '''
        if attribute in titles.keys():
            return

        screen = InfoPage(attribute, name='rune_info')
        config.sm.add_widget(screen)
        config.sm.current = 'rune_info'