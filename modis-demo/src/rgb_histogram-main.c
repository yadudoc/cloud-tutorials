/*
 * rgb_histogram-main.c
 *
 *  Created on: Aug 1, 2013
 *      Author: wozniak
 */


#include <stdio.h>
#include <stdlib.h>

#include "src/rgb_histogram.h"

static void usage(void)
{
  printf("usage: rbg_histogram myfile.rgb\n");
}

/**
  Input to this program should be a raw, greyscale RGB file
  Usage: rgb_histogram.pl myfile.rgb
*/
int
main(int argc, char* argv[])
{
  if (argc != 2)
  {
    usage();
    return 1;
  }

  int histogram[256];

  char* filename = argv[1];
  FILE* file = fopen(filename, "r");
  if (file == NULL)
  {
    printf("could not open: %s\n", filename);
    return 1;
  }

  bool result = rgb_histogram(file, histogram);
  if (!result)
  {
    printf("error reading file: %s\n", filename);
    return 1;
  }

  for (int i = 0; i < 256; i++)
  {
     if (histogram[i] == 0) continue;
     printf("%d %d %02x\n", histogram[i], i, i);
  }

  fclose(file);

  return 0;
}
