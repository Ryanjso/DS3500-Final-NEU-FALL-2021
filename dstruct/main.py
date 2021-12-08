from engine import Engine
from engine import Train_engine
from table import Table
from player import Player
from game import update_prob, Game
import json


def main():
    # f = open('cfr.json')
    # load = json.load(f)
    # update_prob(load)
    #
    # print("TESTING LOAD")
    # for x in load:
    #     print(x, " : ", load[x])

    print("\nPROBBBBBBB*************")
    for x in Game.probability_dict:
        print(x, " : ", Game.probability_dict[x])

    poker = Train_engine()
    poker.go(50000)
    poker.table.current_game.convert_totals()

    data = poker.table.current_game.regrets_dict
    print("\nFINAL*************")
    for x in data:
        print(x, " : ", data[x])

    cfr_scores = open("cfr.json", "w")
    cfr_scores = json.dump(data, cfr_scores)

    update_prob(data)
    print("\nPROBBBBBBB*************")
    for x in Game.probability_dict:
        print(x, " : ", Game.probability_dict[x])

    # player1, player2 = None, None
    #
    # while True:
    #     mode = input("choose a game selection: ai-ai, human-ai, or human-human: ")
    #     if mode in ("ai-ai", "human-ai", "human-human"):
    #         break
    #     else:
    #         print("invalid mode entered")
    #
    # if mode == "ai-ai":
    #     player1 = Player(100, "AI_1", ai=True)
    #     player2 = Player(100, "AI_2", ai=True)
    #
    # if mode == "human-ai":
    #     username = ""
    #     while True:
    #         username = input("enter player username: ")
    #         if username != "":
    #             break
    #         else:
    #             print("username cannot be empty")
    #
    #     player1 = Player(100, username)
    #     player2 = Player(100, "AI", ai=True)
    #
    # if mode == "human-human":
    #     user1 = ""
    #     user2 = ""
    #     while True:
    #         user1 = input("enter player 1 username: ")
    #         user2 = input("enter player 2 username: ")
    #         if user1 != "" and user2 != "":
    #             break
    #         else:
    #             print("one or both usernames were empty")
    #
    #     player1 = Player(100, user1)
    #     player2 = Player(100, user2)
    #
    # t = Table()
    # t.sit(player1)
    # t.sit(player2)
    # t.new_game()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
