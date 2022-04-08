
main_runes = ['domination','precision','inspiration','resolve','sorcery']

titles = {'domination': ['Keystones','Malice','Tracking','Hunter'],
          'precision': ['Keystones','Heroism','Legend','Combat'],
          'inspiration': ['Keystones','Contraptions','Tomorrow','Beyond'],
          'resolve': ['Keystones','Strength','Resistance','Vitality'],
          'sorcery': ['Keystones','Artifact','Excellence','Power']}

runes =  {'domination': {'Keystones': ['electrocute','predator','dark-harvest','hail-of-blades'],
                        'Malice': ['cheap-shot','taste-of-blood','sudden-impact'],
                        'Tracking': ['zombie-ward','ghost-poro','eyeball-collection'],
                        'Hunter': ['ravenous-hunter','ingenious-hunter','relentless-hunter','ultimate-hunter']},

         'precision': {'Keystones': ['press-the-attack','lethal-tempo','fleet-footwork','conqueror'],
                        'Heroism': ['overheal','triumph','presence-of-mind'],
                        'Legend': ['legend-alacrity','legend-tenacity','legend-bloodline'],
                        'Combat': ['coup-de-grace','cut-down','last-stand']},

         'inspiration': {'Keystones': ['glacial-augment','unsealed-spellbook','first-strike'],
                        'Contraptions': ['hextech-flashtraption','magical-footwear','perfect-timing'],
                        'Tomorrow': ['future\'s-market','minion-dematerializer','biscuit-delivery'],
                        'Beyond': ['cosmic-insight','approach-velocity','time-warp-tonic']},

         'resolve': {'Keystones': ['grasp-of-the-undying','aftershock','guardian'],
                        'Strength': ['demolish','font-of-life','shield-bash'],
                        'Resistance': ['conditioning','second-wind','bone-plating'],
                        'Vitality': ['overgrowth','revitalize','unflinching']},

         'sorcery': {'Keystones': ['summon-aery','arcane-comet','phase-rush'],
                        'Artifact': ['nullifying-orb','manaflow-band','nimbus-cloak'],
                        'Excellence': ['transcendence','celerity','absolute-focus'],
                        'Power': ['scorch','waterwalking','gathering-storm']}
         }
list = [3, 2, 1]
list2 = [0, -1, -2]
list.extend(list2)
print(list)
