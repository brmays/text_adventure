import json

from game_action_handler import ActionHandler
from game_view_handler import ViewHandler
from game_character import Character
from game_item import Item
from game_player import Player
from game_room import Room



player = Player
rooms = Room.room_dict
items = Item.item_dict
characters = Character.character_dict

viewHandler = ViewHandler()
viewHandler.set_view_content("action response", "Type your command below.")
actionHandler = ActionHandler(viewHandler)

files = [open('player.json'), open('rooms.json'), open('items.json'), open('characters.json')]
classes = [Player, Room, Item, Character]
assets = [player, rooms, items, characters]

starting_info = zip(files, classes, assets)

for json_file, klass, this_asset in starting_info:
    data = json.load(json_file)
    for asset in data['assets']:
        class_init_params = list()
        for key, val in asset.items():
            class_init_params.append(val)
        if this_asset == player:
            player = Player(viewHandler, *class_init_params)
        else:
            this_asset[asset['name']] = klass(*class_init_params)


viewHandler.update_view("open")
viewHandler.set_view_content("info_text", player.open)
viewHandler.update_view("info")
input("> ")

while 1:
    current_room = rooms[player.current_room]
    viewHandler.set_view_content("room", current_room.description)
    viewHandler.set_view_content("exits", current_room.generate_exit_list("and"))

    room_characters = [characters[x] for x in current_room.characters]
    characters_description = ""
    for room_character in room_characters:
        characters_description = characters_description + room_character.description
        
        if len(room_character.items) > 0:
            character_items = [items[x] for x in room_character.items]
            items_string = Item.generate_list_string(character_items, "and")
            characters_description.join(f"{room_character.name} is holding {items_string}")
    viewHandler.set_view_content("characters", characters_description)
    
    room_items_description = current_room.get_items_description()
    viewHandler.set_view_content("items", room_items_description)
    viewHandler.update_view("main")

    command = input("> ").lower()

    actionHandler.handle_input(command, player)
