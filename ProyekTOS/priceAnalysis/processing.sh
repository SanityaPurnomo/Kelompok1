#!/bin/bash

sources=$1".txt";
source1=$1"1.txt";
source2=$1"2.txt";

awk -F '{"name":' '{for(i=2 ; i <= NF ; i++) {print $i}}' $sources | grep "Cabe Merah Keriting" | sed 's/[{}"]//g' | sed 's/,/| /g' | sed 's/series://g' | sed 's/[0-9][0-9]://g' | sed 's/[0-9]://g' | awk -F'|' '{for(i=8 ; i<NF ; i++){printf("%d\n",$i);}}' > $source1

awk -F '{"name":' '{for(i=2 ; i <= NF ; i++) {print $i}}' $sources | grep "Cabe Merah Besar" | sed 's/[{}"]//g' | sed 's/,/| /g' | sed 's/series://g' | sed 's/[0-9][0-9]://g' | sed 's/[0-9]://g' | awk -F'|' '{for(i=8 ; i<NF ; i++){printf("%d\n",$i);}}' > $source2
