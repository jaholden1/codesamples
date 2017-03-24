import cs50

def main():
    """Prompt user for input and call Pyramid."""

    # prompts user input
    while True:
        print("Height:", end ="")
        height = cs50.get_int()
        if height > 0 and height <= 23:
            break
    # calls pyramid method
    pyramid(height)


def pyramid(height):
    """Draw Marios pyramid."""
    
    # draw pyramid increasing #, and decreasing spaces by height
    for i in range(1,height + 1,1):
        for n in range(height - i, 0, -1):
            print(" ", end="")
        for l in range(0, i + 1, 1):
            print("#", end="")
        print("")
    # success
    exit(0)


if __name__ == "__main__":
    main()
