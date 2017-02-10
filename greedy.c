#include <stdio.h>
#include <cs50.h>

void calculateCoins(int change);
int main(void){
    float input;
    int change;
    printf("O hai! ");
    
    // prompts user input
    do 
    {
     printf("How much change is owed?\n");
     input = get_float();
     change =  (long) ((input* 100)+0.5); 
    }
    while (input < 0);
    
    //calls calculateCoins function
    calculateCoins(change);
}

    // calculate change at end of each loop and count loops until change is 0 and prints
 void calculateCoins(int change)
{
    int coins = 0;
    int quarters = 25;
    int dimes = 10;
    int nickles = 5;
    int pennies = 1;
 
    while(change >=quarters)
{
        change = change - quarters;
        coins++;
    }
    while(change >=dimes)
{
        change = change - dimes;
        coins++;
    }
    while(change >=nickles)
{
        change = change - nickles;
        coins++;
    }
    while(change >=pennies)
{
        change = change - pennies;
        coins++;
    }
    
 printf("%i\n", coins);
}
