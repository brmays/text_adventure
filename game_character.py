import random

class Character():
    number_of_enemies = 0
    character_dict = dict()

    def __init__(self, name, descriptors, experience_value, is_enemy, disposition, description, trigger_item, max_health, health, dexterity, equipment, weakness, items, conversation, pronouns):
        self.name = name
        self.descriptors = descriptors
        self.experience_value = experience_value
        self.is_enemy = is_enemy
        self.disposition = disposition
        self.description = description
        self.trigger_item = trigger_item
        self.max_health = max_health
        self.health = health
        self.dexterity = dexterity
        self.equipment = equipment
        self.weakness = weakness
        self.items = items
        self.conversation = conversation
        self.pronouns = pronouns
        Character.number_of_enemies = Character.number_of_enemies + is_enemy

    def decrement_disposition(self):
        self.disposition = self.disposition - 2
        if self.disposition <= 0:
            self.is_enemy = True

    def get_condition(self):
        health = self.health
        max_health = self.max_health
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
        if self.health > 0:
            return None

    # For now, correct items increase disposition by one, add item disposition worth later
    def bribe(self, bribe_item):
        if bribe_item == self.trigger_item:
            print(f"\n{self.name}: Maybe you're not as bad as everyone says you are")
            self.disposition = self.disposition + 1
        else:
            print("I don't want your trash.")
        if len(self.items) > 0 and self.disposition >= 3:
            print(f"You can take this {self.items[0]} I guess. Don't tell anyone I gave it to you though.")
            return self.items[0]
        else:
            return "Nothing"
