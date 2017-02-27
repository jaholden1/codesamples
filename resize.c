/**
 * Resizes a BMP 24-Bit Image
 */
       
#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: ./resize n infile outfile\n");
        return 1;
    }
    // convert arg to int
    int n = atoi(argv[1]);
    
    // verify n is positive int between 0 and 100
    if (n < 0 || n > 100)
    {
        fprintf(stderr, "Incorrect value %i. n must be between 0 and 100 inclusive.\n", n);
        return 1;
    }
     
    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file 
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 1;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 1;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    BITMAPFILEHEADER bflarge;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);
    // make a copy of bf struct
    bflarge = bf;

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    BITMAPINFOHEADER bilarge;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);
    // make a copy if bi struct
    bilarge = bi;

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 || 
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }
    
    // multiply large image width & height by n
    bilarge.biWidth *= n;
    bilarge.biHeight *= n;

    // determine padding for scanlines (small and large)
    int padding =  (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int paddinglarge = (4 - (bilarge.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // calculate biSizeImage (total size of image in bytes - includes pixels and padding)
    bilarge.biSizeImage = (bilarge.biWidth * abs(bilarge.biHeight) * 3) + paddinglarge * abs(bilarge.biHeight);
    
    // calculate bfSize (total size of file in bytes - includes pixels, padding, and headers)
    bflarge.bfSize = bilarge.biSizeImage + bflarge.bfOffBits;

    // write outfile's BITMAPFILEHEADER
    fwrite(&bflarge, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bilarge, sizeof(BITMAPINFOHEADER), 1, outptr);
    
    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(bilarge.biHeight); i < biHeight; i++)
    {
        // iterate over pixels in scanline
        for (int j = 0; j < bi.biWidth; j++)
        {
            // temporary storage
            RGBTRIPLE triple;
            
            // read RGB triple from infile
            fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

            // loop over n and write RGB triple to outfile
            for(int k = 0; k < n; k++)
                fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
        }

        // skip over padding, if any
        fseek(inptr, padding, SEEK_CUR);
        
        // then add it back 
        for (int k = 0; k < paddinglarge; k++)
        {
            fputc(0x00, outptr);
        }

        // write a new row if the next iteration mod n is not 0
        if (!((i + 1) % n == 0))
        {
            fseek(inptr, -((long)(bi.biWidth*sizeof(RGBTRIPLE) + padding)), SEEK_CUR);
        }
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}