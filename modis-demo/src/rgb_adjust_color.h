/*
 * rgb_adjust_color.h
 *
 *  Created on: Aug 1, 2013
 *      Author: wozniak
 */

#ifndef RGB_ADJUST_COLOR_H_
#define RGB_ADJUST_COLOR_H_

#include <stdbool.h>
#include <stdio.h>

bool
translate(FILE* file, int* translation, FILE* output);

#endif
