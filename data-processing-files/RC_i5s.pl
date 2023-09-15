#!/usr/bin/perl
# RC_i5s.pl
# by Nate Campbell
# reverse complement i5 sequence in GT-seq BC-split input file

use strict; use warnings;

open (FILE, "<$ARGV[0]") or die "Error opening BC-split input file $ARGV[0]\n";

while (<FILE>) {
	chomp;
	if ($. == 1) {
		print "$_\n";
		}
	if ($. > 1) {
		my @info = split ",", $_;
		my $new_i5 = reverse($info[5]);
		$new_i5 =~ tr/ACGT/TGCA/;
		print "$info[0],$info[1],$info[2],$info[3],$info[4],$new_i5\n";
		}
	}
close FILE;
		
