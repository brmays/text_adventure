from game_view_handler import ViewHandler
from sys import exit
from random import random, randint
from functools import partial
from game_fight_handler import FightHandler

class ActionHandler():

    def __init__(self, viewHandler, player, items, rooms, characters):
        self.commands = {
            "examine": self.examine,
            "help": self.examine,
            "move": self.room_command,
            "unlock": self.room_command,
            "equip": self.item_command,
            "take": self.item_command,
            "drop": self.item_command,
            "use": self.item_command,
            "talk": self.talk,
            "fight": self.fight,
            "quit": self.quit
        }
        self.fightHandler = FightHandler
        self.viewHandler = viewHandler
        self.player = player
        self.items = items
        self.rooms = rooms
        self.characters = characters
        self.set_view_content = partial(viewHandler.set_view_content, "action response")

    def handle_input(self, input_string):
        command = "Not found"
        split_input = input_string.split()
        for word in split_input:
            if word in self.commands:
                command = word
        if command == "Not found": 
            self.set_view_content("Sorry, you can't do that right now. Ask for help if needed.")
        else:
            self.commands[command](command, input_string)

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

    def parse_object(self, input_string, object_list):
        target_object = "Not found"
        for object in object_list:
            if object.lower() in input_string:
                target_object = object
        return target_object

    def parse_character(self, input_string, room):
        character_list = self.rooms.room_dict[room].data['characters']
        target_name = self.parse_object(input_string, character_list)
        if target_name == "Not found":
            for character in character_list:
                target_descriptor = self.parse_object(input_string, self.characters.character_dict[character].data['descriptors'])
                if target_descriptor != "Not found":
                    target_name = character
        return target_name

    def view(self, command, input_string):
        if "character" in input_string:
            self.player.update_stats()
            self.viewHandler.update_view("view_character")
        else:
            self.set_view_content("Do you want to view help or character?")

    def examine(self, _, input_string):
        view_tag = self.parse_object(input_string, ["room", "exits", "characters", "items"])
        if "self" in input_string:
            self.player.update_stats()
            self.viewHandler.update_view("view_character")
        elif "backpack" in input_string:
            backpack_contents = "You look into your backpack and see " + self.items.generate_list_string(self.player.data['items'], "and")
            self.viewHandler.set_view_content("info_text", backpack_contents)
            self.viewHandler.update_view("info")
        elif view_tag != "Not found":
            long_text = self.viewHandler.content[view_tag][2]
            self.viewHandler.set_view_content("info_text", long_text)
            self.viewHandler.update_view("info")
        else:
            room_items = self.rooms.room_dict[self.player.data['current_room']].data['items']
            room_item = [self.parse_object(input_string, room_items), self.items.item_dict]
            player_item = [self.parse_object(input_string, self.player.data['items']), self.items.item_dict]
            target_name = [self.parse_character(input_string, self.player.data['current_room']), self.characters.character_dict]
            other = [room_item, player_item, target_name]
            result = ["Not found", None]
            for target in other:
                if target[0] != "Not found":
                    result = target
            if result[0] == "Not found":
                self.set_view_content("You don't see anything here by that name to examine.")
                self.viewHandler.update_view("main")
            else:
                self.viewHandler.set_view_content("info_text",result[1][result[0]].data['description'])
                self.viewHandler.update_view("info")
        input(">")
        self.viewHandler.update_view("main")

    def room_command(self, command, input_string):
        current_room = self.rooms.room_dict[self.player.data['current_room']]
        room_commands = {"move": current_room.change_room, "unlock": current_room.unlock_door}
        room_commands[command](self, self.player, input_string)

    def item_command(self, command, input_string):
        item_commands = {"take": self.items.transfer_to_player, "equip": self.items.player_equip, "drop": self.items.transfer_to_room, "use": self.items.use_item}
        room = self.rooms.room_dict[self.player.data['current_room']]
        room_item = self.parse_object(input_string, room.data['items'])
        player_item = self.parse_object(input_string, self.player.data['items'])
        if player_item == "Not found" and room_item == "Not found":
            self.set_view_content("That item is not here.")
        else:
            self.set_view_content(item_commands[command]([self.player, room], [player_item, room_item]))


    def talk(self, command, input_string):
        target_name = self.parse_character(input_string.data['current_room'])
        if target_name == "Not found":
            self.set_view_content("That person is not here")
        else:
            self.set_view_content(self.characters.character_dict[target_name].data['conversation'])

    def fight(self, command, input_string):
        target_string = self.parse_character(input_string.data['current_room'])
        target_name = self.characters.character_dict[target_string]
        room = self.rooms.room_dict[self.player.data['current_room']]
        fight_instance = FightHandler(self.viewHandler, target_name, room)
        fight_instance.start_fight()

    def act_without_item(self, command, input_string):
        pass

    def quit(self, command, input_string):
        exit()
