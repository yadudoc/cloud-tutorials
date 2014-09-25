#!/bin/bash

# topselected.txt
topselected=$1

# selectedtiles.txt
selectedtiles=$2

# Replace usetype name with number
usetype=$( echo $3 | sed            \
           -e s/water/0/g           \
           -e s/evergreenneedle/1/g \
           -e s/evergreenlead/2/g   \
           -e s/deciduousneedle/3/g \
           -e s/deciduousleaf/4/g   \
           -e s/mixedforest/5/g     \
           -e s/closedshrub/6/g     \
           -e s/openshrub/7/g       \
           -e s/woody/8/g           \
           -e s/savanna/9/g         \
           -e s/grassland/10/g      \
           -e s/wetland/11/g        \
           -e s/cropland/12/g       \
           -e s/urban/13/g          \
           -e s/vegetartion/14/g    \
           -e s/ice/15/g            \
           -e s/barren/16/g         \
           -e s/unclassified/17/g
         )

# Max limit to analyze
maxnum=$4

# Write topselected.txt
result=$( grep " $usetype " $( eval echo $5 ) | sed s/':'/' '/g | sort -rnk2 | awk '{print $1 " " $2}' | head -$maxnum )
echo "$result" > $topselected
   
# Write selectedtiles.txt
for r in $( echo "$result" | awk '{print $1}' )
do
   echo $( basename $r ).rgb |sed s/\.landuse\.byfreq//g >> $selectedtiles
done
exit 0
