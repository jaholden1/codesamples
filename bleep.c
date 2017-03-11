#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>


bool upword(const char *word);
int main(int argc, char *argv[])
{
    if (argc != 2)
    {
      printf("Fatal Error. Abort!\n");
      return false;
    }
// convert string to int
char *s = argv[1];
// initiate upword();
upword(s);
}

/**
 * Returns true if chars are in alphabetical order
 */
bool upword(const char *word)
{
   //loop through pairs
   int n = strlen(word);
   for (int i = 1; i < n; i++) 
   {
       // check for non-alpha characters
       if(!(isalpha(word[i])))
          {
            return false;
            break;
          }
      for (int j = 0, negN = (n - 1); j < negN; j++) 
      {
         // if left value is greater than the right value
         if (word[j] > word[j + 1]) 
         {
            return false;
            break;
         }
      }
   }
    return true;
}
