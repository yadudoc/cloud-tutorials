
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include "src/rgb_histogram.h"

bool
rgb_histogram(FILE* file, int* histogram)
{
  memset(histogram, '\0', 256*sizeof(int));

  unsigned char b[3];

  while (true)
  {
    int rc = fread(b, sizeof(char), 3, file);
    if (rc == 0) break;
    histogram[b[0]]++;
  }

  if (!feof(file))
    return false;

  return true;
}
