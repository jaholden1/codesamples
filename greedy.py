import cs50

def main():
    """Prompt user input and call calculateCoins."""
    
    print("O hai! ", end="")
    
    # prompts user input
    while True:
        print("How much change is owed?")
        n = cs50.get_float()
        y = (n * 100)
        if n > 0.00:
            break
        
    # calls calculateCoins method
    calculateCoins(y)


def calculateCoins(y):
    """Calculate change at end of each loop and count loops until change is 0 and prints."""
    
    coins = 0
    while y >= 25:
        y = y - 25
        coins += 1

    while y >= 10:
        y = y - 10
        coins += 1

    while y >= 5:
        y = y - 5
        coins += 1

    while y >= 1:
        y = y - 1
        coins += 1

    print("{}".format(coins))
        

if __name__ == "__main__":
    main()
        
    