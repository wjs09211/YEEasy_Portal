#!/usr/bin/perl
use strict;
use warnings;

if($#ARGV != 0){
	print "can't not open file\n";
	exit 4;
	}

open(INFILE, $ARGV[0]) or die "Cannot open file\n";

my $count = 0;
my @arr;
my $len;
my $Start;
my $end;
while(my $out = <INFILE>){
	chomp $out;
	if($out=~/<(td class='record2'>)|(<td class='hi_line'>)|(<\/td>\s*$)/){
		if($out!~/(>\s*<\/td>\s*$)|(^<td.*\d\s*<\/td>\s*$)|(^\s*<\/td>\s*$)|([^\s]<\/td>\s*$)|(^<td.*\s*<\/td>\s*$)/){
			#print "$out\n";
			push @arr, $out;
			$count++;	
		}
	}
}
print "The number is $count\n";
for(my $p = 0;$p < $count;$p++){
	$len =length $arr[$p];
	$Start = index($arr[$p], "\'>");
	$end = index($arr[$p], "<\/td>");
	#$end = index($arr[$p], "<", $end+1);
	my $pp;
	if($Start == -1){
	$pp =  substr($arr[$p],0,$end - $Start-1);
	}
	else{
	$pp = substr($arr[$p],$Start+3,$end - $Start-3);
	}
	print "$pp\n";
}

close INFILE;
