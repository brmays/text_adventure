from game_view_handler import ViewHandler
from sys import exit
from random import random, randint
from functools import partial
from game_fight_handler import FightHandler

class ActionHandler():

    def __init__(self, viewHandler, items, rooms, characters):
        self.commands = {
            "examine": self.examine,
            "help": self.examine,
            "move": self.move,
            "take": self.take_item,
            "drop": self.drop_item,
            "use": self.use_item,
            "unlock": self.unlock_door,
            "talk": self.talk,
            "fight": self.fight,
            "equip": self.equip_item,
            "view": self.view,
            "quit": self.quit
        }
        self.viewHandler = viewHandler
        self.items = items
        self.rooms = rooms
        self.characters = characters
        self.set_view_content = partial(viewHandler.set_view_content, "action response")

    # could probably make player a global
    def handle_input(self, input_list, player):
        command = "Not found"
        split_list = input_list.split()
        for word in split_list:
            if word in self.commands:
                command = word
        if command == "Not found": 
            self.set_view_content("Sorry, you can't do that right now. Ask for help if needed.")
        else:
            self.commands[command](input_list, player)

    def generate_list_string(self, word_list, conjunction):
        if len(word_list) == 1:
            return word_list[0] + "."
        elif len(word_list) > 0:
            new_list = list()
            for index, word in enumerate(word_list[:-1]):
                new_list.append(word + ",")
            new_list.append(conjunction + " " + word_list[-1] + ".")
            return " ".join(new_list)
        else:
            return "Something went wrong."

    def transfer_item(self, origin, destination, item):
        origin.remove(item)
        destination.append(item)

    def parse_object(self, input_list, object_list):
        target_object = "Not found"
        for object in object_list:
            if object.lower() in input_list:
                target_object = object
        return target_object

    def parse_character(self, input_list, room):
        character_list = self.rooms.room_dict[room].data['characters']
        target_name = self.parse_object(input_list, character_list)
        if target_name == "Not found":
            for character in character_list:
                target_descriptor = self.parse_object(input_list, self.characters.character_dict[character].data['descriptors'])
                if target_descriptor != "Not found":
                    target_name = character
        return target_name

    def view(self, input_list, player):
        if "help" in input_list:
            self.set_view_content("Help screen coming soon.")
        elif "character" in input_list:
            player.update_stats()
            self.viewHandler.update_view("view_character")
        else:
            self.set_view_content("Do you want to view help or character?")

    def examine(self, input_list, player):
        view_tag = self.parse_object(input_list, ["room", "exits", "characters", "items"])
        if "backpack" in input_list:
            backpack_contents = "You look into your backpack and see " + self.items.generate_list_string(player.data['items'], "and")
            self.viewHandler.set_view_content("info_text", backpack_contents)
            self.viewHandler.update_view("info")
            input(">")
        elif "help" in input_list:
            available_commands = list(self.commands.keys())
            self.viewHandler.draw_help(available_commands)
            input(">")
        elif view_tag != "Not found":
            room_items = self.rooms.room_dict[player.data['current_room']].get_items_description(self.items)
            self.viewHandler.set_view_content("info_text", room_items)
            self.viewHandler.update_view("info")
            input(">")
        else:
            room_items = self.rooms.room_dict[player.data['current_room']].data['items']
            room_item = self.parse_object(input_list, room_items)
            player_item = self.parse_object(input_list, player.data['items'])
            target_name = self.parse_character(input_list, player.data['current_room'])
            target = "Not found"
            if room_item != "Not found":
                target = self.items.item_dict[room_item]
            elif player_item != 'Not found':
                target = self.items.item_dict[player_item]
            elif target_name != 'Not found':
                target = self.characters.character_dict[target_name]
            if target == "Not found":
                self.set_view_content("You don't see anything here by that name to examine.")
            else:
                self.viewHandler.set_view_content("info_text", target.description)
                self.viewHandler.update_view("info")
                input(">")

        self.viewHandler.update_view("main")

    def move(self, input_list, player):
        current_room = self.rooms.room_dict[player.data['current_room']]
        available_directions = list(current_room.data['linked_rooms'].keys())
        cardinals = ["north", "south", "east", "west"]
        direction = self.parse_object(input_list, cardinals)
        if direction == "Not found":
            self.set_view_content(f"Try again. Available directions are {self.generate_list_string(cardinals, 'and')}")
        elif direction not in current_room.data['linked_rooms'].keys():
            self.set_view_content(f"There is no exit in that direction. Available directions are {self.generate_list_string(list(current_room.data['linked_rooms'].keys()), 'and')}")
        else:
            if current_room.data['linked_rooms'][direction] == "locked":
                self.set_view_content("There is a locked door blocking your way.")
            elif direction in available_directions:
                if len(current_room.data['characters']) == 0 and len(current_room.data['random_encounter']["baddie_pool"]) > 0:
                    encounter_roll = random()
                    if encounter_roll + ((current_room.data['random_encounter']["chance"]) / 10) > 1:
                        baddie_roll = randint(0, len(current_room.data['random_encounter']["baddie_pool"]) - 1)
                        baddie = current_room.data['random_encounter']["baddie_pool"][baddie_roll]
                        self.set_view_content(f"As you exit the room, a {baddie} suddenly blocks your path. Press [enter] to continue.")
                        self.viewHandler.update_view("main")
                        input("> ")
                        room = self.rooms.room_dict[player.data['current_room']]
                        opponent = self.characters.character_dict[baddie]
                        fight_instance = FightHandler(self.viewHandler, player, opponent, room)
                        opponent.data['health'] = opponent.data['max_health']
                        fight_instance.start_fight()
                        if len(current_room.data['random_encounter']["treasure_pool"]) > 0 and opponent.data['health'] <= 0:
                            treasure_roll = randint(0, len(current_room.data['random_encounter']["treasure_pool"]) - 1)
                            treasure = current_room.data['random_encounter']["treasure_pool"][treasure_roll]
                            self.set_view_content(f"You have slain your enemy. It was carrying a {treasure}. You can take it, or sacrifice it to the gods of battle. Do you want it? (Y)es or (n)?")
                            self.viewHandler.update_view("main")
                            answer = input("> ")
                            if len(answer) > 0 and answer[0].lower() == "y":
                                self.set_view_content(f"You take the {treasure}. Press [enter] to continue.")
                                player.data['items'].append(treasure)
                            else:
                                self.set_view_content(f"The {treasure} disappears. Press [enter] to continue.")
                            self.viewHandler.update_view("main")
                            input("> ")
                            self.viewHandler.update_view("main")
                        else:
                            self.set_view_content("You have slain your enemy and gained valuable experience.")
                        print("break")

                player.data['current_room'] = current_room.data['linked_rooms'][direction]
                if player.data['current_room'] == "doggy's room":
                    self.viewHandler.set_view_content("info_text", player.data['win'])
                    self.viewHandler.win_game()
                else:
                    self.set_view_content(f"You moved {direction}.")
            else:
                self.set_view_content(f"You can't go that way. You can move {self.generate_list_string(available_directions, 'or')} ")

    def take_item(self, input_list, player):
        room_items = self.rooms.room_dict[player.data['current_room']].data['items']
        target_item = self.parse_object(input_list, room_items)
        if target_item == "Not found":
            self.set_view_content("You can't find that here.")
        elif len(player.data['items']) > 15:
            self.set_view_content("You have too many items in your backpack. You'll need to drop something.")
        else:
            self.transfer_item(room_items, player.data['items'], target_item)
            self.set_view_content(f"You take the {target_item}")

    def unlock_door(self, input_list, player):
        unlock_success, key_used = self.rooms.room_dict[player.data['current_room']].unlock_door(player.data['items'])
        self.set_view_content(unlock_success)
        if key_used != None:
            player.data['items'].remove(key_used)

    def equip_item(self, input_list, player):
        room_items = self.rooms.room_dict[player.data['current_room']].data['items']
        room_item = self.parse_object(input_list, room_items)
        player_item = self.parse_object(input_list, player.data['items'])
        if room_item != "Not found"  or player_item != "Not found":
            new_item = ""
            if room_item != "Not found":
                new_item = room_item
                old_item = player.equip(self.items.item_dict[room_item])
                room_items.remove(room_item)
                player.data['items'].append(room_item)
            elif player_item != "Not found":
                new_item = player_item
                old_item = player.equip(self.items.item_dict[player_item])
            self.set_view_content(f"You equip the {new_item}")
        else:
            self.set_view_content(f"You don't see that anywhere.")

    def drop_item(self, input_list, player):
        room_items = self.rooms.room_dict[player.data['current_room']].data['items']
        target_item = self.parse_object(input_list, player.data['items'])
        if target_item == "Not found":
            self.set_view_content("You don't have that.")
        else:
            self.transfer_item(player.data['items'], room_items, target_item)
            self.set_view_content(f"You drop the {target_item}")

    def use_item(self, input_list, player):
        room_items = self.rooms.room_dict[player.data['current_room']].data['items']
        room_item = self.parse_object(input_list, room_items)
        player_item = self.parse_object(input_list, player.data['items'])
        if room_item != "Not found"  or player_item != "Not found":
            if room_item != "Not found":
                item_to_be_consumed = self.items.item_dict[room_item]
                room_items.remove(room_item)
            else:
                item_to_be_consumed = self.items.item_dict[player_item]
                player.data['items'].remove(player_item)
            if item_to_be_consumed.data['general_type'] == "consumable" and item_to_be_consumed.data['specific_type'] == "health":
                result = player.adjust_health(item_to_be_consumed.data['stat'])
                self.set_view_content(f"You consume the {item_to_be_consumed.data['name']} {result}.")
            else:
                self.set_view_content("You can't use that, at least not now.")

    def talk(self, input_list, player):
        target_name = self.parse_character(input_list, player.data['current_room'])
        if target_name == "Not found":
            self.set_view_content("That person is not here")
        else:
            self.set_view_content(self.characters.character_dict[target_name].data['conversation'])

    def fight(self, input_list, player):
        target_string = self.parse_character(input_list, player.data['current_room'])
        target_name = self.characters.character_dict[target_string]
        room = self.rooms.room_dict[player.data['current_room']]
        fight_instance = FightHandler(self.viewHandler, player, target_name, room)
        fight_instance.start_fight()

    def act_without_item(self, input_list, player):
        pass

    def quit(self, input_list, player):
        exit()
