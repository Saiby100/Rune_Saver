import csv
import os

class Profile:
    '''Class for managing profiles.'''
    def __init__(self):        
        with open('resources/config.txt', 'r') as file:
            self.name = file.readline()
        self.path = f'accounts/{self.name}.csv'

    def profiles(self):
        '''Returns all the existing profiles.'''
        return os.listdir('accounts')

    def name(self):
        '''Gets the name of the current profile.'''
        return self.name

    def data(self):
        '''Gets the rune data of the current profile.'''
        array = []
        with open(self.path, 'r') as file:
            reader = csv.reader(file)
            for line in reader:
                array.append(line)
            return array

    def delete(self):
        '''Deletes the current profile. Returns true if deletion successful, false otherwise.'''
        accounts = os.listdir('accounts')
        if len(accounts) <= 1:
            return False

        os.remove(self.path)
        accounts = os.listdir('accounts')
        self.name = accounts[0].strip('.csv')
        self.path = f'accounts/{accounts[0]}'

        with open('resources/config.txt', 'w') as file:
            file.write(self.name)
        return True

    def save(self, runes):
        '''Saves all the data to the profile's file.'''
        with open(self.path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(runes)

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

        with open('resources/config.txt', 'w') as file:
            file.write(self.name)

    def add_new(self, name):
        '''Creates new account by the specified name. Returns true if creation successful, false otherwise.'''
        if len(self.profiles()) >= 4:
            return False
        try:
            open(f'accounts/{name}.csv', 'x')
            # self.set_current(name)
            return True
        except FileExistsError:
            return False



