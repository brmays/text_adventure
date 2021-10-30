class Items():

    def __init__(self, data):
        self.data = data
        self.item_dict = self.generate_items()

    def generate_items(self):
        item_dict = {}
        for name, data in self.data.items():
            this_item = Item(data)
            item_dict[name] = this_item
        return item_dict
    
    def transfer_item(self, origin, destination, item):
        origin.remove(item)
        destination.append(item)

    def generate_list_string(self, item_list, conjunction):
        if type(item_list[0]) != Item:
            itemized_list = []
            for item in item_list:
                itemized_list.append(self.item_dict[item])
            item_list = itemized_list
        if len(item_list) == 1:
            return item_list[0].data['indefinite_article'] + " " + item_list[0].data['name'] + "."
        elif len(item_list) > 0:
            new_list_string = ""
            for this_item in item_list[:-1]:
                new_list_string = new_list_string + " " + this_item.data['indefinite_article'] + " " + this_item.data['name'] + ","
            new_list_string = new_list_string + " " + conjunction + " " + item_list[-1].data['indefinite_article'] + " " + item_list[-1].data['name'] + ". "
            return new_list_string
        else:
            return "Something went wrong."

    def transfer_to_player(self, player_and_room, parsed_items):
        if parsed_items[1] == "Not found":
            return "You already have that."
        if len(player_and_room[0].data['items']) > 15:
            return "You have too many items in your backpack. You'll need to drop something."
        else:
            self.transfer_item(player_and_room[1].data['items'], player_and_room[0].data['items'], parsed_items[1])
            return f"You take the {parsed_items[1]}"

    def transfer_to_room(self, player_and_room, parsed_items):
        if parsed_items[0] == "Not found":
            return "You don't have that item."
        self.transfer_item(player_and_room[0].data['items'], player_and_room[1].data['items'], parsed_items[0])
        return f"You drop the {parsed_items[0]}"

    def player_equip(self, player_and_room, parsed_items):
        player_has_item = parsed_items[0] == "Not found"
        item = self.item_dict[parsed_items[player_has_item]]
        if item.data['general_type'] != "equipment":
            return "You can't equip that"
        old_item = player_and_room[0].data['equipment'][item.data['specific_type']][0]
        if old_item != 'fist':
            player_and_room[0].data['items'].append(old_item)
        player_and_room[0].data['equipment'][item.data['specific_type']] = [item.data['name'], item.data['stat']]
        player_and_room[player_has_item].data['items'].remove(item.data['name'])
        return f"You equip the {item.data['name']}"

    def use_item(self, player_and_room, parsed_items):
        player_has_item = parsed_items[0] == "Not found"
        item = self.item_dict[parsed_items[player_has_item]]
        if item.data['general_type'] == "consumable" and item.data['specific_type'] == "health":
            player_and_room[player_has_item].data['items'].remove(item.data['name'])
            result = player_and_room[0].adjust_health(item.data['stat'])
            return f"You consume the {item.data['name']} {result}."
        else:
            return "You can't use that, at least not now."

class Item():

    def __init__(self, data):
        self.data = data
