/*
 * rgb_histogram.h
 *
 *  Created on: Aug 1, 2013
 *      Author: wozniak
 */

#ifndef RGB_HISTOGRAM_H
#define RGB_HISTOGRAM_H

#include <stdbool.h>

/**
   @param histogram OUT histogram[color]=<count of that color>
                        Size of histogram is 256
   @return True; false on error
 */
bool rgb_histogram(FILE* file, int* histogram);

#endif
