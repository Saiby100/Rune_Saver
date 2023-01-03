from .profile import Profile
from widgets.runemanager import RuneManager
from kivy.uix.screenmanager import ScreenManager, NoTransition


def init():
    '''
        This initializes the global variables.
    '''
    global profile, saved_runes, sm, items, titles, runes, secondary_runes

    with open('resources/config.txt', 'r') as file:
        profile = Profile(
            file.readline().strip('\n'),
            file.readline().strip('\n')
        )
    saved_runes = RuneManager(profile.get_rune_data())
    sm = ScreenManager(transition=NoTransition())

    champ_definitions = {
        'aurelionsol': 'aurelion sol',
        'drmundo': 'dr. mundo',
        'jarvaniv': 'jarvan iv',
        'leesin': 'lee sin',
        'masteryi': 'master yi',
        'missfortune': 'miss fortune',
        'monkeyking': 'wukong',
        'tahmkench': 'tahm kench',
        'twistedfate': 'twisted fate',
        'xinzhao': 'xin zhao'
    }

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
