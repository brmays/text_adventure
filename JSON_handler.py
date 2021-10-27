class JSONHandler():
    # take a dict of classes - file names, search for jsons that match the files, and populate classes with dicts of json content
    def __init__(self, name, room_description, description, indefinite_article, general_type, specific_type, stat):
        self.name = name
        self.room_description = room_description
        self.description = description
        self.indefinite_article = indefinite_article
        self.general_type = general_type
        self.specific_type = specific_type
        self.stat = stat
