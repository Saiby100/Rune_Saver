from kivymd.uix.button import MDIconButton, MDFloatingActionButton
from kivymd.uix.card import MDCardSwipe, MDCardSwipeFrontBox, MDCardSwipeLayerBox, MDCard
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivy.uix.image import Image
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.list import ImageLeftWidget, OneLineAvatarListItem, OneLineIconListItem, IconLeftWidget
from kivymd.uix.label import MDLabel
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.tooltip import MDTooltip

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

class SwipeToDeleteItem(MDCardSwipe):
    def __init__(self, text, img_source):
        super().__init__()
        self.size_hint_y = None
        self.icon = MDIconButton(icon='trash-can',
                                 pos_hint={'center_y': .5})
        self.list_item = OneLineAvatarListItem(text=text)
        self.img = ImageLeftWidget()
        self.img.source=img_source
        self.list_item.add_widget(self.img)
        self.front_layer = MDCardSwipeFrontBox()
        self.front_layer.add_widget(self.list_item)

        self.back_layer = MDCardSwipeLayerBox()
        self.back_layer.add_widget(self.icon)

        self.add_widget(self.back_layer)
        self.add_widget(self.front_layer)
        self.height = self.list_item.height

    def bind_back(self, **kwargs):
        self.icon.bind(**kwargs)

    def bind_front(self, **kwargs):
        self.list_item.bind(**kwargs)


class FloatingButton(MDFloatingActionButton, MDTooltip):
    pass

class SavedRunes: 
    def __init__(self, account_data):
        self.runes = []
        for line in account_data:
            self.runes.append(Rune(line))

    def add_new_rune(self, new_rune):
        for i, rune in enumerate(self.runes):
            if new_rune.champ <= rune.champ:
                self.runes.insert(i, new_rune)
                return
        self.runes.append(new_rune)

    def delete_rune(self, rune):
        self.runes.remove(rune)

    def to_array(self):
        array = []
        for rune in self.runes:
            temp_arr = [rune.champ, rune.name]
            temp_arr.extend(rune.attributes())
            array.append(temp_arr)
        return array

    def change_account(self, account_data):
        self.runes.clear()
        for line in account_data:
            self.runes.append(Rune(line))

    def rune_index(self, rune):
        return self.runes.index(rune)

class IconListItem(OneLineIconListItem):
    def __init__(self, text, icon):
        super().__init__()
        self.text = text
        self.icon = IconLeftWidget(icon=icon)
        self.add_widget(self.icon)

class Card(MDCard):
    def __init__(self, src, txt):
        super().__init__()
        self.orientation = 'vertical'
        self.size_hint = (None, None)
        self.radius = '25dp'

        self.add_widget(Image(source=src,
                              allow_stretch=True,
                              keep_ratio=False,
                              size_hint=(None,None),
                              size=(self.size[0], self.size[1]-20)))
        self.add_widget(MDLabel(text=txt,
                                font_style='Caption',
                                halign='center'))

class RuneCard(MDCard): 
    def __init__(self, src, text=None):
        super().__init__()
        self.orientation = 'vertical'
        self.padding = '5dp'
        self.spacing = '5dp'
        self.radius = '25dp'

        self.add_widget(Image(source=src,
                              allow_stretch=True))

        if text is not None:
            self.add_widget(MDLabel(text=text,
                                    halign='center',
                                    font_style='Caption'))

class ItemCard(RuneCard):
    def __init__(self, src, text=None):
        super().__init__(src, text)
        self.size_hint = (None, None)


class Rune(SwipeToDeleteItem):
    def __init__(self, row):
        self.build = []
        self.champ, self.name, self.main, self.key, self.slot1, self.slot2, \
        self.slot3, self.secondary, self.slot_1, self.slot_2 = row
        super().__init__(self.name, f'icons/champ_icons/{self.champ}.png')

    def attributes(self):
        return [self.main, self.key, self.slot1, self.slot2, self.slot3, self.secondary, self.slot_1, self.slot_2]

    def edit(self, row):
        self.champ, self.name, self.main, self.key, self.slot1, self.slot2, \
        self.slot3, self.secondary, self.slot_1, self.slot_2 = row
        self.list_item.text = self.name

    def add_build(self):
        pass

