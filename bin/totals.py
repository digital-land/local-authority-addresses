#!/usr/bin/env python3

import sys
import csv
import json

postcode = {}
fieldnames = ["postcode", "ONSUD", "ONSPD"]

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

    for row in csv.DictReader(open("var/uprn.csv")):
        total["all"] += 1

        # only look at BPLUs with ONSUD entry
        if row["ONSUD"] == "":
            total["missing-onsud"] += 1
            continue

        # skip addresses outside of England
        if row["ONSUD"][0] != "E":
            if row["ONSPD"][0:1] == "E":
                total["adopted"] += 1
            continue

        total["england"] += 1

        # compare ONSUD and ONSPD
        if row["ONSPD"] == "":
            total["missing-onspd"] += 1
        elif row["ONSUD"] == row["ONSPD"]:
            total["same"] += 1
        else:
            total["different"] += 1

            if row["ONSUD"][0:1] != row["ONSPD"][0:1]:
                total["exiled"] += 1

    print(json.dumps(total, sort_keys=True, indent=4))
