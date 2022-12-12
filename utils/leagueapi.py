from riotwatcher import LolWatcher, ApiError


class LeageData:

    def __init__(self, name, region, api_key):
        self.name = name
        self.region = region

        self.watcher = LolWatcher(api_key)
        self.profile = self.watcher.summoner.by_name(region, name)
        self.api_key = api_key

    def profile_data(self):
        return self.profile

    def get_stats(self):
        return self.watcher.league.by_summoner(self.region, self.profile['id'])


if __name__ == '__main__':
    api = LeageData('Saiby100', 'euw1',
                    '12345678')
    data = api.get_stats()
    print(data)
