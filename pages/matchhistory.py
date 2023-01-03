from kivy.uix.screenmanager import Screen
from utils import config
from widgets.listitems import MatchListItem
from kivymd.uix.label import MDLabel


class MatchHistory(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        if config.profile.player.hashistory:
            for player in config.profile.player.matches:
                list_item = MatchListItem(
                    champ=player['Champion'],
                    kda=player['KDA'],
                    won=player['Won']=='True',
                    farm=player['Farm'],
                    items=player['Items']
                )

                self.ids.layout.add_widget(list_item)

        else:
            self.ids.layout.add_widget(MDLabel(text='Match History'))

    def refresh_player_matches(self):
        if not config.profile.get_match_history():
            return

        self.ids.layout.clear_widgets()

        for player in config.profile.player.matches:
            list_item = MatchListItem(
                champ=player['Champion'],
                kda=player['KDA'],
                won=player['Won']=='True',
                farm=player['Farm'],
                items=player['Items']
            )

            self.ids.layout.add_widget(list_item)
