#!/usr/bin/perl
use strict;
use warnings;
use Encode qw(encode decode);
use utf8;
no utf8;


if($#ARGV != 0){
	print "input not found\n";
	exit 4;
}

open(INFILE, $ARGV[0]) or die "Cannot open file\n";

my $count = 0;
my @arr;
my $isload = 0;
my $count_poc = 0;
my @poc;
my $load_buf;
while(my $out = <INFILE>){#Ū�Ҫ��� 

	if($isload == 1){
		push @arr, $out;
		$count++;
		if($out=~/<\/td>\s*$/){
			$isload = 0;
		}
	}
	if($out=~/<\/tr><tr class="record2">/){
		$isload = 1;
	}
}
close INFILE;
for(my $p = 0;$p < $count;$p++){#�h���S�θ�� 
	#print "$arr[$p] ***ted***\n";
	$arr[$p] =~ s/<td align="left" valign="middle"><\/td>/*/g;
	$arr[$p] =~ s/<td valign="middle"><\/td>/*/g;
	$arr[$p] =~ s/<a.*<\/td>//g;
	$arr[$p] =~ s/<td.*target="_top">//g;
	#print "$arr[$p]\n";
}
for(my $p = 0;$p <= $count;$p++){#�C��C�P��ƦX���@�r�� 
	if($p == $count or $arr[$p]=~/<td class="hi_line" valign="middle">/){
		push @poc, $load_buf;
		$count_poc++;
		$load_buf = "";
	}
	else{
		$load_buf = $load_buf.$arr[$p];
	}
}
printf "%32s%32s%32s%32s%32s%32s\n","Monday","Tuesday","Wendnesday","Thursday","Friday","Saturday";#�L�P 
for(my $q = 1; $q < $count_poc;$q++){
	$poc[$q] =~ s/\s+//g;#�h�ť� 
	#print "$poc[$q]\n";
	my $len = length $poc[$q];
	my $start;
	my $time;
	my @week;
	$start = index($poc[$q],"<\/td>");#-------------------- 
	$time = substr($poc[$q],0,$start);#���X�Ұ�ɶ� 
	$poc[$q] = substr($poc[$q],$start + 5);#--------------- 
	$poc[$q] =~ s/<\/td>//g;#�h�S�θ�� 
	#print "+++++++++++++++++++++++++++\n";
	print "$time\n";#�L�ɶ� 
	#print "+++++++++++++++++++++++++++\n";
	while($len != 0){#���X�o��ҨC�P�Ұ� 
		my $eat = substr($poc[$q],0,1);
		if($eat eq "*"){
			push @week,"no";
			$poc[$q] = substr($poc[$q],1);
		}
		else{
			$start = index($poc[$q],"<\/a>");
			$eat = substr($poc[$q],0,$start);
			push @week,$eat;
			$poc[$q] = substr($poc[$q],$start +4);
		}
		$len = length $poc[$q];
	}
	#printf "%30s"," ";
	for(my $t =0;$t < 6;$t++){
		#$week[$t] =~ s/\s+//g;
		#$week[$t] = encode("utf8",$week[$t]);
#		utf8::encode($week[$t]);		
		$len = length $week[$t];#���o�r����� 
		#print "\n+++++++++++++++++++++++++++++++++\n";
		#print "$len\n";
		my $len_notchar = $week[$t]=~ tr/[0-9a-zA-Z]/[0-9a-zA-Z]/ + 2;#���o�D����r�r�� 
		#print "\n++++++++++++++++++++++++++++++++\n";
		#print "$len\t";
		#if($len > 30){
		#	$len =14 +  ($len-14)/5;	
		#}
		#for(my $l = 0;$l < 32 - $len;$l++){
		#	print " ";
		#}
		#print "%$len"."s\n";
		if($len > 2){
			my $len_buf =$len_notchar + ($len -$len_notchar)/3;#���o�u��r�� 
			#print "\n++++++++++++++++++\n";
			#print "$len_buf\n";
			#print "\n++++++++++++++++++\n";
			$len =$len + (32 - $len_buf) - ($len_buf - $len_notchar); #���o�ƪ����� 
			#$len = $len + 10;
			#my $qq = $len -32;
			#print"\n";
			#print "%$len"."s\n";
			printf "%$len"."s",$week[$t];
			#print "$week[$t]\t";
		}
		else{
		my $ten = 32;
		printf "%$ten"."s",$week[$t];
		#print "$week[$t]\t";
		}
	}
	print "\n";
}


print "**********************************\n";
#for(my $r = 1;$r < $count_poc;$r++){
#	$poc[$r] =~ s/\s+//g;
#	#$poc[$r] =~ s/<\/td>//;
#	print "$poc[$r]\n\n\n";
#}
print "**********************************\n";

