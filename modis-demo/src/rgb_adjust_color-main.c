
/*
 * rgb_adjust_color-main.c
 *
 *  Created on: Aug 1, 2013
 *      Author: wozniak
 */

#include <stdbool.h>
#include <stdio.h>
#include <string.h>

#include "src/rgb_adjust_color.h"

static void usage(void)
{
  printf("usage: rbg_adjust_color input.rgb table.txt output.rgb\n");
}

static bool scan_translation(const char* translation_filename,
                             int* translation);

/**
   Usage: rgb_adjust_color input.rgb table.txt output.rgb
*/
int
main(int argc, char* argv[])
{
  if (argc != 4)
  {
    usage();
    return 1;
  }

  int translation[17];

  bool result = scan_translation(argv[2], translation);
  if (!result) return 1;

  FILE* input_file = fopen(argv[1], "r");
  if (input_file == NULL)
  {
    printf("could not open input file: %s\n", argv[1]);
    return false;
  }

  FILE* output_file = fopen(argv[3], "w");
  if (output_file == NULL)
  {
    printf("could not open output file: %s\n", argv[3]);
    return false;
  }

  translate(input_file, translation, output_file);

  return 0;
}

/**
 * @param translation OUT The translation table
 */
static bool
scan_translation(const char* translation_filename, int* translation)
{
  FILE* translation_file = fopen(translation_filename, "r");
  if (translation_file == NULL)
  {
    printf("could not open translation table: %s\n",
           translation_filename);
    return false;
  }

  char buffer[64];
  int key;
  int value;
  while (true)
  {
    char* result = fgets(buffer, 64, translation_file);
    if (!result) break;
    int n = sscanf(buffer, "#%x #%x", &key, &value);
    if (n != 2)
    {
      printf("bad line in translation table: %s\n", buffer);
      return false;
    }
    // printf("%x __ %x\n", key, value);
    int k = key % 17;
    // printf("k: %i\n", k);
    unsigned char* p = (unsigned char*) &value;
    unsigned char t = p[0];
    // printf("p: %x %x %x %x\n", p[0], p[1], p[2], p[3]);
    memcpy(&p[0], &p[2], sizeof(char));
    memcpy(&p[2], &t, sizeof(char));
    translation[k] = value;
  }
  printf("scan done\n");
  return true;
}
