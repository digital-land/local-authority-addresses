#!/usr/bin/env python3

import sys
import csv

postcode = {}
fieldnames = ["postcode", "codepo", "onspd", "nspl"]


def load(name):
    for row in csv.DictReader(open("var/%s.csv" % (name))):
        key = row["postcode"].replace(" ", "")
        postcode.setdefault(key, {})
        postcode[key]["postcode"] = row["postcode"]
        postcode[key][name] = row[name]


if __name__ == "__main__":
    load("codepo")
    load("onspd")
    load("nspl")

    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    writer.writeheader()

    for postcode, row in postcode.items():
        writer.writerow(row)
