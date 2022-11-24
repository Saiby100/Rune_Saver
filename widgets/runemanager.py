from .listitems import CustomIconAvatarListItem

class Rune(CustomIconAvatarListItem):
    '''
        This is a class for the Rune widgets on library page.
    '''
    def __init__(self, **kwargs):
        self.build = []
        self.champ, self.name, self.main, self.key, self.slot1, self.slot2, \
        self.slot3, self.secondary, self.slot_1, self.slot_2 = kwargs['row']
        super().__init__(text=self.name, 
                         source=f'icons/champ_icons/{self.champ}.png')

    def attributes(self):
        return [self.main, self.key, self.slot1, self.slot2, self.slot3, self.secondary, self.slot_1, self.slot_2]

    def edit(self, row):
        self.champ, self.name, self.main, self.key, self.slot1, self.slot2, \
        self.slot3, self.secondary, self.slot_1, self.slot_2 = row

        self.text = self.name

    def open_drop_menu(self, instance):
        '''
            Opens the drop menu on the library page.
        '''
        screen = self.parent.parent.parent.parent.parent #References library screen
        screen.rune_drop_menu.caller = instance
        screen.rune_drop_menu.open()

    def select_rune(self):
        '''
            Called when Rune list item is pressed
        '''
        #References library screen
        self.screen = self.parent.parent.parent.parent.parent 
        self.screen.view_rune(self)

    def add_build(self):
        '''
            TODO: Add feature for adding item builds for a rune.
        '''
        pass

class RuneManager: 
    '''
        This class manages saved runes for each profile..
    '''
    def __init__(self, rune_data):
        '''
            This takes the rune data (2D array) and
            initializes them to Rune objects, and adds them
            to an array.
        '''
        self.runes = []
        for line in rune_data:
            self.runes.append(Rune(row=line))

        self.size = len(self.runes)

    def add_new_rune(self, new_rune, low, high):
        '''
            Adds a new rune in alphabetical order by champion name.
            Returns the index of the rune in the saved runes array.
        '''
        while high - low >= 4: 
            mid = low + (high - 1) // 2

            if self.runes[mid].champ == new_rune.champ:
                self.runes.insert(mid, new_rune)
                self.size += 1
                return mid

            if self.runes[mid].champ > new_rune.champ: 
                high = mid - 1

            else: 
                low = mid + 1

        for i in range(low, high+1):
            if new_rune.champ <= self.runes[i].champ:
                self.runes.insert(i, new_rune) 
                self.size += 1
                return i
        
        self.runes.insert(self.size - 1, new_rune)
        return self.size - 1

    def delete_rune(self, rune):
        '''
            Removes a rune from the stored runes.
            size is reduced by 1.
        '''
        self.runes.remove(rune)
        self.size -= 1

    def to_array(self):
        '''
            Returns all runes in a 2D array format.
        '''
        array = []
        for rune in self.runes:
            temp_arr = [rune.champ, rune.name]
            temp_arr.extend(rune.attributes())
            array.append(temp_arr)
        return array

    def change_account(self, account_file):
        '''
            Clears the current stored runes and reads in a new 
            file with stored runes.
            Size is set to the length of self.runes array.
        '''
        self.runes.clear()
        for line in account_file:
            self.runes.append(Rune(row=line))

        self.size = len(self.runes)

    def rune_index(self, rune):
        '''
            Returns the index of a rune in the stored runes array.
        '''
        return self.runes.index(rune)
