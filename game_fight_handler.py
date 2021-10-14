from game_player import Player
from game_view_handler import ViewHandler
from random import random
from time import sleep

class FightHandler():

    def __init__(self, viewHandler, player, opponent, room):
        self.viewHandler = viewHandler
        self.commands = {"a": self.attack, "d": self.defend, "r": self.run_away}
        self.player = player
        self.opponent = opponent
        self.room = room
        self.is_players_turn = player.dexterity > opponent.dexterity
        self.command_lines = [
            "Press (a)ttack, (d)efend, or (r)un away.",
            "Press [enter] to continue."
        ]
        self.defense_up = False
        self.default_delay = 2

    def handle_fight(self):
        if self.player.health < 1:
            self.kill_player()
        elif self.opponent.health < 1:
            self.kill_opponent()
            experience = self.player.add_experience(self.opponent.experience_value)
            self.viewHandler.set_view_content("action response", experience)
            self.viewHandler.update_view("fight")
            input("> ")
        elif self.is_players_turn:
            self.get_command()
        else:
            self.take_enemy_action()


    def get_command(self):
        self.viewHandler.set_view_content("fight_command", self.command_lines[0])
        self.viewHandler.update_view("fight")
        input_text = input(">").lower()
        if len(input_text) < 1:
            self.viewHandler.set_view_content("action response", "Please type one of the commands below.")
            self.get_command()
        elif input_text[0] in self.commands.keys():
            command = self.commands[input_text[0]]
            command(True)
        else:
            self.viewHandler.set_view_content("action response", "That didn't work. Try something else.")
            self.viewHandler.update_view("fight")
            self.get_command()

    def start_fight(self):
        # add a roll here later
        print(self.opponent.health)
        self.update_fight_pane_info([False, False])
        if self.player.dexterity > self.opponent.dexterity:
            self.update_viewHandler(
                f"Being more nimble than {self.opponent.name}, you get the first attack. Press [ENTER] to get started.",
                self.command_lines[0], 0
            )
            self.is_players_turn = True
            self.handle_fight()
        else:
            self.update_viewHandler(
                f"{self.opponent.name} got the jump on you. Defend yourself.",
                self.command_lines[1], 0
                )
            input(">")
            self.take_enemy_action()

    def attack(self, is_player):
        participants = [self.opponent, self.player]
        names = [self.opponent.name, "you"]
        attacker, defender, name = participants[is_player], participants[not is_player], names[not is_player]
        modifier = (attacker.dexterity - defender.dexterity) / 10
        roll = random() + modifier
        if self.defense_up == True:
            roll = roll - (roll/2)
            self.defense_up = False
        if roll > .5:
            damage = max(attacker.equipment["weapon"][1] - defender.equipment["armor"][1], 0)
            defender.health = defender.health - damage
            self.update_fight_pane_info([not is_player, is_player])
            if damage > 0:
                self.update_viewHandler(f"The attack hits {name} for {damage} hit points.", "", self.default_delay)
            else:
                self.update_viewHandler(f"The attack lands, but the {attacker.equipment['weapon'][0]} has no effect.", "", self.default_delay)
            self.update_fight_pane_info([False, False])
            self.viewHandler.update_view("fight")
        else:
            self.update_viewHandler("The attack misses.", "", self.default_delay)
            self.viewHandler.update_view("fight")
        self.is_players_turn = not self.is_players_turn
        self.handle_fight()

    def defend(self, unused_var):
        self.defense_up = True
        self.update_viewHandler("You do your best to prepare for the next attack.", "", self.default_delay)
        self.is_players_turn = not self.is_players_turn
        self.handle_fight()

    def run_away(self, unused_var):
        if self.player.dexterity * 2 > self.opponent.dexterity or self.opponent.health < (self.opponent.max_health / 2):
            for dir, n_room in self.room.linked_rooms.items():
                if n_room != "locked":
                    direction, new_room = dir, n_room
            self.player.current_room = new_room
            self.update_viewHandler(f"You manage to flee to the {direction}.", "", self.default_delay)
            self.viewHandler.set_view_content("action response", f"You are now in the {new_room}.")
            self.viewHandler.update_view("main")
        else:
            self.update_viewHandler(f"{self.opponent.name} blocks your escape.", "", self.default_delay)
            self.is_players_turn = not self.is_players_turn
            self.handle_fight()
    
    def take_enemy_action(self):
       # maybe insert some AI here at some point1
       self.update_viewHandler(f"An attack is incoming from {self.opponent.name}'s {self.opponent.equipment['weapon'][0]}.", "", self.default_delay)
       self.attack(False)

    def kill_player(self):
        self.update_viewHandler(f"{self.opponent.name} has bested you.", "", self.default_delay)
        self.viewHandler.draw_death()

    def kill_opponent(self):
        if self.opponent.name in self.room.characters:
            self.room.description = self.room.description + f" {self.opponent.name}'s body is lying on the floor."
            self.room.characters.remove(self.opponent.name)
            self.update_viewHandler(
                f"You have defeated {self.opponent.name}. As {self.opponent.pronouns['sub'].lower()} falls, all of {self.opponent.pronouns['pos']} possessions spill out onto the floor", "", self.default_delay)
            self.room.items = self.room.items + self.opponent.items

    def update_viewHandler(self, action, fight, delay):
        self.viewHandler.set_view_content("action response", action)
        self.viewHandler.set_view_content("fight_command", fight)
        self.viewHandler.update_view("fight")
        sleep(delay)

    def update_fight_pane_info(self, bam):
        player_health_bits = int((self.player.health / self.player.max_health) * 10)
        player_health_bar = "[" + (player_health_bits * "#") + ((10 - player_health_bits) * " ") + "]"
        player_health_nums = "(" + str(self.player.health) + "/" + str(self.player.max_health) + ")"
        opponent_condition = self.opponent.get_condition()

        fight_vitals = {
            "player": {
                "weapon": self.player.equipment["weapon"][0],
                "armor": self.player.equipment["armor"][0],
                "health_bar": player_health_bar,
                "health_nums": player_health_nums,
                "bam": bam[0]
            },
            "opponent": {
                "name": self.opponent.name,
                "weapon": self.opponent.equipment["weapon"][0],
                "armor": self.opponent.equipment["armor"][0],
                "condition": opponent_condition,
                "bam": bam[1]
            }
        }
        self.viewHandler.fight_vitals = fight_vitals
