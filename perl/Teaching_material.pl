#!/usr/bin/perl
use strict;
use warnings;
use Term::ANSIColor qw(:constants);
$Term::ANSIColor::AUTORESET=1;

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
#my $red = "\033[0:31m";
while(my $out = <INFILE>){
	chomp $out;
	if($out=~/(<td class='record2'>)|(<td class='hi_line'>)|(<\/td>\s*$)/){
		#print "$out\n";
		#(^<td.*\d\s*<\/td>\s*$)
		#(>\s*<\/td>\s*$)
		#([^\s]<\/td>\s*$)
		if($out!~/(<\/a>\s*<\/td>\s*$)|(^\s*<\/td>\s*$)|(^<td class='hi_line' align='center'>\s*<\/td>\s*$)|(^<td class='record2' align='center'>\s*<\/td>\s*$)/){
#(^<td.*\s*<\/td>\s*$)
			#print "$out\n";
			push @arr, $out;
			$count++;	
		}
	}
}
close INFILE;
my @arr1;
my $arr_count = 0;
#print "The number is $count\n";
for(my $p = 10;$p < $count-1;$p++){
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
	#print "$pp***\n";
	push @arr1, $pp;
	$arr_count++;
}
#printf "%50s%50s\n","test","test";
my $index = 1;
for(my $i = 0;$i < $arr_count;$i++){
	if($i % 4 == 0){
		print MAGENTA "\n$index\t";
		$index++;
		print BLUE "schedule:";
		print " $arr1[$i]\n";
		#printf "%$len"."s",$arr1[$i];
	}
	if($i % 4 == 1){
		print "\t";
		print BLUE "outline:";
		print " $arr1[$i]\n";
		#printf "%$len"."s",$arr1[$i];
		#print "\n";
	}
	if($i % 4 == 2){
		print "\t";
		print BLUE "submit time:";
		print " $arr1[$i]\n";
	}
	if($i % 4 == 3){
		print "\t";
		print BLUE "download times:";
		print " $arr1[$i]\n";
	}
}



#close INFILE;
