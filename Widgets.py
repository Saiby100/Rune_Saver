from kivymd.uix.button import MDFloatingActionButton, MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.list import OneLineIconListItem, IconRightWidget
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.tooltip import MDTooltip
from kivy.properties import StringProperty, ObjectProperty, ListProperty
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.behaviors import HoverBehavior
from kivy.utils import get_color_from_hex
from kivymd.uix.list import OneLineAvatarIconListItem, OneLineListItem
from kivy.metrics import dp
from kivy.uix.recycleview.views import RecycleDataViewBehavior

items = ['Abyssal Mask', 'Anathema\'s Chains', 'Archangel\'s Staff',
         'Ardent Censer', 'Axiom Arc', "Banshee's Veil", 'Berserker\'s Greaves',
         'Black Cleaver', 'Black Mist Scythe', 'Blade of the Ruined Ki', 'Bloodthirster',
         'Boots of Swiftness', 'Bulwark of the Mountai', 'Chempunk Chainsword',
         'Chemtech Putrifier', 'Cosmic Drive', 'Crown of the Shattered Quee',
         'dark seal', 'Dead Man\'s Plate', 'Death\'s Dance', 'Demonic Embrace',
         'Divine Sunderer', 'Duskblade of Draktharr', 'Eclipse', 'Edge of Night',
         'Essence Reaver', 'Evenshroud', 'Everfrost', 'Fimbulwinter', 'Force of Nature',
         'Frostfire Gauntlet', 'Frozen Heart', 'Galeforce', 'Gargoyle Stoneplate', 'Goredrinker',
         'Guardian Angel', 'Guinsoo\'s Rageblade', 'hailblade', 'Hextech Rocketbelt', 'Horizon Focus',
         'Hullbreaker', 'Immortal Shieldbow', 'Imperial Mandate', 'Infinity Edge', 'Ionian Boots of Lucidity',
         "Knight's Vow", 'Kraken Slayer', "Liandry's Anguish", 'Lich Bane', 'Locket of the Iron Solari',
         "Lord Dominik's Regards", 'Lost Chapter', 'Luden\'s Tempest', 'Manamune', 'Maw of Malmortius',
         "Mejai's Soulstealer", 'Mercurial Scimitar', "Mikael's Blessi", 'Mobility Boots', 'Moonstone Renewer',
         'Morellonomico', 'Mortal Reminder', 'Muramana', "Nashor's Tooth", 'Navori Quickblades',
         'Night Harvester', 'Pauldrons of Whiterock', 'Phantom Dancer', 'Plated Steelcaps', "Prowler's Claw",
         "Rabadon's Deathca", "Randuin's Ome", 'Rapid Firecanno', 'Ravenous Hydra', 'Redemptio', 'Riftmaker',
         "Runaan's Hurricane", "Rylai's Crystal Scepter", "Seraph's Embrace", "Serpent's Fa", "Serylda's Grudge",
         'Shadowflame', 'Shard of True Ice', "Shurelya's Battleso", 'Silvermere Daw', "Sorcerer's Shoes",
         'Spirit Visage', 'Staff of Flowing Water', "Sterak's Gage", 'Stormrazor', 'Stridebreaker',
         'Sunfire Aegis', 'The Collector', 'Thornmail', 'Titanic Hydra', 'Trinity Force', 'Turbo Chemtank',
         'Umbral Glaive', 'Vigilant Wardstone', 'void staff', "Warmog's Armor", "Winter's Approach", "Wit's End",
         "Youmuu's Ghostblade", "Zeke's Convergence", "Zhonya's Hourglass"
         ]


titles = {'domination': ['Keystones', 'Malice', 'Tracking', 'Hunter'],
          'precision': ['Keystones', 'Heroism', 'Legend', 'Combat'],
          'inspiration': ['Keystones', 'Contraptions', 'Tomorrow', 'Beyond'],
          'resolve': ['Keystones', 'Strength', 'Resistance', 'Vitality'],
          'sorcery': ['Keystones', 'Artifact', 'Excellence', 'Power']
          }

