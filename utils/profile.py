from riotwatcher import LolWatcher, ApiError
import csv
import os

champ_def = {
    'AurelionSol': 'aurelion sol',
    'DrMundo': 'dr. mundo',
    'JarvanIV': 'jarvan iv',
    'Leesin': 'lee sin',
    'MasterYi': 'master yi',
    'MissFortune': 'miss fortune',
    'MonkeyKing': 'wukong',
    'TahmKench': 'tahm kench',
    'TwistedFate': 'twisted fate',
    'XinZhao': 'xin zhao'
}

class Player:

    def __init__(self, name, region='euw1'):
        self.name = name
        self.region = region
        self.hasdata = False
        self.hashistory = False

    def add_data(self, array):
        '''
            Initializes the player details attributes for Player object.
        '''
        self.level = array[0].strip('\n')
        self.icon = array[1].strip('\n')
        self.tier = array[2].strip('\n')
        self.rank = array[3].strip('\n')
        self.wins = array[4].strip('\n')
        self.losses = array[5].strip('\n')

        self.champ1 = (array[6].strip('\n'), array[7].strip('\n'))
        self.champ2 = (array[8].strip('\n'), array[9].strip('\n'))
        self.champ3 = (array[10].strip('\n'), array[11].strip('\n'))

        self.hasdata = True

    def add_match_history(self, array):
        '''
            Initializes the player match history attributes.
        '''
        self.matches = []
        for match in array:
            self.matches.append(
                {
                    'Name': match[0],
                    'Champion': match[1],
                    'Level': match[2],
                    'KDA': match[3],
                    'Farm': match[4],
                    'Won': match[5],
                    'Items': match[6:]
                }
            )
        self.hashistory = True

    def matches_to_array(self):
        '''
            Returns the player match history as a 2D array.
        '''
        array = []
        for match in self.matches:
            temp = [
                match['Name'],
                match['Champion'],
                match['Level'],
                match['KDA'],
                match['Farm'],
                match['Won']
            ]
            temp.extend(match['Items'])

            array.append(temp)

        return array

    def data_to_array(self):
        '''
            Returns the player data as an array.
        '''
        return [
            self.level+'\n',
            self.icon+'\n',
            self.tier+'\n',
            self.rank+'\n',
            self.wins+'\n',
            self.losses+'\n',
            self.champ1[0]+'\n',
            self.champ1[1]+'\n',
            self.champ2[0]+'\n',
            self.champ2[1]+'\n',
            self.champ3[0]+'\n',
            self.champ3[1]+'\n'
        ]

    def icon_src(self):
        if os.path.isfile(f'icons/profileicon/{self.icon}.png'):
            return f'icons/profileicon/{self.icon}.png'
        return 'icons/profileicon/none.png'

    def rank_emblem(self):
        return f'icons/tiers/Emblem_{self.tier.capitalize()}.png'

    def champ1_img(self):
        if os.path.isfile(f'icons/champ_images/{self.champ1[0].lower()}.png'):
            return f'icons/champ_images/{self.champ1[0].lower()}.png'
        return 'icons/profileicon/none.png'

    def champ2_img(self):
        if os.path.isfile(f'icons/champ_images/{self.champ2[0].lower()}.png'):
            return f'icons/champ_images/{self.champ2[0].lower()}.png'
        return 'icons/profileicon/none.png'

    def champ3_img(self):
        if os.path.isfile(f'icons/champ_images/{self.champ3[0].lower()}.png'):
            return f'icons/champ_images/{self.champ3[0].lower()}.png'
        return 'icons/profileicon/none.png'

    def show(self):
        '''
            FOR DEBUGGING
        '''
        print(
            self.level+'\n' +
            self.icon+'\n' +
            self.tier+'\n' +
            self.rank+'\n' +
            self.wins+'\n' +
            self.losses+'\n' +
            self.champ1[0]+'\n' +
            self.champ1[1]+'\n' +
            self.champ2[0]+'\n' +
            self.champ2[1]+'\n' +
            self.champ3[0]+'\n' +
            self.champ3[1]
        )

        for match in self.matches_to_array():
            print(match)


