#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

//declare vigenereCypher() function
void vigenereCypher(string str, string key);

int main(int argc, string argv[])
//if single command line arg isn't provided, abort
{
    if (argc != 2){
       printf("Fatal Error. Abort!\n");
       return 1;
    }
//if integers or special characters are provided in key, abort
     string key = argv[1];
    for(int i = 0, n = strlen(key); i < n; i++)
            {
                char keyletter = key[i];
                if (!isalpha(keyletter))
                {
                        printf("Fatal Error. Abort!\n");
                        return 1;
                }
            }
            
        printf("plaintext: ");
//get string input from user
        string str = get_string();

////Check that input is not empty
 if (str != NULL) {
printf("ciphertext: ");
vigenereCypher(str, key);
return 0;

}
 }
 
//encode string 
 void vigenereCypher(string str, string key)
 {
//loop through characters in both plaintext & key for length of plaintext
        for(int i = 0, j =0, n = strlen(str); i < n; i++, j++)
            {
//if jth iteration is longer than the length of key, loop back to the first character and start again
         if (j >= strlen(key))
        {
            j = 0;
        }
        
 char strletter = str[i];
 char keyletter = key[j];
 //declare variables
 int klindexamount = 0;
 int strindexamount = 0;
 //if user input character is not alpha, print the value and don't increment the key character
     if(!isalpha(strletter))
                {
                     printf("%c", strletter); 
                     j--;
                }
          
                if(isalpha(strletter))
                {
   //calculate value for conversion from ASCII to index based on case type for Key char                       
                     if(isupper(keyletter))
                    {
                        klindexamount = 65;
                    }
                    if(islower(keyletter))
                    {
                        klindexamount = 97;
                    }
  //calculate value for conversion from ASCII to index based on case type for plaintext char                        
                    if(isupper(strletter))
                    {
                        strindexamount = 65;
                    }
                    if(islower(strletter))
                    {
                        strindexamount = 97;
                    }
 //calculate index value for plaintext + key and convert back to ASCII  
                  int strencode = (((strletter - strindexamount)  + (keyletter - klindexamount)) % 26) + strindexamount;
            printf("%c", strencode); 
                    }
            }
             printf("\n");
}
