#!/usr/bin/perl
# add_indexSeqs.pl
# by Nate Campbell
# adds the index read sequences from i7 and i5 fastq files to the R1 (or R2) fastq file from the same run...
# provide the R1, i7, and i5 fastq files as command line arguments in that order

use strict; use warnings;

die "provide R1.fastq i7.fastq and i5.fastq files\n" unless @ARGV == 3;

my $file = "temp.fq";

`paste $ARGV[0] $ARGV[1] $ARGV[2] > $file`;

my $out = "$ARGV[0]";
$out =~ s/\..*/_indexed.fastq/;

open (OUT, ">$out") or die "Error opening output fastq file check permissions\n";

open (FASTQ, "<$file") or die "Error opening $file\n";

while (<FASTQ>) {
	my $infoline = $_;
	my $seqline = <FASTQ>;
	my $infoline2 = <FASTQ>;
	my $qual = <FASTQ>;
	my @infos = split "\t", $infoline;
	my @quals = split "\t", $qual;
	my @infos2 = split "\t", $infoline2;
	$infoline = $infos[0];
	chomp ($seqline);
	my @seqs = split "\t", $seqline;
	my @stuff = split ":", $infoline;
	pop(@stuff);
	$infoline = join ":", @stuff;
	$infoline = "$infoline:$seqs[1]\+$seqs[2]";
	print OUT "$infoline\n$seqs[0]\n+\n$quals[0]\n";
	if ($. % 4000000 == 0) {my $reads = $./4/1000000; print "$reads million reads completed\n";}
	}
close FASTQ;

`rm $file`;
