from riotwatcher import LolWatcher, ApiError
import csv
import os

class Player:
    def __init__(self, dict):
        '''Defines each player in the match history array'''
        self.name = dict["Player Name"]
        self.champ_id = dict["Player Champion Id"]
        self.kda = dict["KDA"]
        self.farm = dict["Farm"]
        self.won = dict["Win"]

class Profile:
    '''Class for managing profiles.'''
    def __init__(self):
        self.region = 'euw1'
        self.player = {}
        self.has_local_data = False

        with open('resources/config.txt', 'r') as file:
            self.name = file.readline().strip('\n')
            self.api_key = file.readline().strip('\n')
        self.path = f'accounts/{self.name}.csv'    
        
        self.refresh_player_info()
    
    def get_player_info_from_file(self):
        '''Fetches last data saved on the player'''
        with open(f'accounts/{self.name}.txt', 'r') as file:
            array = ['level', 'icon', 'tier', 'rank', 'wins', 'losses', 'points']
            for i, line in enumerate(file):
                self.player[array[i]] = line.strip('\n')
                    
    def profiles(self):
        '''Returns all the existing profiles.'''
        return self.files('csv')

    def name(self):
        '''Gets the name of the current profile.'''
        return self.name

    def data(self):
        '''Gets the rune data of the current profile and returns it in a 2d array'''
        array = []
        with open(self.path, 'r') as file:
            reader = csv.reader(file)
            for line in reader:
                array.append(line)
            return array

    def delete(self):
        '''Deletes the current profile. Returns true if deletion successful, false otherwise.'''
        accounts = self.files('csv')
        if len(accounts) <= 1:
            return False

        os.remove(self.path)
        accounts = self.files('csv')

        self.set_current(accounts[0].strip('.csv'))
        return True

    def save(self, runes):
        '''Saves all the data to the profile's file.'''
        with open(self.path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(runes)
        
        if self.player['level'] is None: #Player data doesn't need to save.
            return

        player_keys = ['level', 'icon', 'tier', 'rank', 'wins', 'losses', 'points']
        
        with open(f'accounts/{self.name}.txt', 'w') as file:
            for key in player_keys:
                file.write(str(self.player[key])+'\n')

        with open('resources/config.txt', 'w') as file:
            file.write(self.name+'\n'+self.api_key)
        
    def rename(self, new_name):
        '''Renames the current profile. Returns true if renaming successful, false otherwise.'''
        path = f'accounts/{new_name}.csv'
        try:
            os.rename(self.path, path)
            self.set_current(new_name)
            return True

        except FileExistsError:
            return False

    def set_current(self, account_name):
        '''Sets the profile object to the specified name.'''
        self.name = account_name
        self.path = f'accounts/{account_name}.csv'
        self.refresh_player_info()

        with open('resources/config.txt', 'w') as file:
            file.write(self.name+'\n')
            file.write(self.api_key+'\n')

    def refresh_player_info(self):
        if f'{self.name}.txt' in self.files('txt'): 
            '''Previous data has been recorded on player'''
            self.get_player_info_from_file()
        else:
            '''No data on player exists'''
            self.reset_player()

    def add_new(self, name):
        '''Creates new account by the specified name. Returns true if creation successful, false otherwise.'''
        if len(self.profiles()) >= 4:
            return False
        try:
            open(f'accounts/{name}.csv', 'x')
            return True

        except FileExistsError:
            return False

    def files(self, extension):
        '''Returns all files with the specified extension in the accounts directory as an array'''
        files = [file for file in os.listdir('accounts')
                 if file.endswith('.'+extension)]

        return files
    
    def add_key(self, api_key):
        '''Collects player info. Returns true if successful, false otherwise.'''
        if api_key is None: 
            api_key = self.api_key
        try: 
            self.watcher = LolWatcher(api_key)
            self.profile = self.watcher.summoner.by_name(self.region, self.name)
            self.player['level'] = self.profile['summonerLevel']
            self.player['icon'] = self.profile['profileIconId']
        
            if self.player['level'] < 30:
                return False

            self.stats = self.watcher.league.by_summoner(self.region, self.profile['id'])[0]
            self.player['wins'] = self.stats['wins']
            self.player['losses'] = self.stats['losses']
            self.player['tier'] = self.stats['tier']
            self.player['rank'] = self.stats['rank']
            self.player['points'] = self.stats['leaguePoints']
            self.api_key = api_key
            return True

        except ApiError:
            return False
        except ValueError: 
            return False
    
    def reset_player(self):
        '''Sets player dictionary to defaults (None)'''
        attributes = ['level', 'icon', 'tier', 'rank', 'wins', 'losses', 'points']
        for attribute in attributes:
            self.player[attribute] = None

    def get_match_history(self, max=5):
        '''Returns last five matches played'''
        my_region = self.region
        player_puuid = self.watcher.summoner.by_name(my_region, self.name)["puuid"]

        my_matches = self.watcher.match.matchlist_by_puuid(my_region, player_puuid)

        history = []
        MAX = max
        for x, match_id in enumerate(my_matches):
            if (x >= MAX):
                break
            history.append(self.watcher.match.by_id(my_region, match_id))

        matches = []
        for match in history:
            match_data = []
            for details in match["info"]["participants"]:
                match_row = {}
                match_row["items"] = []

                match_row["Player Name"] = details["summonerName"]
                match_row["Player Champion Id"] = details["championName"]
                match_row["Level"] = details["champLevel"]

                for i in range(7):
                    match_row["items"].append(str(details["item"+str(i)]))

                try:
                    kills = details["challenges"]["takedowns"] - details["assists"]
                except KeyError:
                    kills = details["kills"] 

                deaths = details["deaths"]
                assists = details["assists"]
                
                match_row["KDA"] = f"{kills}/{deaths}/{assists}"
                match_row["Farm"] = details["totalMinionsKilled"]
                match_row["Win"] = details["win"]

                match_data.append(Player(match_row))

            matches.append(match_data)
        return matches
        
    
    

