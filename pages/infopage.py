from kivy.uix.screenmanager import Screen
from utils import config

class InfoPage(Screen):
    '''
        Page to view rune description.
    '''
    def __init__(self, attr, **kwargs):
        '''
            This initializes the superclass, sets up page layout 
            and fetches the rune description from the appropriate file.
        '''
        super().__init__(**kwargs)

        self.attribute = attr

        text = ""
        with open(f'rune_files/{self.attribute}.txt', 'r') as file:
            for line in file.readlines():
                text += line.strip()
                text += '\n'
        
        self.ids.rune_img.source = f'icons/runes/{self.attribute}.png'
        self.ids.attr_title.text = self.attribute.title()
        self.ids.attr_description.text = text

    def go_back(self):
        '''
            This removes the current page from the screen manager,
            and moves back to the view rune page.
        '''
        config.sm.current = 'view_page'
        config.sm.remove_widget(self)