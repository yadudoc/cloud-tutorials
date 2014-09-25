#!/bin/bash

# markmap selectedTileFile outputMap
BINDIR=$(cd $(dirname $0); pwd)

tilefile=$1
outmap=$2
xres=721
yres=361

cp $BINDIR/world.rgb $outmap.step

cat $tilefile | while read f ; do
  hv=$(echo $f | sed -e 's,^.*/,,' -e 's/\..*//')
  h=$(echo $hv | sed -e 's/h//' -e 's/v..//' -e 's/^0//')
  v=$(echo $hv | sed -e 's/h..//' -e 's/v//' -e 's/^0//')
  $BINDIR/rgb_draw_rectangle.pl $outmap.step $xres $yres $(( $h * 20 )) $(( $v * 20 )) $(( $h * 20 + 20 )) $(( $v * 20 + 20)) $outmap.tmp
  mv $outmap.tmp $outmap.step
done

# Convert output to PNG
$BINDIR/rgb_to_png.py $outmap.step $xres $yres $outmap
rm $outmap.step
