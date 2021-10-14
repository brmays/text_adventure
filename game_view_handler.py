from sys import builtin_module_names, exit
from os import system, name
from math import ceil
from textwrap import wrap

class ViewHandler():

    def __init__(self):
        self.views = {
            "open": self.draw_open,
            "info": self.draw_info,
            "main": self.draw_main,
            "fight": self.draw_fight,
            "die": self.draw_death,
            "view_character": self.view_character
        }
        self.content = {
            "room": [3, [], []], # max length, truncated text, full text
            "exits": [1, [], []],
            "characters": [3, [], []],
            "items": [3, [], []],
            "action response": [3, [], []],
            "fight_command": [1, [], []],
            "info_text": [11, [], []]
        }
        self.player_info = {}
        self.fight_vitals = {}
        self.info_text = {}
        self.width = 74

    def clear(self):
        if name == 'nt':
            _ = system('cls')
        else:
            _ = system('clear')

    def update_view(self, view):
        self.clear()
        self.views[view]()

    def win_game(self):
        self.clear()
        self.draw_info()
        input("> ")
        exit()

    def beautify_text(self, text, center):
        wrapped_text = wrap(text)
        formatted_text = []
        for line in wrapped_text:
            spaces = 71 - len(line)
            if center:
                formatted_line = "* " + ((spaces//2) * " ") + line + (((spaces // 2) + (spaces % 2)) * " ") + "*"
            else:
                formatted_line = "* " + line + (spaces * " ") + "*"
            formatted_text.append(formatted_line)
        return formatted_text
    
    def truncate_text(self, formatted_text, max_length, part):
        trailing_text = f"...  Type 'examine {part}' for more information"
        # if formatted_text[-1][len(formatted_text[-1])- (len(trailing_text) + 2):] ==  " " * len(trailing_text) + " *":
        #     return formatted_text
        last_line = formatted_text[max_length - 1]
        formatted_text = formatted_text[:max_length - 1]
        words = last_line.split()
        new_last_line = words[0]
        for word in words[1:]:
            if len(new_last_line + " " + word) + len(trailing_text) >= 70:
                new_last_line = new_last_line + trailing_text
                new_last_line = new_last_line +  (((73 - len(new_last_line)) * " ") + "*")
                break
            else:
                space = ""
                if word not in [".,!?-"]:
                    space = " "
                new_last_line = new_last_line + space + word
        formatted_text.append(new_last_line)
        return formatted_text

    def set_view_content(self, part, text):
        center = False
        if part == "action response" or part == "fight":
            center = True
        formatted_text = self.beautify_text(text, center) 
        self.content[part][2] = formatted_text
        max_length = self.content[part][0]
        if len(formatted_text) > max_length:
            formatted_text = self.truncate_text(formatted_text, max_length, part)
        elif len(formatted_text) < max_length:
            formatted_text.insert(0, "*" + (72 * " ") + "*")
            for i in range(max_length - len(formatted_text)):
                formatted_text.append("*" + (72 * " ") + "*")
        self.content[part][1] = formatted_text

    def draw_open(self):
        print(self.width * "*")
        for i in range(5):
            print("|" + ((self.width-2) * " ") + "|")
        print("|" + (26 * " ") + "Text Adventure Game" + (27 * " ") + "|")
        for i in range(7):
            print("|" + ((self.width-2) * " ") + "|")
        print("|" + (24 * " ") + "Press ENTER to continue" + (25 * " ") + "|")
        for i in range(3):
            print("|" + ((self.width-2) * " ") + "|")
        print(74 * "*")

        input(">")

    # fix this view
    def draw_death(self):
        self.clear()
        print(74 * "*")
        for i in range(8):
            print("|" + (72 * " ") + "|")
        print("|" + (28 * " ") + "You have ceased to exist." + (19 * " ") + "|")
        for i in range(8):
            print("|" + (72 * " ") + "|")
        print(74 * "*")

        input(">")
        exit()

    def centerize(self, lines, width, edges):
        centered_text = []
        for line in lines:
            centered_line = ""
            if len(line) > 0 and line[0] == " ":
                centered_line = edges[0] + line + ((width - len(line)) * " ") + edges[1]
            else:
                left_space = ((width - len(line)) // 2) * " "
                right_space = (len(left_space) + (width - len(line)) % 2) * " "
                centered_line = edges[0] + left_space + line + right_space + edges[1]
            centered_text.append(centered_line)
        return centered_text

    def get_fight_panels(self):
            l_col = 36
            r_col = 35
            # windows doesn't support the unicode. quick fix here. mathmamize it later
            bam = [
                "",
                "\\\\\\    ///",
                "\\\\\\  ///",
                "\\\\\\///",
                "///\\\\\\",
                "///  \\\\\\",
                "///    \\\\\\",
                ""
            ]

            left_side = [
                [
                    "","Player", 
                    "", f"   Weapon: {self.fight_vitals['player']['weapon']}",
                    f"   Armor: {self.fight_vitals['player']['armor']}", 
                    "", f"Health: {self.fight_vitals['player']['health_bar']}",
                    self.fight_vitals['player']['health_nums']
                ], 
                bam
            ]
            left_side_centered = self.centerize(left_side[self.fight_vitals['player']['bam']], l_col, ["!", "|"])

            right_side = [
                [
                    "", f"{self.fight_vitals['opponent']['name']}",
                    "", f"   Weapon: {self.fight_vitals['opponent']['weapon']}",
                    f"   Armor: {self.fight_vitals['opponent']['armor']}",
                    "", f"Status: {self.fight_vitals['opponent']['condition']}",
                    ""
                ],
                bam
            ]
            right_side_centered = self.centerize(right_side[self.fight_vitals['opponent']['bam']], r_col, ["", "!"])

            fight_panels = []
            for left, right in zip(left_side_centered, right_side_centered):
                fight_panels.append(left + right)
            
            return fight_panels

    # so many magic numbers, refactor
    def draw_fight(self):
        l_col = 36
        r_col = 35
        print(74 * "!")
        fight_panels = self.get_fight_panels()
        for line in fight_panels:
            print(line)
        print(f"!{l_col * '_'}|{r_col * '_'}!")
        print(f"!{72*' '}!")
        for line in self.content["action response"][1]:
            print(line)
        print(f"!{72*' '}!")
        print(f"!{72*'.'}!")
        print(self.content["fight_command"][1][0])
        print(f"!{72*'.'}!")
        print(74 * "!")

    def view_character(self):
        print(74 * "*")
        for i in range(2):
            print("|" + (72 * " ") + "|")
        print("|" + (29 * " ") + "Level:" + (9 * " ") + self.player_info["level"] + ((28 - len(self.player_info["level"])) * " ") + "|")
        print("|" + (29 * " ") + "Experience:" + (4 * " ") + self.player_info["experience"] + ((28 - len(self.player_info["experience"])) * " ") + "|")
        print("|" + (29 * " ") + "Next Level:" + (4 * " ") + self.player_info["to_next"] + ((28 - len(self.player_info["to_next"])) * " ") + "|")
        for i in range(2):
            print("|" + (72 * " ") + "|")
        print("|" + (29 * " ") + "Health:" + (8 * " ") + self.player_info["health"]+ "/" + self.player_info["max_health"] + ((27 - len(self.player_info["health"]) - len(self.player_info["max_health"])) * " ") + "|")
        print("|" + (29 * " ") + "Dexterity:" + (5 * " ") + self.player_info["dexterity"] + ((28 - len(self.player_info["dexterity"])) * " ") + "|")
        for i in range(2):
            print("|" + (72 * " ") + "|")
        print("|" + (29 * " ") + "Weapon:" + (6 * " ") + self.player_info["weapon"] + ((10 - len(self.player_info["weapon"])) * " ") + self.player_info["weapon_stat"] + ((20 - len(self.player_info["weapon_stat"])) * " ") + "|")
        print("|" + (29 * " ") + "Armor:" + (7 * " ") + self.player_info["armor"]  + ((10 - len(self.player_info["armor"])) * " ") + self.player_info["armor_stat"] + ((20 - len(self.player_info["armor_stat"])) * " ") + "|")
        for i in range(3):
            print("|" + (72 * " ") + "|")
        print(74 * "*")

        input(">")

    def draw_info(self):
        print(self.width * "*")
        print("|" + ((self.width -2) * " ") + "|")
        for line in self.content["info_text"][1]:
            print(line)
        print("|" + ((self.width -2) * " ") + "|")
        print("|" + (24 * " ") + "Press ENTER to continue" + (25 * " ") + "|")
        for i in range(3):
            print("|" + ((self.width-2) * " ") + "|")
        print(74 * "*")
    
    def draw_help(self, commands):
        self.clear()
        # 17
        columns = [7, 25, 43, 61]
        rows = ceil(len(commands)/4)
        for i in range(len(commands) % 4):
            commands.append(" ")
        print(self.width * "*")
        for i in range(3):
            print("|" + ((self.width-2) * " ") + "|")
        print("|" + (6 * " ") + "Available Commands:" + (47 * " ") + "|")
        print("|" + ((self.width-2) * " ") + "|")
        for i in range(rows):
            row_commands = commands[i * 4: (i * 4) + 4]
            this_line = "|"
            for index, column in enumerate(columns):
                this_line = this_line + ((column - len(this_line)) * " " + row_commands[index])
            this_line = this_line + ((73 - len(this_line)) * " " + "|")
            print(this_line)
        for i in range(max(5 - rows, 0)):
            print("|" + ((self.width-2) * " ") + "|")
        for i in range(2):
            print("|" + ((self.width-2) * " ") + "|")
        print(f"|{5*' '}Most commands need to be followed another word. For example, {6* ' '}|")
        print(f"|{5*' '}'move south' or 'talk to fred'. Capitalization, grammar, and{7*' '}|")
        print(f"|{5*' '}puncutation aren't important. Ex: 'take potion' is the same as{5*' '}|")
        print(f"|{5*' '}'TAKE THE POTION' is the same as 'Take the potion, please.{9*' '}|")
        print("|" + ((self.width-2) * " ") + "|")
        print(74 * "*")


    def draw_main(self):
        print(74 * "*")
        for line in self.content["room"][1]:
            print(line)
        print("|___" + (66 * " ") + "___|")
        for line in self.content["exits"][1]:
            print(line)
        print("|___" + (66 * " ") + "___|")
        for line in self.content["characters"][1]:
            print(line)
        print("|___" + (66 * " ") + "___|")
        for line in self.content["items"][1]:
            print(line)
        print("|___" + (66 * " ") + "___|")
        for line in self.content["action response"][1]:
            print(line)
        print(74 * "*")
