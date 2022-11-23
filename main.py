import atexit
from kivy.core.window import Window
from kivymd.app import MDApp
from pages.library import Library
from pages.playerprofile import PlayerProfile
from pages.buildrune import BuildRune
from pages.matchhistory import MatchHistory
from utils import config

Window.minimum_width, Window.minimum_height = (705, 500)
Window.size = (980, 670)

class RuneSaver(MDApp):
    '''
        This class initializes the screen manager and manages the app.
    '''
    def build(self):
        
        #Initialize global variables.
        config.init()
        '''
            Valid themes: 'Light' or 'Dark'.
        '''
        self.theme_cls.theme_style = "Dark"
        '''
            Valid Themes: Red, Pink, Purple, DeepPurple, Indigo, Blue,
            LightBlue, Cyan, Teal, Green, LightGreen, Lime, Yellow,
            Amber, Orange, DeepOrange, Brown, Gray, BlueGray
        '''
        self.theme_cls.primary_palette = "BlueGray"

        return config.sm

    def on_start(self):
        '''
            This is called when the application is launched.
        '''
        config.sm.add_widget(Library(name='library'))
        config.sm.add_widget(BuildRune(name='rune_page'))
        config.sm.add_widget(PlayerProfile(name='profile'))
        config.sm.add_widget(MatchHistory(name='match_history'))
        config.sm.current = 'library'
    
    def change_screen(self, screen_name):
        '''
            This is used for moving between library, profile, 
            and match history pages.
            Called from kv file.
        '''
        if config.sm.current == screen_name: 
            return
        config.sm.current = screen_name

if __name__ == '__main__':

    @atexit.register
    def save():
        config.profile.save(config.saved_runes.to_array())

    RuneSaver().run()