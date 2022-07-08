from kivy.animation import Animation
from kivymd.uix.behaviors import HoverBehavior
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.properties import BooleanProperty, StringProperty, ListProperty
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.label import MDLabel
from Widgets import runes, secondary_runes

class ImageButton(ButtonBehavior, Image, HoverBehavior):
    name = StringProperty()

class IconDrawer(MDRelativeLayout):
    is_open = BooleanProperty(True)
    row = ListProperty(['domination', 'precision', 'sorcery', 'inspiration', 'resolve'])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.radius = '50dp'
        self.size_hint_y = None
        titles = self.row
        if titles is not None:
            for i, title in enumerate(titles):
                self.add_widget(ImageButton(source=f'icons/runes/{title}.png',
                                            name=title,
                                            on_release=lambda x: self.toggle(x),
                                            pos_hint={'x': i/len(titles)}))
    def toggle(self, caller):
        '''Toggle function used by icons in the drawer'''
        if self.is_open:
            self.close(caller)
        else:
            self.open()
    
    def open(self):
        '''Expands the drawer'''
        self.remove_widget(self.title_label)
        self.is_open = True
        x = 0
        for i in range(len(self.children)-1, -1, -1):
            open_anim = Animation(pos_hint={'x': x}, opacity=1, duration=.2)
            open_anim.start(self.children[i])
            x+=1/len(self.children)
    
    def close(self, caller):
        '''Closes the drawer with the caller being visible'''
        self.manager = self.parent #Initialize drawer manager
        self.selected_button = caller
        self.is_open = False

        caller_anim = Animation(pos_hint={'x': 0}, duration=.2)
        anim = Animation(pos_hint={'x': 0}, opacity=0, duration=.2)
        
        for img_btn in self.children:
            if img_btn.name == caller.name:
                caller_anim.start(img_btn)
            else:
                anim.start(img_btn)
        self.show_title()
        if caller.name in runes.keys():
            self.parent.add_corresponding_drawers(caller.name)
    
    def show_title(self):
        '''Show the selected button's name when icon drawer closes'''
        self.title_label = MDLabel(text=self.selected_button.name.title(),
                                   pos_hint={'x': .5},
                                   opacity=0)
        self.add_widget(self.title_label)

        label_anim = Animation(opacity=1, duration=.5)
        label_anim.start(self.title_label)
    


class IconDrawerManager(MDRelativeLayout):
    '''Class specifically used for build rune page'''
    is_primary = BooleanProperty(True)
    main_rune = StringProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(IconDrawer(pos_hint={'top':1}))

    def remove_corresponding_drawers(self):
        '''Removes all drawers below the primary rune drawer'''
        self.animate_drawers_collapse()
        for i in range(len(self.children)-1):
            self.remove_widget(self.children[0])

    def add_corresponding_drawers(self, main_rune):
        '''Adds rune drawers corresponding to chosen rune on primary drawer'''
        if self.main_rune == main_rune and len(self.children) > 1: 
            return
        if len(self.children) > 1:
            self.remove_corresponding_drawers()
        
        if self.is_primary:
            for key in runes[main_rune]:
                drawer = IconDrawer(row=runes[main_rune][key],
                                    pos_hint={'top': 1},
                                    opacity=0)
                self.add_widget(drawer)
        else:
            for i in range(2):
                drawer = IconDrawer(row=secondary_runes[main_rune],
                                    pos_hint={'top': 1},
                                    opacity=0)
                self.add_widget(drawer)

        self.animate_drawers_expansion()
        self.main_rune = main_rune

    def animate_drawers_expansion(self):
        '''Animates the adding of corresponding rune drawers'''
        x = val = 1/len(self.children)

        for i in range(len(self.children)-1):
            animation = Animation(pos_hint={'top':x}, opacity=1, duration=.3)
            x += val
            animation.start(self.children[i])
    
    def animate_drawers_collapse(self):
        '''Animates the removal of rune drawers'''
        animation = Animation(pos_hint={'top': 1}, opacity=0, duration=.3)
        for i in range(len(self.children)-1):
            animation.start(self.children[i])

    def preset(self, rune):
        '''Presets the icon manager to the given rune'''
        rune.reverse()
        self.add_corresponding_drawers(rune[len(rune)-1])
        self.children[len(self.children)-1].close(ImageButton(name=rune[len(rune)-1]))
        
        for i in range(len(self.children)-1):
            self.children[i].close(ImageButton(name=rune[i]))

    def reset(self):
        '''Removes all corresponding drawers and resets the primary rune drawer to open'''
        for i in range(len(self.children)-1):
            self.remove_widget(self.children[0])

        if not self.children[0].is_open: 
            self.children[0].open() 

    def drawer_titles(self):
        '''Returns all the drawers of the manager'''
        titles = []
        for child in self.children:
            titles.append(child.selected_button.name)
            
        titles.reverse()
        return titles