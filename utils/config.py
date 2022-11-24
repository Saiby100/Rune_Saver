from Profile import Profile
from widgets.runemanager import RuneManager
from kivy.uix.screenmanager import ScreenManager, NoTransition

def init():
    '''
        This initializes the global variables.
    '''
    global profile, saved_runes, sm, items, titles, runes, secondary_runes

    profile = Profile()
    saved_runes = RuneManager(profile.get_rune_data())
    sm = ScreenManager(transition=NoTransition())

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