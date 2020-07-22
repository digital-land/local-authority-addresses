#!/bin/bash

echo "## CSV headers"
echo
echo "| File | Lines | Size |Columns |"
echo "| --- | --- | --- |--- |"
for file in $*
do
	lines=$(wc -l $file | cut -f1)
	size=$(du -h $file | cut -f1)
  case $file in
	*.csv) cols=$(head -1 $file | sed -e 's/,/, /g' -e 's///') ;;
	*) cols="";;
	esac
	echo "| $file | $lines | $size | $cols |"
done

