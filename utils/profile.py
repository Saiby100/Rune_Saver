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
        '''
            This initializes the player region, data, name, api_key and path.        
        '''
        self.region = 'euw1'
        self.player_data = {}

        with open('resources/config.txt', 'r') as file:
            self.name = file.readline().strip('\n')
            self.api_key = file.readline().strip('\n')
        self.rune_data_path = f'accounts/runes/{self.name}.csv'    
        self.player_data_path = f'accounts/data/{self.name}.csv'    

        self.refresh_player_data()

    def key_is_valid(self, api_key):
        '''
            Returns True if the api_key is valid, False otherwise.
            If api_key is None, saved api_key is checked.
        '''
        if api_key is None: 
            api_key = self.api_key

        try:
            self.watcher = LolWatcher(api_key)
            self.profile = self.watcher.summoner.by_name(self.region, self.name)
            self.api_key = api_key

            return True

        except ApiError:
            return False
    
    def get_local_player_data(self):
        '''Fetches locally saved data on the player'''

        with open(f'accounts/data/{self.name}.txt', 'r') as file:
            array = ['level', 'icon', 'tier', 'rank', 'wins', 'losses', 'points']

            for i, line in enumerate(file):
                self.player_data[array[i]] = line.strip('\n')
    
                    
    def get_all_profiles(self, data=False):
        '''
            Returns all the existing profiles' rune data by default.
            If data is True, this returns all data files for all profiles.
        '''
        if data:
            return self.files('txt')

        return self.files('csv')

    def get_rune_data(self):
        '''
            Gets the rune data of the current profile and returns it in a 
            2d array.
        '''
        array = []
        with open(self.rune_data_path, 'r') as file:
            reader = csv.reader(file)
            for line in reader:
                array.append(line)
            return array

    def delete_profile(self, name=None):
        '''
            Deletes the specified/current profile. 
            Returns true if deletion successful, false otherwise.
        '''
        accounts = self.files('csv')
        if len(accounts) <= 1:
            return False

        if name is None:
            #Delete current profile
            os.remove(self.rune_data_path)

            try:
                os.remove(self.player_data_path)
            except FileNotFoundError:
                #No local data on player exists.
                pass

            accounts = self.files('csv')

            self.set_current(accounts[0].strip('.csv'))

        else: 
            #Delete specified profile
            os.remove(f'accounts/runes/{name}.csv')
            os.remove(f'accounts/data/{name}.txt')

        return True

    def save(self, runes):
        '''Saves all the data to the profile's file.'''
        with open(self.rune_data_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(runes)

        with open('resources/config.txt', 'w') as file:
            file.write(self.name+'\n'+self.api_key)
        
        if self.player_data['level'] is None: #Player data doesn't need to save.
            return

        player_keys = ['level', 'icon', 'tier', 'rank', 'wins', 'losses', 'points']
        
        with open(f'accounts/data/{self.name}.txt', 'w') as file:
            for key in player_keys:
                file.write(str(self.player_data[key])+'\n')
        
    def rename(self, new_name):
        '''
            Renames the current profile. 
            Returns true if renaming successful, false otherwise.
        '''

        runes_path = f'accounts/runes/{new_name}.csv'
        data_path = f'accounts/data/{new_name}.txt'
        try:
            os.rename(self.rune_data_path, runes_path)
            os.rename(self.player_data_path, data_path)
            self.set_current(new_name)
            return True

        except FileExistsError:
            return False

    def set_current(self, account_name):
        '''
            Sets the profile object to the specified name.
        '''
        if f'{account_name}.csv' in self.files('csv'):
            #Alter config file here
            self.name = account_name
            self.rune_data_path = f'accounts/runes/{account_name}.csv'
            self.player_data_path = f'accounts/data/{account_name}.txt'
            self.refresh_player_data()

            with open('resources/config.txt', 'w') as file:
                file.write(self.name+'\n')
                file.write(self.api_key+'\n')

    def refresh_player_data(self):
        '''
            Refreshes current player data to new player data.
            Used to set current profile to a different one.
        '''
        if self.key_is_valid(self.api_key):
            self.fetch_player_api_data(None)

        elif f'{self.name}.txt' in self.files('txt'):
            self.get_local_player_data()
        
        else:
            self.set_player_data_to_none()

    def create_new_profile(self, name):
        '''
            Creates new account by the specified name. 
            Returns true if creation successful, false otherwise.
        '''
        if len(self.get_all_profiles()) >= 4:
            #Too many accounts
            return False
        try:
            open(f'accounts/runes/{name}.csv', 'x')
            return True

        except FileExistsError:
            return False

    def files(self, extension):
        '''Returns all files with the specified extension in the accounts directory as an array'''
        if extension == 'txt':
            files = [file for file in os.listdir('accounts/data')
                    if file.endswith('.'+extension)]

        else:
            files = [file for file in os.listdir('accounts/runes')
                    if file.endswith('.'+extension)]

        return files
    
    def fetch_player_api_data(self, api_key):
        '''
            Collects player info. 
            Returns true if successful, false otherwise.
            If api key is none, this uses the saved api key.
            '''
        if api_key is None: 
            api_key = self.api_key

        if self.key_is_valid(api_key):
            try: 
                self.watcher = LolWatcher(api_key)
                self.profile = self.watcher.summoner.by_name(self.region, self.name)
                self.player_data['level'] = self.profile['summonerLevel']
                self.player_data['icon'] = self.profile['profileIconId']
            
                if self.player_data['level'] < 30:
                    return False

                self.stats = self.watcher.league.by_summoner(self.region, self.profile['id'])[0]
                self.player_data['wins'] = self.stats['wins']
                self.player_data['losses'] = self.stats['losses']
                self.player_data['tier'] = self.stats['tier']
                self.player_data['rank'] = self.stats['rank']
                self.player_data['points'] = self.stats['leaguePoints']
                self.api_key = api_key
                return True

            except ValueError: 
                return False
    
    def set_player_data_to_none(self):
        '''
            Sets player dictionary to defaults (None).
        '''
        attributes = ['level', 'icon', 'tier', 'rank', 'wins', 'losses', 'points']
        for attribute in attributes:
            self.player_data[attribute] = None

    def get_match_history(self, max=5):
        '''
            Returns last five matches played
        '''
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
        
    
if __name__ == '__main__':
    profile = Profile()
    with open('accounts/runes/Predator122.csv', 'r') as file:
        reader = csv.reader(file)
        for line in reader:
            print(line)
