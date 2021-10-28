import json
from os.path import join

from game_action_handler import ActionHandler
from game_view_handler import ViewHandler
from game_character import Characters
from game_item import Items
from game_player import Player
from game_room import Rooms
from JSON_handler import JSONHandler


player, rooms, items, characters = Player, Rooms, Items, Characters

json_handler = JSONHandler(join('assets', 'new_game'), {'player.json': player, 'rooms.json': rooms, 'items.json': items, 'characters.json': characters})
data = json_handler.populate_classes()
player, rooms, items, characters = data['player'], data['rooms'], data['items'], data['characters']

viewHandler = ViewHandler()
viewHandler.set_view_content("action response", "Type your command below.")
actionHandler = ActionHandler(viewHandler)
player.viewHandler = viewHandler

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
