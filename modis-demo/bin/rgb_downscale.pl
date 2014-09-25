#!/usr/bin/perl 

# Downscale an rgb image
# Usage: rgb_downscale.pl input.rgb xres yres scalefactor output.rgb

sub array_avg {
    my $result=0;
    foreach(@_){ $result += $_; }
    return int($result/@_);
}

my ($input_filename, $xres, $yres, $scalefactor, $output_filename) = @ARGV;

open(FILE_OUTPUT, ">$output_filename") || die "Unable to write to $output_filename!";
open(FILE_INPUT, "$input_filename") || die "Unable to open $input_filename!";
local $/;
my @values = unpack('C*', <FILE_INPUT>);
close(FILE_INPUT);

my $x=0, $y=0;
while($y < $yres) {
   my (@reds, @greens, @blues) = ();

   foreach my $yloc ($y..$y+($scalefactor-1)) {
      foreach my $xloc ($x..$x+($scalefactor-1)) {
         my $index = ($yloc * $xres + $xloc) * 3;
         push(@reds, $values[$index]);
         push(@greens, $values[$index+1]);
         push(@blues, $values[$index+2]);         
      }
   }

   my $red = &array_avg(@reds);
   my $green = &array_avg(@greens);
   my $blue = &array_avg(@blues);
   print FILE_OUTPUT pack('C3', $red, $green, $blue);

   if( ($x+$scalefactor) >= $xres ) { $x = 0; $y += $scalefactor; } 
   else { $x += $scalefactor; }
}

close(FILE_INPUT);
close(FILE_OUTPUT);
