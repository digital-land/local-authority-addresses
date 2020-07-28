#!/usr/bin/env python3

import os
import sys
import csv
from io import TextIOWrapper
from zipfile import ZipFile
import sqlite3

header = {}
connection = None
cursor = None

field = {
    "uprn": {"datatype": "INTEGER",},
    "parent_uprn": {"datatype": "INTEGER",},
    "postcode": {"datatype": "TEXT",},
    "custodian": {"datatype": "INTEGER",},
    "latitude": {"datatype": "REAL",},
    "longitude": {"datatype": "REAL",},
}

table = {
    "blpu": ["uprn", "parent_uprn", "postcode", "custodian", "latitude", "longitude"],
}

blpu_insert = "INSERT INTO {table} ({cols}) VALUES ({values});".format(
    table="blpu",
    cols=",".join(table["blpu"]),
    values=",".join(["?"] * len(table["blpu"])),
)


def load_headers(path, filename, record_identifier):
    with ZipFile(path) as z:
        with z.open(filename, "r") as f:
            row = next(csv.reader(TextIOWrapper(f, "utf-8")))
            header[record_identifier] = {row[i]: i for i in range(0, len(row))}


def load_zipfile(path):
    global count
    with ZipFile(path) as z:
        for info in z.infolist():
            print(info.filename)
            with z.open(info.filename, "r") as infile:
                blpu = []
                for row in csv.reader(TextIOWrapper(infile, "utf-8")):
                    if row[0] == "21":
                        # BLPU records in England
                        if row[1] == "I" and row[header["21"]["COUNTRY"]] == "E":
                            blpu.append(
                                (
                                    row[header["21"]["UPRN"]],
                                    row[header["21"]["PARENT_UPRN"]],
                                    row[header["21"]["POSTCODE_LOCATOR"]],
                                    row[header["21"]["LOCAL_CUSTODIAN_CODE"]],
                                    row[header["21"]["LATITUDE"]],
                                    row[header["21"]["LONGITUDE"]].replace("-.", "-0."),
                                )
                            )

                count = len(blpu)
                if count:
                    cursor.executemany(blpu_insert, blpu)
                    print(info.filename, count)
                connection.commit()


if __name__ == "__main__":
    load_headers(sys.argv[1], "Record_21_BLPU_Header.csv", "21")

    connection = sqlite3.connect(sys.argv[3])

    # add SpatialLite
    connection.enable_load_extension(True)
    connection.load_extension(os.environ["SPATIALITE_EXTENSION"])
    connection.execute("select InitSpatialMetadata(1)")

    # try and speed-up loading
    cursor = connection.cursor()
    cursor.execute("PRAGMA synchronous = OFF")
    cursor.execute("PRAGMA journal_mode = OFF")

    connection.execute(
        "CREATE TABLE IF NOT EXISTS {table}({cols});".format(
            table="blpu",
            cols=",".join(
                ["%s %s" % (col, field[col]["datatype"]) for col in table["blpu"]]
            ),
        )
    )

    connection.execute("SELECT AddGeometryColumn('blpu', 'point', 4326, 'POINT', 2);")

    print("loading ..")
    load_zipfile(sys.argv[2])

    print("committing ..")
    connection.commit()

    print("creating index ..")
    connection.execute(
        "CREATE INDEX IF NOT EXISTS blpu_index on blpu (uprn, postcode, custodian);"
    )

    # this is very slow
    print("creating spatial index ..")
    connection.execute('select CreateSpatialIndex("blpu", "point");')

    print("committing ..")
    connection.commit()
    connection.close()
