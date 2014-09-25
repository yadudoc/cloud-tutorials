#!/bin/bash

# Return a new modis files with the 0-16 pixel values changed to
# colors that reflect the land use of that region. (See legend)
#
# usage: colormodis.sh original.rgb recolored.rgb

infile=$1
outfile=$2
scale=${3-12}
xres=${4-2400}
yres=${5-2400}

BINDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Translation table - edit colors here
cat > translate.txt <<EOF
#000000 #2041b3
#010101 #006a0f
#020202 #007c25
#030303 #00a25b
#040404 #00a125
#050505 #069228
#060606 #9e9668
#070707 #c1c48f
#080808 #85aa5b
#090909 #b1b741
#0a0a0a #a4d07e
#0b0b0b #73abae
#0c0c0c #ccd253
#0d0d0d #d90000
#0e0e0e #9de36e
#0f0f0f #b6b5c2
#101010 #949494
EOF

$BINDIR/rgb_adjust_color.pl $infile translate.txt $outfile.tmp
$BINDIR/rgb_downscale.pl $outfile.tmp $xres $yres $scale $outfile
