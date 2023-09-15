#!/usr/bin/perl
# RC_i7s.pl
# by Nate Campbell
# reverse complement i7 sequence in GT-seq BC-split input file

use strict; use warnings;

open (FILE, "<$ARGV[0]") or die "Error opening BC-split input file $ARGV[0]\n";

while (<FILE>) {
	chomp;
	if ($. == 1) {
		print "$_\n";
		}
	if ($. > 1) {
		my @info = split ",", $_;
		my $new_i7 = reverse($info[3]);
		$new_i7 =~ tr/ACGT/TGCA/;
		print "$info[0],$info[1],$info[2],$new_i7,$info[4],$info[5]\n";
		}
	}
close FILE;
		
