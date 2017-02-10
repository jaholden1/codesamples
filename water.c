#include <stdio.h>
#include <cs50.h>

void min(int n);

int main(void)
{
    // prompts user input
    printf("Minutes: ");
    int minutes= get_int();

    //calls min function
    min(minutes);
}

    //calculates value based on user input
void min(int minutes)
{
    int bottles = minutes * 12;
    printf("Bottles: %i\n", bottles);
}