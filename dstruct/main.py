from engine import Engine
from engine import Train_engine


def main():

    poker = Train_engine()
    poker.go(1000)
    print("\nFINAL*************")
    for x in poker.table.current_game.regrets_dict:
        print(x, " : ", poker.table.current_game.regrets_dict[x])



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
