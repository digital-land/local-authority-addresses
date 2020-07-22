#!/usr/bin/env python3

import sys
import csv

postcode = {}
fieldnames = ["postcode", "codepo", "ONSPD", "NSPL"]


def load(name):
    for row in csv.DictReader(open("var/%s.csv" % (name))):
        key = row["postcode"].replace(" ", "")
        postcode.setdefault(key, {})
        postcode[key]["postcode"] = row["postcode"]
        postcode[key][name] = row["local-authority-district"]


if __name__ == "__main__":
    load("codepo")
    load("ONSPD")
    load("NSPL")

    writer = csv.DictWriter(open("var/postcode.csv", "w", newline=""), fieldnames=fieldnames)
    writer.writeheader()

    for postcode, row in sorted(postcode.items()):
        writer.writerow(row)
