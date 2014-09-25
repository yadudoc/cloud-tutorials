#!/usr/bin/perl 

# Usage: rgb_adjust_color.pl input.rgb table.txt output.rgb

my ($input_filename, $translation_table, $output_filename) = @ARGV;
open(FILE_INPUT, "$input_filename") || die "Unable to open $input_filename!";
open(FILE_OUTPUT, ">$output_filename") || die "Unable to create $output_filename";

# Read translation table into a hash
my %tr_table = ();
open(TRANSLATION_TABLE, "$translation_table") || die "Unable to open $translation_table";
while(<TRANSLATION_TABLE>) {
   my ($from, $to) = split;
   $tr_table{lc($from)} = lc($to);
}

# Read data
$/ = \3;
while(<FILE_INPUT>) {
   my $hex = lc(sprintf ("#%2.2X%2.2X%2.2X", unpack('C3', $_)));

   if(defined($tr_table{$hex})) { 
      my $new_value = $tr_table{$hex};
      print FILE_OUTPUT pack('C3', 
                             hex(substr($new_value,1,2)),
                             hex(substr($new_value,3,2)),
                             hex(substr($new_value,5,2))
      );
   } 

   else { print FILE_OUTPUT $_; }
}

close(FILE_INPUT);
close(FILE_OUTPUT);
