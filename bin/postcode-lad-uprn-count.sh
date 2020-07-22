#!/bin/sh

columns="postcode,ONSPD,ONSUD"

echo "$columns,count"
csvcut -c "$columns" |
  sed 1d |
  sort |
  uniq -c |
  sed 's/^ *\([0-9][0-9]*\)  *\(.*$\)/\2,\1/'