class Profile:
    '''
        Class for managing profiles.
    '''

    def __init__(self, name=None, apikey=None):
        '''
            This initializes the player region, data, name, api_key and path.        
        '''
        self.name = name
        self.region = 'euw1'
        self.api_key = apikey
        self.player = Player(name)

        self.rune_data_path = f'accounts/runes/{self.name}.csv'
        self.player_data_path = f'accounts/data/{self.name}.txt'
        self.match_data_path = f'accounts/data/{self.name}_matches.csv'

        self.get_local_player_data()
        self.get_local_match_data()

    def key_is_valid(self, api_key):
        '''
            Returns True if the api_key is valid, False otherwise.
            If api_key is None, saved api_key is checked.
        '''
        if api_key is None:
            api_key = self.api_key

        try:
            self.watcher = LolWatcher(api_key)
            self.profile = self.watcher.summoner.by_name(
                self.region, self.name)
            self.api_key = api_key

            return True

        except ApiError:
            return False

    def get_local_player_data(self):
        '''
            Fetches locally saved data on the player.
        '''
        if f'{self.name}.txt' not in self.files('txt'):
            return False

        with open(f'accounts/data/{self.name}.txt', 'r') as file:

            lines = file.readlines()
            self.player.add_data(lines)

        return True

    def get_local_match_data(self):
        '''
            Fetches local match history data.
        '''
        if not os.path.isfile(self.match_data_path):
            return

        with open(self.match_data_path) as file:
            reader = csv.reader(file)
            self.player.add_match_history(list(reader))
            return

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
            # Delete current profile
            os.remove(self.rune_data_path)

            try:
                os.remove(self.player_data_path)

            except FileNotFoundError:
                # No local data on player exists.
                pass

            accounts = self.files('csv')

            self.set_current(accounts[0].strip('.csv'))

        else:
            # Delete specified profile
            os.remove(f'accounts/runes/{name}.csv')
            os.remove(f'accounts/data/{name}.txt')

        return True

    def save(self, runes):
        '''
            Saves all the data to the profile's file.
        '''
        with open(self.rune_data_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(runes)

        with open('resources/config.txt', 'w') as file:
            file.write(self.name+'\n'+self.api_key)

        # Player data doesn't need to save.
        if not self.player.hasdata:
            return

        with open(self.player_data_path, 'w') as file:
            file.writelines(self.player.data_to_array())

        self.save_match_data()

    def save_match_data(self):
        '''
            Saves match data to a file.
        '''
        if not self.player.hashistory:
            return

        with open(self.match_data_path, 'w', newline='') as file:
            writer = csv.writer(file)
            for match in self.player.matches_to_array():
                writer.writerow(match)

    def rename(self, new_name):
        '''
            Renames the current profile. 
            Returns true if renaming successful, false otherwise.
        '''
        runes_path = f'accounts/runes/{new_name}.csv'
        data_path = f'accounts/data/{new_name}.txt'
        match_path = f'accounts/data/{new_name}.csv'
        try:
            os.rename(self.rune_data_path, runes_path)
            os.rename(self.player_data_path, data_path)
            os.rename(self.match_data_path, match_path)
            self.set_current(new_name)
            return True

        except FileExistsError:
            return False

    def set_current(self, account_name):
        '''
            Sets the profile object to the specified name.
        '''
        if f'{account_name}.csv' in self.files('csv'):
            self.name = account_name
            self.rune_data_path = f'accounts/runes/{account_name}.csv'
            self.player_data_path = f'accounts/data/{account_name}.txt'
            self.match_data_path = f'accounts/data/{account_name}_matches.csv'

            self.player = Player(account_name)
            self.get_local_player_data()
            self.get_local_match_data()

            # Alter config file here
            with open('resources/config.txt', 'w') as file:
                file.write(self.name+'\n')
                file.write(self.api_key+'\n')

    def create_new_profile(self, name):
        '''
            Creates new account by the specified name. 
            Returns true if creation successful, false otherwise.
        '''
        if len(self.get_all_profiles()) >= 4:
            # Too many accounts
            return False
        try:
            open(f'accounts/runes/{name}.csv', 'x')
            return True

        except FileExistsError:
            return False

    def files(self, extension):
        '''
            Returns all files with the specified extension in the accounts 
            directory as an array.
        '''
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
                if self.profile['summonerLevel'] < 30:
                    return False

                self.stats = self.watcher.league.by_summoner(
                    self.region, self.profile['id'])[0]

                data = [
                    str(self.profile['summonerLevel']),
                    str(self.profile['profileIconId']),
                    self.stats['tier'],
                    self.stats['rank'],
                    str(self.stats['wins']),
                    str(self.stats['losses'])
                ]
                data.extend(self.get_champ_masteries())

                self.player.add_data(data)

                self.api_key = api_key
                return True

            except ValueError:
                return False

    def get_champ_masteries(self):
        '''
            Gets the top 3 champ masteries for the current player.
            Returns an array of tuples with the champ and its corresponding
            mastery level.
        '''
        id_arr = self.watcher.champion_mastery.by_summoner(
            self.region, self.profile['id'])
        latest = self.watcher.data_dragon.versions_for_region(self.region)[
            'n']['champion']
        static_champ_list = self.watcher.data_dragon.champions(
            latest, False, 'en_US')

        champ_dict = {}
        for key in static_champ_list['data']:
            row = static_champ_list['data'][key]
            champ_dict[row['key']] = row['id']

        champ_arr = []
        for i in range(3):
            champ_arr.append(champ_dict[str(id_arr[i]['championId'])])
            champ_arr.append(str(id_arr[i]['championLevel']))
        return champ_arr

    def get_match_history(self, max=10):
        '''
            Returns last five matches played
        '''
        if not self.key_is_valid(None):
            return False

        my_region = self.region
        player_puuid = self.watcher.summoner.by_name(
            my_region, self.name)["puuid"]

        my_matches = self.watcher.match.matchlist_by_puuid(
            my_region, player_puuid)

        history = []
        MAX = max
        for x, match_id in enumerate(my_matches):
            if (x >= MAX):
                break
            history.append(self.watcher.match.by_id(my_region, match_id))

        matches = []
        for match in history:
            for details in match["info"]["participants"]:
                if details["summonerName"] == self.name:
                    match_row = []
                    items = []

                    for i in range(7):
                        items.append(str(details["item"+str(i)]))
                    match_row.append(details['summonerName'])

                    if details['championName'] in champ_def.keys():
                        match_row.append(
                            champ_def[details["championName"]]
                            )
                    else:
                        match_row.append(details["championName"])
                    match_row.append(details['champLevel'])

                    try:
                        kills = details["challenges"]["takedowns"] - \
                            details["assists"]
                    except KeyError:
                        kills = details["kills"]

                    deaths = details["deaths"]
                    assists = details["assists"]

                    match_row.append(f"{kills}/{deaths}/{assists}")
                    match_row.append(details['totalMinionsKilled'])
                    match_row.append(details['win'])
                    match_row.extend(items)

                    matches.append(match_row)

        self.player.add_match_history(matches)


if __name__ == '__main__':
    profile = Profile('Saiby100', 'RGAPI-4d6ed83a-199d-461a-aa36-697685146214')
    profile.player.show()
