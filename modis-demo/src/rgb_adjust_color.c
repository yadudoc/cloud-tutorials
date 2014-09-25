
/*
 * rgb_adjust_color.c
 *
 *  Created on: Aug 1, 2013
 *      Author: wozniak
 */

#include <string.h>

#include "src/rgb_adjust_color.h"

bool
translate(FILE* file, int* translation, FILE* output)
{
  unsigned char b[3];

  while (true)
  {
    int rc = fread(b, sizeof(b), 1, file);
    if (rc == 0) break;
    int k = 0;
    char* t = (char*) &k;
    memcpy(&t[0], &b[0], sizeof(char)*3);
    int v;
    if (k == 0xffffff)
      v = 0xffffff;
    else
      v = translation[k%17];
    char* p = (char*) &v;
    // printf("%u %u %u\n", b[0], b[1], b[2]);
    // printf("%x -> %x\n", k, v);
    fwrite(&p[0], sizeof(char), 3, output);
  }

  if (!feof(file))
    return false;

  return true;
}
