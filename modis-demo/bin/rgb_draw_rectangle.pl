#!/usr/bin/perl 

# Draw a rectangle on an RGB file
# Usage: draw_rectangle.pl infile.rgb xmin ymin xmax ymax outfile.rgb

my ($input_filename, $xres, $yres, $xmin, $ymin, $xmax, $ymax, $output_filename) = @ARGV;
open(FILE_INPUT, "$input_filename") || die "Unable to open $input_filename!";
open(FILE_OUTPUT, ">$output_filename") || die "Unable to create $output_filename";

# Read data three bytes at a time (RGB)
$/ = \3;
my $x=0, $y=0;
while(<FILE_INPUT>) {
   (my $red, my $green, my $blue) = unpack('C3', $_);

   # Left and right of rectangle, 2 pixels wide
   if ( $x == $xmin || $x == $xmin+1 || $x == $xmax || $x == $xmax-1 ) {
      if ( $y <= $ymax && $y >= $ymin ) { 
         $red="255"; $blue="0"; $green="0"; }
   } 

   # Top and bottom, 2 pixels high
   if ( $y == $ymin || $y == $ymin-1 || $y == $ymax || $y == $ymax-1 ) {
      if ( $x <= $xmax && $x >= $xmin ) { 
         $red="255"; $blue="0"; $green="0";
      }
   }
   
   print FILE_OUTPUT pack('C3', $red, $green, $blue);

   if($x == $xres-1) { $x = 0; $y++; } 
   else { $x++; }
}

close(FILE_INPUT);
close(FILE_OUTPUT);
