#!/usr/bin/perl -w

# Input to this program should be a raw, greyscale RGB file
# Usage: rgb_histogram.pl myfile.rgb

my $image_filename = shift;
open(IMAGEFILE, "$image_filename") || die "Unable to open $image_filename!\n";
binmode IMAGEFILE;

my @pixelcount;
foreach my $count (0..255) { $pixelcount[$count] = 0; }

# Read values, three bytes at a time
$/ = \3; 
foreach(<IMAGEFILE>) {
   $pixelcount[unpack('C', $_)]++;
}
close(IMAGEFILE);

foreach my $count (0..255) {
   if($pixelcount[$count] == 0) { next; }
   printf("%d %d %02x\n", $pixelcount[$count], $count, $count);
}
