#include <stdio.h>
#include <cs50.h>

 
int pyramid(int height);

int main(void)
{
 int height;
 
    // prompts user input
    do
    {
        printf("Height:");
        height = get_int();
    }
    while ((height < 0) || (height > 23));
 
    //calls pyramid function
    pyramid(height);
}

    // loop user input to create rows, spaces, and hashes
int pyramid(int height)
{
    int rows;
    int space;
    int hash;
    for (rows = 1; rows <= height; rows++) 
    {
        for (space = (height - rows); space > 0; space--)
        {
            printf(" "); 
        }
 
        for (hash = 0; hash <= rows; hash++)
        {   
            printf("#"); 
        }
 
        printf("\n");
    }
    return 0;
}