
class Items():

    def __init__(self, data):
        self.data = data
        self.item_dict = self.generate_items

    def generate_items(self):
        item_dict = {}
        for name, data in self.data.items():
            this_item = Item(data)
            item_dict[name] = this_item
        return item_dict

    def generate_list_string(item_list, conjunction):
        if type(item_list[0]) != Item:
            itemized_list = []
            for item in item_list:
                itemized_list.append(Item.item_dict[item])
            item_list = itemized_list
        if len(item_list) == 1:
            return item_list[0].indefinite_article + " " + item_list[0].name + "."
        elif len(item_list) > 0:
            new_list_string = ""
            for this_item in item_list[:-1]:
                new_list_string = new_list_string + " " + this_item.indefinite_article + " " + this_item.name + ","
            new_list_string = new_list_string + " " + conjunction + " " + item_list[-1].indefinite_article + " " + item_list[-1].name + ". "
            return new_list_string
        else:
            return "Something went wrong."

class Item():

    def __init__(self, data):
        self.data = data
