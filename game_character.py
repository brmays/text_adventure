import random

class Characters():
    number_of_enemies = 0
    character_dict = dict()

    def __init__(self, data):
        self.data = data
        self.character_dict = self.generate_characters()

    def generate_characters(self):
        character_dict = {}
        for name, data in self.data.items():
            this_character = Character(data)
            character_dict[name] = this_character
        return character_dict

class Character():

    def __init__(self, data):
        self.data = data

    def decrement_disposition(self):
        self.data['disposition'] = self.data['disposition'] - 2
        if self.data['disposition'] <= 0:
            self.data['is_enemy'] = True

    def get_condition(self):
        health = self.data['health']
        max_health = self.data['max_health']
        if health == max_health:
            return "untouched"
        elif health > max_health / 2:
            return "scuffed  "
        elif health < max_health * .25:
            return "reeling  "
        else:
            return "bloodied "

    # this can be a future feature. Need to tie the body to a room or it will be buggy
    def search_body(self):
        if self.data['health'] > 0:
            return None

    # For now, correct items increase disposition by one, add item disposition worth later
    def bribe(self, bribe_item):
        if bribe_item == self.data['trigger_item']:
            print(f"\n{self.name}: Maybe you're not as bad as everyone says you are")
            self.data['disposition'] = self.data['disposition'] + 1
        else:
            print("I don't want your trash.")
        if len(self.data['items']) > 0 and self.data['disposition'] >= 3:
            print(f"You can take this {self.data['items'][0]} I guess. Don't tell anyone I gave it to you though.")
            return self.data['items'][0]
        else:
            return "Nothing"
