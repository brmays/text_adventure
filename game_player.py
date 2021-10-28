class Player():

    def __init__(self, data):
        self.data_dict = data
        self.viewHandler = None
        self.level = 1
        self.experience = 0
        self.level_up = 100
        self.max_health = 10
        self.health = 10
        self.dexterity = 3
        self.equipment = {
            "weapon": ["fist", 2],
            "armor": ["t-shirt", 1]
        }

    def update_stats(self):
        new_stats = {
                "level": str(self.level), 
                "experience": str(self.experience), 
                "to_next": str(self.level_up),
                "health": str(self.health),
                "max_health": str(self.max_health),
                "dexterity": str(self.dexterity),
                "weapon": str(self.equipment["weapon"][0]),
                "weapon_stat": str(self.equipment["weapon"][1]),
                "armor": str(self.equipment["armor"][0]),
                "armor_stat": str(self.equipment["armor"][1]),
        }
        self.viewHandler.player_info = new_stats

    def equip(self, item):
        if item.general_type == "equipment":
            old_item = self.equipment[item.specific_type][0]
            self.equipment[item.specific_type] = [item.name, item.stat]
            return old_item
        else:
            self.viewHandler.set_view_content("action response", "You can't equip that.")

    def add_experience(self, experience):
        new_experience = self.experience + experience
        if new_experience >= self.level_up:
            self.level = self.level + 1
            self.level_up = self.level_up + (self.level_up * self.level)
            self.dexterity = self.dexterity + self.level
            self.health, self.max_health = self.max_health + (self.level * 2), self.max_health + (self.level * 2)
            return "Congratulations. You have leveled up. Type 'view character' to see your new stats."
            # make a congrats, you leveled up view
        else:
            self.experience = new_experience
            return f"You have gained {experience} experience points."

    def adjust_health(self, value):
        if value > 0:
            self.health = min(self.health + value, self.max_health)
            return "and feel a little better"
        else:
            self.health = self.health + value
            if self.health <= 0:
                self.viewHandler.draw_death()
            return "and feel a little worse"





    

