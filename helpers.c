/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */
 
#include <cs50.h>
#include <stdio.h>

#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false.  (binary search  O(log n)
 */
bool search(int value, int values[], int n)
{
    if (n < 0)
    {
        return false;
    }
   // set values for first, last, and middle of array.
   int min = 0;
   int max = n - 1;
   int med = (min+max) / 2;
 
   // if max is equal to or less than min, you have looked through all of the values
   while (max >= min) 
   {
      // if needle value is greater than the med set the new min as one greater than the med and recalculate med
      if (values[med] < value)
      {
         min = med + 1;   
         med = (min + max) / 2;
      }
      // if value is equal to med, break the loop
      else if (values[med] == value) 
      {
          return 1;
          break;
      }
      // if not greater than, needle value should be less than med. Set the new max as one less than the med, and recalculate med
      else
      {
         max = med - 1;
         med = (min + max) / 2;
      }
}
return 0;  
}

/**
 * Sorts array of n values. (bubble sort  O(n2)
 */
void sort(int values[], int n)
{
   //loop through pairs
   for (int i = 1; i < n; i++) {
      for (int j = 0, negN = (n - 1); j < negN; j++) 
      {
         // if left value is greater than the right value
         if (values[j] > values[j + 1]) 
         {
           // set the value that needs to bubble up in temp var, the lower value as values[j] and values[j +1] as tmp value
           int tmp = values[j];
            values[j] = values[j + 1];
            values[j + 1] = tmp;
         }
      }
   }
    return;
}
