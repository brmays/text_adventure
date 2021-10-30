from game_fight_handler import FightHandler
from game_item import Items
from random import random, randint

class Rooms():

    def __init__(self, data):
        self.data = data
        self.room_dict = self.generate_rooms()
    
    def generate_rooms(self):
        room_dict = {}
        for name, data in self.data.items():
            this_room = Room(data)
            room_dict[name] = this_room
        return room_dict

class Room():
    
    def __init__(self, data):
        self.data = data

    def change_room(self, action_handler, player, input_string):
        cardinals = ["north", "south", "east", "west"]
        target_direction = list(filter(lambda direction: direction in cardinals, input_string.split()))
        if len(target_direction) != 0: target_direction = target_direction[0]
        if len(target_direction) == 0 or target_direction not in self.data['linked_rooms'].keys():
            return f"You can't go that way. There are exits to the {self.generate_exit_list('and')}"
        if self.data['linked_rooms'][target_direction] == "locked":
            return "There is a locked door blocking your way."
        if len(self.data['characters']) == 0 and len(self.data['random_encounter']["baddie_pool"]) > 0:
            encounter_roll = random()
            if encounter_roll + ((self.data['random_encounter']["chance"]) / 10) > 1:
                baddie_roll = randint(0, len(self.data['random_encounter']["baddie_pool"]) - 1)
                baddie = action_handler.characters.character_dict[self.data['random_encounter']["baddie_pool"][baddie_roll]]
                random_encounter = action_handler.fightHandler(action_handler.viewHandler, player, baddie, self)
                random_encounter.handle_random_encounter()
        player.data['current_room'] = self.data['linked_rooms'][target_direction]
        if player.data['current_room'] == "doggy's room":
            self.viewHandler.set_view_content("info_text".data['win'])
            self.viewHandler.win_game()
        else:
            return "You moved {target_direction}."

    def unlock_door(self, _, player, __):
        locks = self.data['locks']
        if len(locks) == 0:
            return "There are no locked doors in this room."
        for lock in locks:
            if lock['unlocked_with'] in player.data['items']:
                player.data['items'].remove(lock['unlocked_with'])
                self.data.linked_rooms[lock['direction']] = lock['location']
                return f"You unlock the door to the {lock['direction']} but you accidentally snap the key off."
        return "The keys you have don't fit any of the doors here."

    def generate_exit_list(self, conjunction):
        exits = [*self.data['linked_rooms']]
        if len(exits) == 1:
            return f"There is an exit to the {exits[0]}."
        elif len(exits) == 2:
            return f"There are exits to the {exits[0]} and {exits[1]}."
        else:
            exit_string = "There are exits to the "
            for exit in exits[:-1]:
                exit_string = exit_string + exit + ", "
            exit_string = exit_string + conjunction + " " + exits[-1] + "."
            return exit_string

    def get_items_description(self, items):
        room_items = [items.item_dict[x] for x in self.data['items']]
        room_items_description = ""
        for item in room_items:
            room_items_description = room_items_description + item.data['room_description']  + " "
        return room_items_description
