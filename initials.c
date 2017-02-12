#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>


  //**more comfortable**//

  void printInitials(string s);
int main(void) {
    //Get user input string
    string s = get_string();

    //if user provided input, print initials
    if (s != NULL) {
      printInitials(s);
    }
  }
  //get initials based on user input
void printInitials(string s) {
  int n = 0;
  //print the first letter of the users input if it is not a space
  if (s[n] != ' ') {
    printf("%c", toupper(s[0]));
  }
  //loop through characters until the end of the string  
  while (s[n] != '\0') {
    //if a space is encountered, increase n until it is not a space anymore and print the next character     
    if (s[n] == ' ') {
      while (s[n] == ' ') {
        n++;
      }
      //checks that the next character after the spaces is not the end of string '\0'
      if (s[n] != '\0') {
        printf("%c", toupper(s[n]));
      }
    }
    n++;
  }
  printf("\n");
}


  //**less comfortable**//

  /* int main(void) {
     //Get user input string
     string s = get_string();

     int n = 0;
     
     //Check that input is not empty
     if (s != NULL) {
     //print the first letter of the users input
       printf("%c", toupper(s[0]));
     //loop through characters until the end of the string  
       while (s[n] != '\0') {
     //if a space is encountered, increase n by one to get the next char and print      
         if (s[n] == ' ') {
           n++;
           printf("%c", toupper(s[n]));
         }
         n++;
       }
       printf("\n");
     }
   }*/