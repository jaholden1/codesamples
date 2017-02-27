/**
 * Recovers JPEGs from a forensic image
 */
 
#include <stdio.h>
#include <cs50.h>
#include <stdio.h>
#include <stdint.h>

int main(int argc, string argv[]){
    
     // remember filenames
    char *raw_file = argv[1];
    
    // ensure proper usage
    if(argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }
    
    // open card.raw file 
    FILE *inptr = fopen(raw_file, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", raw_file);
        return 2;
    }
    
    // struct containing bytes being read
   uint8_t buffer[512];
   
   //set counter
   int n= 0;
   FILE *img = NULL;
   
   // read 512 blocks, 1 byte each into a buffer
    while(fread(buffer, 512, 1, inptr))
    {
        // if first 4 bytes of header is that of a jpeg, execute the following
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // close last image file since we have just hit the beginning of another
            if (img != NULL)
            {
                fclose(img);
            }
            
            // array that will store the output
            char filename[7];
            
            // create file name starting with 000.jpg
            sprintf(filename, "%03i.jpg", n);
            
            // open file with writing permissions
            img = fopen(filename, "w");
            // increment counter
            n++;
        }
        // write 512 blocks, 1 byte each
        if (img != NULL)
        {
            fwrite(buffer, 512, 1, img);
        }
    }
    // close any remaining files
    if (img != NULL)
    {
        fclose(img);
    }
          
    // close outfile      
    fclose(inptr);
        
    // success
    return 0;
    
}


// line 41 Question: To be honest, zamyla gave us this part of the code and I don't understand the buffer[3] & 0xf0) == 0xe0 part..
// line 50 Question: I understand creating an array to store output, but don't understand the number value put inside. All documentation I found it looked as though the number can be anything as long as it is enough.