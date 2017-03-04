/**
 * Implements a dictionary's functionality.
 */
 
#include <stdbool.h>
#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>


#include "dictionary.h"

// counter
int n = 0;

// create hashtable
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

node *hashtable[50];

/**
 * Creates hash function
 */
int hash(const char *word)
{
    // return an index
    int index = 0;
    return index;
}

/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char* word)
{
    // create copy of word
    char new_word[strlen(word)];
    strcpy(new_word, word);

    // traverse linked list
    node *head = hashtable[hash(new_word)];
    node *cursor = head;
    
    // word is misspelled if NULL
    while (cursor != NULL)
    {
        // compare two strings
        int result = strcasecmp(new_word, cursor->word);
        if (result == 0)
        {
            // match
            return true;
        }
        // reassign cursor to what node is pointing too
        cursor = cursor->next;
    }
    return false;
}


/**
 * Loads dictionary into memory. Returns true if successful else false.
 */
bool load(const char* dictionary)
{
    // open dictionary file 
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }
    
    char word[LENGTH + 1];
    // scan dictionary word by word
    while (fscanf(file, "%s", word) != EOF)
    {
        // increment counter to determine number of words
        n++;
        // allocate enough space in memory to store our node
        node *new_node = malloc(sizeof(node));

        // malloc a node * for each new word
        if (new_node == NULL)
        {
            unload();
            return false;
        }
        else
        {
            // copy word into node
            strcpy(new_node->word, word);
        }
            // insert into linked list
            node *head = hashtable[hash(word)];
            new_node->next = head;
            hashtable[hash(word)] = new_node;
    }

    fclose(file);
    // success
    return true;
}

/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void)
{
    if (n == 0)
    {
        return 0;
    }
    return n;
}

/**
 * Unloads dictionary from memory. Returns true if successful else false.
 */
bool unload(void)
{
    // increment passed into hashtable so memory isn't leaked
    int n = 0;
    // new node pointer to first element in linked list
    node *cursor = hashtable[n];
    node *temp = NULL;
        while(cursor != NULL)
        {
            
            // create temporary node pointer
            node *temp = cursor;
            // advance cursor
            cursor = cursor->next;
            // free temporary node pointer
            free(temp);
            n++;
        }
         // temp will be null if unsuccessful
         if(temp) 
        {
            return false;
        }
    // success
    return true;
}



// ln 107: why can't i assign head to this part..