class RPGInfo():
    author = "Anonymous"

    def __init__(self, game_title):
        self.title = game_title

    def welcome(self):
        print("\n\nWelcome to %s\n" %(self.title))

    def help_menu(self):
        print("You find yourself in a spooky house crawling with the undead.\nYou will need to find and defeat all your enemies with items they have a weakness for to win the game.\nDon't die in the process!!")
        print("\nTo get you started...\n")
        print("You may move between rooms using:\nnorth, south, east, west\n\n")
        print("These commands may be used to interact with your environment:\n"
        "\ntalk: Hear what they want to say."
        "\nhug: Give them a hug, if they'll let you.\n     This may benefit you."
        "\nfight: You may need to defeat all your enemies.\n       Not everyone you meet is an enemy."
        "\nbribe: You may bribe some characters for items they carry"
        "\nsleep: You may put some characters to sleep."
        "\nwake: Wake up a sleeping chracter"
        "\nlook: Look closely at items in the room"
        "\nbag: Look at the inventory on your backpack.\n     You can carry a maximum of five items."
        "\ntake: Take an item and place it in your backpack"
        "\ndrop: Remove an item from your backpack and leave it in an empty room.\n      You can only remove an item if there is no other item already that room.\n      Using an item will remove it form your inventory as well.\n\n")
        print("Now let's start!!")

    @staticmethod
    def info():
        print("        Created during FutureLearn.com course by me!\n")

    @classmethod
    def credits(cls):
        print("Thank you for playing")
        print("Created by %s\n\n\n\n" %(cls.author))


