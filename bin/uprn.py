#!/usr/bin/env python3

import sys
import csv

postcode = {}
uprn = {}
fieldnames = ["uprn", "postcode", "addressbase-custodian", "ONSUD", "ONSPD"]


if __name__ == "__main__":

    print("reading postcode .. ")
    for row in csv.DictReader(open("var/postcode.csv")):
        postcode[row["postcode"]] = row["ONSPD"]

    print("reading BLPU .. ")
    for row in csv.DictReader(open("var/AddressBase/BLPU.csv")):
        uprn[row["UPRN"]] = {
            "uprn": row["UPRN"],
            "postcode": row["POSTCODE_LOCATOR"],
            "addressbase-custodian": row["LOCAL_CUSTODIAN_CODE"],
            "ONSPD": postcode.get(row["POSTCODE_LOCATOR"], ""),
        }

    print("reading ONSUD .. ")
    for row in csv.DictReader(open("var/ONSUD.csv")):
        key = row["uprn"]
        uprn.setdefault(key, {})
        uprn[key]["ONSUD"] = row["local-authority-district"]

    print("writing .. ")
    writer = csv.DictWriter(open("var/uprn.csv", "w", newline=""), fieldnames=fieldnames)
    writer.writeheader()

    for uprn, row in uprn.items():
        writer.writerow(row)
