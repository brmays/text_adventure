class Player():

    def __init__(self, data):
        self.data = data['player']
        self.viewHandler = None

    def update_stats(self):
        new_stats = {
                "level": str(self.data['level']),
                "experience": str(self.data['experience']),
                "to_next": str(self.data['level_up']),
                "health": str(self.data['health']),
                "max_health": str(self.data['max_health']),
                "dexterity": str(self.data['dexterity']),
                "weapon": str(self.data['equipment']["weapon"][0]),
                "weapon_stat": str(self.data['equipment']["weapon"][1]),
                "armor": str(self.data['equipment']["armor"][0]),
                "armor_stat": str(self.data['equipment']["armor"][1]),
        }
        self.viewHandler.player_info = new_stats

    def equip(self, item):
        if item.data['general_type'] == "equipment":
            old_item = self.data['equipment'][item.data['specific_type']][0]
            self.data['equipment'][item.data['specific_type']] = [item.data['name'], item.data['stat']]
            return old_item
        else:
            self.viewHandler.set_view_content("action response", "You can't equip that.")

    def add_experience(self, experience):
        new_experience = self.data['experience'] + experience
        if new_experience >= self.data['level_up']:
            self.data['level'] = self.data['level'] + 1
            self.data['level_up'] = self.data['level_up'] + (self.data['level_up'] * self.data['level'])
            self.data['dexterity'] = self.data['dexterity'] + self.data['level']
            self.data['health'], self.data['max_health'] = self.data['max_health'] + (self.level * 2), self.data['max_health'] + (self.data['level'] * 2)
            return "Congratulations. You have leveled up. Type 'view character' to see your new stats."
            # make a congrats, you leveled up view
        else:
            self.data['experience'] = new_experience
            return f"You have gained {experience} experience points."

    def adjust_health(self, value):
        if value > 0:
            self.data['health'] = min(self.data['health'] + value, self.data['max_health'])
            return "and feel a little better"
        else:
            self.data['health'] = self.data['health'] + value
            if self.data['health'] <= 0:
                self.viewHandler.draw_death()
            return "and feel a little worse"
