from Profile import Profile
from Widgets import SavedRunes
from kivy.uix.screenmanager import ScreenManager, NoTransition

def init():
    '''
        This initializes the global variables.
    '''
    global profile, saved_runes, sm
    profile = Profile()
    saved_runes = SavedRunes(profile.get_rune_data())
    sm = ScreenManager(transition=NoTransition())