import cs50
import sys

def main():
    """Encode plaintext using caesars cypher."""
    
    # if 1 command line arg isn't provided, abort
    if len(sys.argv) != 2:
        print("Usage: ./caesar k")
        exit(1)
    
    # get string input from user
    print("plaintext: ", end="")
    n = cs50.get_string()
    y = sys.argv[1]
    
    # check that input is not empty
    if n != None:
        print("ciphertext: ", end="")
        caesarCypher(n, y)
        exit(0)


def caesarCypher(n,y):
    """Encode string."""
    
    # convert each char to numeric value, add key and convert back to char if char is alpha
    for i in n:
        if (ord(i) >= 65 and ord(i) <= 90):
            x = (((ord(i) + int(y))  - 65) % 26) + 65
            ascii = chr(x)
            print("{}".format(ascii), end="")
        elif (ord(i) >= 97 and ord(i) <= 122):
            x = (((ord(i) + int(y))  - 97) % 26) + 97
            ascii = chr(x)
            print("{}".format(ascii), end="")
        else:
            print(i, end="")
    print("")


if __name__ =="__main__":
    main()