class Tab(MDFloatLayout, MDTabsBase):
    pass


class PanelManager():
    def __init__(self, primary_titles, secondary_titles):
        self.primary_panels = []
        self.secondary_panels = []
        array = []
        array.extend(runes.keys())
        #Adds primary panels
        for i, title in enumerate(primary_titles):
            if i == 0:
                self.primary_panels.append(ExpansionPanel(title, self, Content(array)))
            else:
                self.primary_panels.append(ExpansionPanel(title, self, Content()))

        #Adds Secondary panels
        for i, title in enumerate(secondary_titles):
            if i == 0:
                self.secondary_panels.append(ExpansionPanel(title, self, Content(array)))
            else:
                self.secondary_panels.append(ExpansionPanel(title, self, Content()))

    def primary_panels(self):
        return self.primary_panels

    def secondary_panels(self):
        return self.secondary_panels

    def update_panels(self, title, panel):
        panel_titles = []
        panel_titles.extend(runes[title.lower()].keys())

        if panel in self.primary_panels:
            for i in range(1, len(self.primary_panels)):
                current_panel = self.primary_panels[i]
                current_panel.change(runes[title.lower()][panel_titles[i-1]])
                current_panel.change_title(panel_titles[i-1].title())

        else:
            for i in range(1, len(self.secondary_panels)):
                current_panel = self.secondary_panels[i]
                current_panel.change(secondary_runes[title.lower()])
                current_panel.change_title(f'Slot {i}')

    def reset_panels(self):
        array = ['Primary', 'Keystones', 'Slot 1', 'Slot 2', 'Slot 3', 'Secondary', 'Slot 1', 'Slot 2']
        for i, panel in enumerate(self.primary_panels):
            panel.reset(array[i])

        for i, panel in enumerate(self.secondary_panels):
            panel.reset(array[i+5])

class ExpansionPanel(MDExpansionPanel):
    def __init__(self, title, panel_box, content=None):
        self.panel_cls = MDExpansionPanelOneLine(text=title)
        self.panel_cls.font_style = 'Body2'
        self.panel_box = panel_box
        if content is not None:
            self.content = content
        super().__init__()

    def text(self):
        return self.panel_cls.text

    def change_title(self, new_title):
        array = []
        array.extend(runes.keys())
        #If its a header title, then all panel contents below it changes
        if new_title.lower() in array:
            self.panel_box.update_panels(new_title, self)
        self.panel_cls.text = new_title

    def reset(self, title):
        if self.panel_cls.text not in runes.keys():
            self.content = Content()
        self.panel_cls.text = title

    def change(self, array):
        if self.content is not None:
            self.content.change_content(array)
            return
        self.content = Content(array)

class Content(MDBoxLayout):
    def __init__(self, rune_headers=None):
        super().__init__()
        self.adaptive_height = True
        self.orientation = 'vertical'

        if rune_headers is not None:
            for rh in rune_headers:
                self.add_widget(ListItem(rh.title(), f'icons/runes/{rh}.png'))

    def change_content(self, rune_headers):
        self.clear_widgets()
        for rh in rune_headers:
            self.add_widget(ListItem(rh.title(), f'icons/runes/{rh}.png'))

class ListItem(OneLineAvatarListItem):
    def __init__(self, text, image_source):
        super().__init__()

        self.text = text
        self.source = image_source

        self.image = ImageLeftWidget()
        self.image.source = self.source
        self.add_widget(self.image)

        self.bind(on_release=self.update_panel_title)

    def update_panel_title(self, instance):
        self.parent.parent.change_title(self.text)