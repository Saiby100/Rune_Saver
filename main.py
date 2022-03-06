from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.window import Window


class myApp(App):
    def build(self):
        global sm
        sm = ScreenManager(transition=FadeTransition)


class ChampSelect(Screen):
    def __init__(self, page_name):
        super().__init__(name=page_name)


class Library(Screen):
    def __init__(self, page_name):
        super().__init__(name=page_name)






if __name__ == '__main__':
    myApp().run()
