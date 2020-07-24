#!/usr/bin/env python3

import sys
import csv
import json

postcode = {}
fieldnames = ["postcode", "onsud", "onspd"]

total = {
    'all': 0,
    'england': 0,
    'same': 0,
    'different': 0,
    'adopted': 0,
    'exiled': 0,
    'missing-onsud': 0,
    'missing-onspd': 0,
}

if __name__ == "__main__":

    for row in csv.DictReader(open("var/postcode-uprn.csv")):
        total["all"] += 1

        # only look at BPLUs with ONSUD entry
        if row["onsud"] == "":
            total["missing-onsud"] += 1
            continue

        # skip addresses outside of England
        if row["onsud"][0] != "E":
            if row["onspd"][0:1] == "E":
                total["adopted"] += 1
            continue

        total["england"] += 1

        # compare onsud and onspd
        if row["onspd"] == "":
            total["missing-onspd"] += 1
        elif row["onsud"] == row["onspd"]:
            total["same"] += 1
        else:
            total["different"] += 1

            if row["onsud"][0:1] != row["onspd"][0:1]:
                total["exiled"] += 1

    print(json.dumps(total, sort_keys=True, indent=4))
