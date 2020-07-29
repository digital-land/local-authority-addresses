#!/usr/bin/env python3

# create a spatialite database for analysing local authority addresses
# - TBD: move to use simonw's tools

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
        CREATE TABLE geography (
            geography TEXT PRIMARY KEY,
            name TEXT
        );
        """
    )

    connection.execute(
        """
        CREATE TABLE custodian (
            custodian INTEGER PRIMARY KEY,
            name TEXT
        );
        """
    )

    connection.execute(
        """
        CREATE TABLE organisation (
            organisation TEXT PRIMARY KEY,
            name TEXT,
            custodian INTEGER,
            geography TEXT,

            FOREIGN KEY (custodian) REFERENCES custodian (custodian)
            FOREIGN KEY (geography) REFERENCES geography (geography)
        );
        """
    )

    connection.execute(
        """
        CREATE TABLE postcode (
            postcode TEXT PRIMARY KEY,
            codepo TEXT,
            onspd TEXT,
            nspl TEXT,
            longitude REAL,
            latitude REAL,

            FOREIGN KEY (codepo) REFERENCES geography (geography),
            FOREIGN KEY (onspd) REFERENCES geography (geography),
            FOREIGN KEY (nspl) REFERENCES geography (geography)
        );"""
    )

    connection.execute(
        """
        CREATE TABLE uprn (
            uprn INTEGER PRIMARY KEY,
            postcode TEXT,
            custodian INTEGER,
            longitude REAL,
            latitude REAL,
            onsud TEXT,

            FOREIGN KEY (postcode) REFERENCES postcode (postcode),
            FOREIGN KEY (custodian) REFERENCES custodian (custodian),
            FOREIGN KEY (onsud) REFERENCES geography (geography)
        );"""
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


def load_geography(cursor, path):
    print("loading %s" % path)
    for row in csv.DictReader(open(path, newline="")):
        cursor.execute(
            """
            INSERT INTO geography(geography, name)
            VALUES ("%s", "%s");
            """
            % (
                row["geography"],
                row["name"]
            )
        )

def load_custodian(cursor, path):
    print("loading %s" % path)
    for row in csv.DictReader(open(path, newline="")):
        cursor.execute(
            """
            INSERT INTO custodian(custodian, name)
            VALUES ("%s", "%s");
            """
            % (
                row["addressbase-custodian"],
                row["name"]
            )
        )

def load_organisation(cursor, path):
    print("loading %s" % path)
    for row in csv.DictReader(open(path, newline="")):
        cursor.execute(
            """
            INSERT INTO organisation(organisation, name, custodian, geography)
            VALUES ("%s", "%s", "%s", "%s");
            """
            % (
                row["organisation"],
                row["name"],
                row["addressbase-custodian"],
                row["statistical-geography"],
            )
        )


def load_postcode(cursor, path):
    print("loading %s" % path)
    for row in csv.DictReader(open(path, newline="")):
        cursor.execute(
            """
            INSERT INTO postcode(postcode, codepo, onspd, nspl)
            VALUES ("%s", "%s", "%s", "%s");
            """
            % (
                row["postcode"],
                row["codepo"],
                row["onspd"],
                row["nspl"],
            )
        )


def load_blpu(cursor, path):
    print("loading %s" % path)
    for row in csv.DictReader(open(path, newline="")):
        cursor.execute(
            """
            INSERT INTO uprn(uprn, postcode, custodian, onsud, longitude, latitude)
            VALUES ("%s", "%s", "%s", "%s", "%s", "%s");
            """
            % (
                row["uprn"],
                row["postcode"],
                row["addressbase-custodian"],
                row["onsud"],
                row["longitude"],
                row["latitude"],
            )
        )



if __name__ == "__main__":

    db = sys.argv[1]
    connection = open_connection(db)
    create_tables(connection)
    cursor = create_cursor(connection)

    load_geography(cursor, "var/geography.csv")
    commit(connection)

    load_custodian(cursor, "var/addressbase-custodian.csv")
    commit(connection)

    load_organisation(cursor, "var/organisation.csv")
    commit(connection)

    load_postcode(cursor, "var/postcode.csv")
    commit(connection)

    # load_blpu(cursor, "var/AddressBase/BLPU.csv")
    load_blpu(cursor, "tmp/uprn.csv")
    commit(connection)

    connection.close()
