#!/bin/sh

columns="postcode"

echo "count,$columns"
csvcut -c "$columns" |
  sed 1d |
  sort |
  uniq -c |
  sed 's/^ *\([0-9][0-9]*\)  *\(.*$\)/\1,\2/' |
  sort -rn