runes = {'domination': {'Keystones': ['electrocute', 'predator', 'dark-harvest', 'hail-of-blades'],
                        'Malice': ['cheap-shot', 'taste-of-blood', 'sudden-impact'],
                        'Tracking': ['zombie-ward', 'ghost-poro', 'eyeball-collection'],
                        'Hunter': ['treasure-hunter', 'ingenious-hunter', 'relentless-hunter', 'ultimate-hunter']},

         'precision': {'Keystones': ['press-the-attack', 'lethal-tempo', 'fleet-footwork', 'conqueror'],
                       'Heroism': ['overheal', 'triumph', 'presence-of-mind'],
                       'Legend': ['legend-alacrity', 'legend-tenacity', 'legend-bloodline'],
                       'Combat': ['coup-de-grace', 'cut-down', 'last-stand']},

         'inspiration': {'Keystones': ['glacial-augment', 'unsealed-spellbook', 'first-strike'],
                         'Contraptions': ['hextech-flashtraption', 'magical-footwear', 'perfect-timing'],
                         'Tomorrow': ['future\'s-market', 'minion-dematerializer', 'biscuit-delivery'],
                         'Beyond': ['cosmic-insight', 'approach-velocity', 'time-warp-tonic']},

         'resolve': {'Keystones': ['grasp-of-the-undying', 'aftershock', 'guardian'],
                     'Strength': ['demolish', 'font-of-life', 'shield-bash'],
                     'Resistance': ['conditioning', 'second-wind', 'bone-plating'],
                     'Vitality': ['overgrowth', 'revitalize', 'unflinching']},

         'sorcery': {'Keystones': ['summon-aery', 'arcane-comet', 'phase-rush'],
                     'Artifact': ['nullifying-orb', 'manaflow-band', 'nimbus-cloak'],
                     'Excellence': ['transcendence', 'celerity', 'absolute-focus'],
                     'Power': ['scorch', 'waterwalking', 'gathering-storm']}
         }

secondary_runes = {'domination': ['cheap-shot', 'taste-of-blood', 'sudden-impact', 'zombie-ward', 'ghost-poro',
                                  'eyeball-collection', 'treasure-hunter', 'ingenious-hunter', 'relentless-hunter',
                                  'ultimate-hunter'],
                   'precision': ['overheal', 'triumph', 'presence-of-mind', 'legend-alacrity', 'legend-tenacity',
                                 'legend-bloodline', 'coup-de-grace', 'cut-down', 'last-stand'],
                   'inspiration': ['hextech-flashtraption', 'magical-footwear', 'perfect-timing', 'future\'s-market',
                                   'minion-dematerializer', 'biscuit-delivery', 'cosmic-insight', 'approach-velocity',
                                   'time-warp-tonic'],
                   'resolve': ['demolish', 'font-of-life', 'shield-bash', 'conditioning', 'second-wind',
                               'bone-plating', 'overgrowth', 'revitalize', 'unflinching'],
                   'sorcery': ['nullifying-orb', 'manaflow-band', 'nimbus-cloak', 'transcendence', 'celerity',
                               'absolute-focus', 'scorch', 'waterwalking', 'gathering-storm']
                   }

class ToolTipIconButton(MDIconButton, MDTooltip): 
    '''Icon Button with tooltip'''
    pass

class CustomOneLineListItem(OneLineListItem, HoverBehavior):
    '''OneLineListItem with hover feature'''
    def on_enter(self):
        self.app = MDApp.get_running_app()
        self.text_color = self.app.theme_cls.primary_color

    def on_leave(self):
        self.text_color = self.app.theme_cls.text_color

class CustomIconListItem(OneLineIconListItem, HoverBehavior):
    '''A OneLineIconListItem with hoverbehaviour'''
    icon = StringProperty()

    def on_enter(self):
        self.app = MDApp.get_running_app()
        self.text_color = self.app.theme_cls.primary_color

    def on_leave(self): 
        self.text_color = self.app.theme_cls.text_color

class NavItem(CustomIconListItem):
    '''Navigation items in navigation barused on Home pages (Profile Rune Library, Match History)'''
    def on_enter(self):
        self.app = MDApp.get_running_app()
        if self.text_color != self.app.theme_cls.primary_color:
            self.text_color = self.app.theme_cls.primary_light

    def on_leave(self):
        if self.text_color != self.app.theme_cls.primary_color:
            self.text_color = self.app.theme_cls.text_color


