#!/usr/bin/env python3

# create a spatialite database for analysing local authority addresses
# - could move to use simonw's tools

import os
import sys
import csv
import sqlite3


def open_connection(path):
    connection = sqlite3.connect(path)

    # SpatialLite extension
    connection.enable_load_extension(True)
    connection.load_extension(
        os.environ.get(
            "SPATIALITE_EXTENSION", "/usr/lib/x86_64-linux-gnu/mod_spatialite.so"
        )
    )
    connection.execute("select InitSpatialMetadata(1)")
    return connection


def create_tables(connection):
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS organisation (
            organisation TEXT PRIMARY KEY,
            name TEXT,
            custodian INTEGER,
            geography TEXT
        );

        CREATE TABLE IF NOT EXISTS geography (
            geography TEXT PRIMARY KEY,
            FOREIGN KEY (organisation) REFERENCES organisation (organisation)
        );

        CREATE TABLE IF NOT EXISTS postcode (
            postcode TEXT PRIMARY KEY,
            FOREIGN KEY (codepo) REFERENCES geography (geography),
            FOREIGN KEY (onsud) REFERENCES geography (geography),
            FOREIGN KEY (nspl) REFERENCES geography (geography),
            longitude REAL,
            latitude REAL
        );

        CREATE TABLE IF NOT EXISTS uprn (
            uprn INTEGER PRIMARY KEY,
            FOREIGN KEY (postcode) REFERENCES postcode (postcode)
            FOREIGN KEY (custodian) REFERENCES organisation (custodian)
            longitude REAL,
            latitude REAL
        );
        """
    )
    connection.execute("SELECT AddGeometryColumn('uprn', 'point', 4326, 'POINT', 2);")


def create_cursor(connection):
    cursor = connection.cursor()
    cursor.execute("PRAGMA synchronous = OFF")
    cursor.execute("PRAGMA journal_mode = OFF")
    return cursor


def commit(connection):
    print("committing ..")
    connection.commit()


def load_organisation(cursor, path):
    print("loading %s", path)
    for row in csv.DictReader(open(path, newline="")):
        cursor.execute(
            """
            INSERT INTO uprn(uprn, postcode, custodian, longitude, latitude)
            VALUES (%s, "%s", %s, %s, %s);
            """
            % (
                row["UPRN"],
                row["POSTCODE_LOCATOR"],
                row["LOCAL_CUSTODIAN_CODE"],
                row["LONGITUDE"].replace("-.", "-0."),
                row["LATITUDE"],
            )
        )


def load_blpu(cursor, path):
    print("loading %s", path)
    for row in csv.DictReader(open(path, newline="")):
        cursor.execute(
            """
            INSERT INTO uprn(uprn, postcode, custodian, longitude, latitude)
            VALUES (%s, "%s", %s, %s, %s);
            """
            % (
                row["UPRN"],
                row["POSTCODE_LOCATOR"],
                row["LOCAL_CUSTODIAN_CODE"],
                row["LONGITUDE"].replace("-.", "-0."),
                row["LATITUDE"],
            )
        )



if __name__ == "__main__":
    connection = open_connectuon("addresses.db")
    create_tables(connection)
    cursor = create_cursor(connection)

    load_organisation(cursor, "var/organisation.csv")
    #load_blpu(cursor, "var/AddressBase/BLPU.csv")
    load_blpu(cursor, "tmp/blpu.csv")
    commit(connection)

    connection.close()
