from engine import Engine


def main():

    poker = Engine()
    poker.go(runs=1)
    poker.play_ai(2)

    poker.go(100)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