class Card(MDCard, HoverBehavior):
    text = StringProperty()
    source = StringProperty()
    '''Card used on champ select page'''
    def build_rune(self):
        screen = self.parent.parent.parent.parent #Refereces champ-select page
        screen.build_rune(self.text)

    def on_enter(self):
        self.app = MDApp.get_running_app()
        self.md_bg_color = self.app.theme_cls.primary_dark
    
    def on_leave(self):
        self.md_bg_color = self.app.theme_cls.bg_light

class RuneCard(MDCard):
    '''Card used on view Rune Page'''
    source = StringProperty()
    txt = StringProperty()

    def view_attribute(self):
        screen = self.parent.parent.parent.parent.parent.parent.parent.parent #References the ViewRune page
        screen.view_attribute(self.txt.lower())

class ItemCard(RuneCard):
    '''Card that will be used for creating builds (TODO)'''
    def __init__(self, src, text=None):
        super().__init__(src, text)
        self.size_hint = (None, None)



class FloatingButton(MDFloatingActionButton, MDTooltip):
    pass

class CustomIconRightWidget(IconRightWidget):
    '''Icon that contains an instance variable pointing to the rune that it is on'''
    rune = ObjectProperty()

class CustomIconAvatarListItem(OneLineAvatarIconListItem, HoverBehavior):
    text = StringProperty()
    source = StringProperty()

    def on_enter(self):
        self.app = MDApp.get_running_app()
        self.bg_color = self.app.theme_cls.bg_light

        self.right_icon = CustomIconRightWidget(icon='dots-vertical',
                                                rune=self)
        self.right_icon.bind(on_release=self.open_drop_menu)

        self.add_widget(self.right_icon)
    
    def on_leave(self):
        self.bg_color = self.app.theme_cls.bg_normal
        self.children[0].remove_widget(self.right_icon)

class Rune(CustomIconAvatarListItem):
    def __init__(self, **kwargs):
        self.build = []
        self.champ, self.name, self.main, self.key, self.slot1, self.slot2, \
        self.slot3, self.secondary, self.slot_1, self.slot_2 = kwargs['row']
        super().__init__(text=self.name, 
                         source=f'icons/champ_icons/{self.champ}.png')

    def attributes(self):
        return [self.main, self.key, self.slot1, self.slot2, self.slot3, self.secondary, self.slot_1, self.slot_2]

    def edit(self, row):
        self.champ, self.name, self.main, self.key, self.slot1, self.slot2, \
        self.slot3, self.secondary, self.slot_1, self.slot_2 = row

        self.text = self.name

    def open_drop_menu(self, instance):
        '''Opens the drop menu on the library page'''
        screen = self.parent.parent.parent.parent.parent #References library screen
        screen.rune_drop_menu.caller = instance
        screen.rune_drop_menu.open()

    def select_rune(self):
        '''Called when Rune list item is pressed'''
        self.screen = self.parent.parent.parent.parent.parent #References library screen
        self.screen.view_rune(self)

    '''TODO: Add feature for adding item builds for a rune'''
    def add_build(self):
        pass

class SavedRunes: 
    '''Manages all the saved runes in an account'''
    def __init__(self, account_file):
        self.runes = []
        for line in account_file:
            self.runes.append(Rune(row=line))

    def add_new_rune(self, new_rune):
        '''Adds a new rune in alphabetical order by champion name.
           Returns the index of the rune in the saved runes array'''
        for i, rune in enumerate(self.runes):
            if new_rune.champ <= rune.champ:
                self.runes.insert(i, new_rune)
                return i
        self.runes.append(new_rune)
        return len(self.runes) -1

    def delete_rune(self, rune):
        '''Removes a rune from the stored runes'''
        self.runes.remove(rune)

    def to_array(self):
        '''Returns all runes in a 2D array format'''
        array = []
        for rune in self.runes:
            temp_arr = [rune.champ, rune.name]
            temp_arr.extend(rune.attributes())
            array.append(temp_arr)
        return array

    def change_account(self, account_file):
        '''Clears the current stored runes and reads in a new file with stored runes'''
        self.runes.clear()
        for line in account_file:
            self.runes.append(Rune(row=line))

    def rune_index(self, rune):
        '''Returns the index of a rune in the stored runes array'''
        return self.runes.index(rune)

class Tab(MDFloatLayout, MDTabsBase):
    pass
