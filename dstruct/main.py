from game import Game
from player import Player


def main():

    game = Game(ante=10)

    player1 = Player(100, "Dwight")
    player2 = Player(100, "Michael")

    game.join_game(player1)
    game.join_game(player2)

    print(game.get_players())

    game.start_game()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
