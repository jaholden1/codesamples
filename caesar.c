#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

//declare caesarCypher() function
void caesarCypher(string str, int key);

int main(int argc, string argv[])
//if 1 command line arg isn't provided, abort
{
    if (argc != 2){
       printf("Fatal Error. Abort!\n");
       return 1;
    }
    
    //convert string to int
        int key = atoi(argv[1]);
        printf("plaintext: ");
        
        //get string input from user
        string str = get_string();
        
    //Check that input is not empty
    if (str != NULL) {
        printf("ciphertext: ");
        caesarCypher(str, key);
        return 0;
    }
}

//encode string
void caesarCypher(string str, int key)
{
  //loop through chars in string
            for(int i = 0, n = strlen(str); i < n; i++){
                int cindex = 0;
                char c = str[i];
                
                if(isalpha(c)){
                    // change value to get numeric index based on upper or lower case char
                    if(isupper(c)){
                        cindex = 65;
                    }
                    if(islower(c)){
                        cindex = 97;
                    }
                    // add key to char, convert to numeric index to encipher and convert back to ASCII to print
                        int ascii = (((c + key) - cindex) % 26) + cindex;
        printf("%c", ascii);
            }
            else{
            //don't do any conversions if char is not alpha
             printf("%c", c);
            }
        }
        printf("\n"); 
        }

