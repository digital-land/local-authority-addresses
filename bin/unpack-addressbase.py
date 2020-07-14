#!/usr/bin/env python3

# unpack AddressBase Premium ZIP into a CSV file for each table with headers


import sys
import csv
from io import TextIOWrapper
from zipfile import ZipFile

outdir = "./var/"

header = {}
writer = {}


def load_header(filename, reader):
    (_, record, name, _) = filename.split("_")
    fieldnames = next(reader)
    path = "%s%s.csv" % (outdir, name)
    writer[record] = csv.writer(open(path, "w"))
    writer[record].writerow(fieldnames)


def unpack_file(filename, reader):
    print(filename)
    for row in reader:
        writer[row[0]].writerow(row)


def zipfile(path, unpack):
    with ZipFile(path) as z:
        for info in z.infolist():
            with z.open(info.filename, "r") as infile:
                if not info.is_dir():
                    unpack(info.filename, csv.reader(TextIOWrapper(infile, "utf-8")))


if __name__ == "__main__":
    zipfile(sys.argv[1], load_header)
    zipfile(sys.argv[2], unpack_file)
    exit(0)
