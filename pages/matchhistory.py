from kivy.uix.screenmanager import Screen
from utils import config
from widgets.listitems import MatchListItem
from kivymd.uix.label import MDLabel


class MatchHistory(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        if config.profile.matches:
            for player in config.profile.matches:
                list_item = MatchListItem(
                    champ=player.champ,
                    kda=player.kda,
                    won=player.won,
                    farm=str(player.farm),
                    items=player.items
                )

                self.ids.layout.add_widget(list_item)
        
        else: 
            self.ids.layout.add_widget(MDLabel(text="Match History"))
    
    def refresh_player_matches(self):
        config.profile.get_match_history()
        if not config.profile.matches:
            return

        self.ids.layout.clear_widgets()

        for player in config.profile.get_match_history():
            list_item = MatchListItem(
                champ=player.champ,
                kda=player.kda,
                won=player.won,
                farm=str(player.farm),
                items=player.items
            )

            self.ids.layout.add_widget(list_item)