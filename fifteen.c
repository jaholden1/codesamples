/**
 * fifteen.c
 *
 * Implements Game of Fifteen (generalized to d x d).
 *
 * Usage: fifteen d
 *
 * whereby the board's dimensions are to be d x d,
 * where d must be in [DIM_MIN,DIM_MAX]
 *
 * Note that usleep is obsolete, but it offers more granularity than
 * sleep and is simpler to use than nanosleep; `man usleep` for more.
 */
 
#define _XOPEN_SOURCE 500

#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

// constants
#define DIM_MIN 3
#define DIM_MAX 9

// board
int board[DIM_MAX][DIM_MAX];

// dimensions
int d;
int tile;


// prototypes
void clear(void);
void greet(void);
void init(void);
void draw(void);
bool move(int tile);
bool won(void);

int main(int argc, string argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        printf("Usage: fifteen d\n");
        return 1;
    }

    // ensure valid dimensions
    d = atoi(argv[1]);
   
    if (d < DIM_MIN || d > DIM_MAX)
    {
       
        printf("Board must be between %i x %i and %i x %i, inclusive.\n",
            DIM_MIN, DIM_MIN, DIM_MAX, DIM_MAX);
        return 2;
    }

    // open log
    FILE *file = fopen("log.txt", "w");
    if (file == NULL)
    {
        return 3;
    }

    // greet user with instructions
    greet();

    // initialize the board
    init();

    // accept moves until game is won
    while (true)
    {
        // clear the screen
        clear();

        // draw the current state of the board
        draw();

        // log the current state of the board (for testing)
        for (int i = 0; i < d; i++)
        {
            for (int j = 0; j < d; j++)
            {
                fprintf(file, "%i", board[i][j]);
                if (j < d - 1)
                {
                    fprintf(file, "|");
                }
            }
            fprintf(file, "\n");
        }
        fflush(file);

        // check for win
        if (won())
        {
            printf("ftw!\n");
            break;
        }

        // prompt for move
        printf("Tile to move: ");
        int tile = get_int();
        
        // quit if user inputs 0 (for testing)
        if (tile == 0)
        {
            break;
        }

        // log move (for testing)
        fprintf(file, "%i\n", tile);
        fflush(file);

        // move if possible, else report illegality
        if (!move(tile))
        {
            printf("\nIllegal move.\n");
            usleep(500000);
        }

        // sleep thread for animation's sake
        usleep(500000);
    }
    
    // close log
    fclose(file);

    // success
    return 0;
}

/**
 * Clears screen using ANSI escape sequences.
 */
void clear(void)
{
    printf("\033[2J");
    printf("\033[%d;%dH", 0, 0);
}

/**
 * Greets player.
 */
void greet(void)
{
    clear();
    printf("WELCOME TO GAME OF FIFTEEN\n");
    usleep(2000000);
}

/**
 * Initializes the game's board with tiles numbered 1 through d*d - 1
 * (i.e., fills 2D array with values but does not actually print them).  
 */
void init(void)
{
    int area= (d * d);
    int n = 0;
 
    // two for loops to iterate through 2d array - rows/columns
    for (int i = 0; i < d; i++)
    {
        // subtract one more from area on each iteration
        for (int j = 0; j < d; j++)
        {
            n++;
            board[i][j] = (area - n);
        }
    }   
    // if d is even and the tiles on board odd, swap 1 and 2 so game can be won
    if ((d % 2) == 0)
    {
        // find values immediately one & two columns to the left of 0 (bottom right corner) and swap
        int d1 = d - 1;
        int d2 = d - 2;
        int d3 = d - 3;
        int tmp = board[d1][d2];
        board[d1][d2] = board[d1][d3];
        board[d1][d3] = tmp; 
    }               
}

/**
 * Prints the board in its current state.
 */
void draw(void)
{
    int n = 0;
    // rows
    for (int i = 0; i < d; i++)
    {
        // columns
        for (int j = 0; j < d; j++)
        {
            n++; 
            // print tile value unless it is zero 0
            if (board[i][j] == 0) 
            {
                printf("__");
            }
            else
            {
               printf("%2d", board[i][j]); 
            }
        }
        printf("\n"); 
    }    
}

/**
 * If tile borders empty space, moves tile and returns true, else
 * returns false. 
 */
bool move(int tile)  
{
    int visibleArea = (d * d) -1;
    // check if user input tile number is on board
    if (!(tile <= visibleArea && tile > 0)) 
    {
        return false;
    }
    // loop through table until board value equals tile and get row & col vars 
    int row = 0;
    int col = 0;
    int left = 0;
    int right = 0;
    int top = 0;
    int bottom = 0;

    for (int i = 0; i < d; i++)
    {
        for (int j = 0; j < d; j++)
        {
            if (board[i][j] == tile)
            {
                row = i;
                col = j;
                left = j - 1;
                right = j + 1;
                top = i - 1;
                bottom = i + 1;
            }
        }
    }
    // look for tile in VALID spots (not less than 0 and greater than d-1) adjacent to row/col
    if (board[top][col] == 0 && top >= 0)
    {
        board[top][col] = board[row][col];
        board[row][col] = 0;
        return true;
    }
    else if (board[bottom][col] == 0 && bottom < d)
    {
        board[bottom][col] = board[row][col];
        board[row][col] = 0;
        return true;
    }
    else if (board[row][left] == 0 && left >= 0)
    {
        board[row][left] = board[row][col];
        board[row][col] = 0;
        return true;
    }
    else if (board[row][right] == 0 && right < d)
    {
        board[row][right] = board[row][col];
        board[row][col] = 0;
        return true;
    }
    return false;
}

/**
 * Returns true if game is won (i.e., board is in winning configuration), 
 * else false.
 */
bool won(void)  
{
    // set incremental value to check values against in loop
    int n = 0;
    int area= (d * d);

    for (int i = 0; i < d; i++)
    {
        for (int j = 0; j < d; j++)
        {
            // increment n with each col. when board is in correct decreasing order, n will never equal board value
            // since n increments before check, if n is equal to area than that should be the end
            n++;
            if (n != area && board[i][j] != n)
            {
                return false;
            }
        }
    }
    return true;
}
