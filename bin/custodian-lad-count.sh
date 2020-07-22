#!/bin/sh

columns="addressbase-custodian,ONSUD,ONSPD"

echo "$columns,count"
csvcut -c "$columns" |
  sed 1d |
  sort |
  uniq -c |
  sed 's/^ *\([0-9][0-9]*\)  *\(.*$\)/\2,\1/'
