from game_item import Items

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

    # only supporting one locked door per room right now
    def unlock_door(self, player_items):
        if len(self.data['locks']) == 0:
            return ("There are no locked doors in this room."), None
        keys = []
        for item in player_items:
            item_ob = Items.item_dict[item]
            print(item_ob)
            if item_ob.general_type == "key":
                keys.append(item_ob)
        if len(keys) == 0:
            return("You don't have any keys."), None
        print(self.data['locks'])
        print(self.data['locks'])
        for lock, lock_stats in self.data['locks'].items():
            for key in keys:
                if lock_stats["path"] == key.data['specific_type']:
                    self.data['linked_rooms'][lock_stats["direction"]] = lock_stats["location"]
                    del self.locks[lock]
                    return f"You unlock the door to the {lock_stats['direction']} but the key breaks off in the lock.", key.name
        return "The keys you have don't fit any of the doors here.", None

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
