# How to find the local authority for an address

[Guidance](https://digital-land.github.io/local-authority-addresses) to help people building a government or other public service determine the local authority which an individual property or premises resides.

This repository also includes some [analysis](https://digital-land.github.io/local-authority-addresses/analysis) of English UPRNs, local authority districts, and postcodes which was developed to inform the guidance.

The analysis uses a [spatialite](https://www.gaia-gis.it/fossil/libspatialite/index) database, built from the proprietary OS AddressBase Premium dataset combined with a number of open data sources.

<a href="https://www.flickr.com/photos/psd/50165771136/in/dateposted-public/" title="Spatialite schema"><img src="https://live.staticflickr.com/65535/50165771136_255fe99b5b_c.jpg" alt="Spatialite schema"></a>

The database can be explored using [datasette](https://datasette.readthedocs.io/en/stable/). There is a set of example queries in the accompanying Jupyter notebook.

# Data sources

The following data sources are downloaded by the build process:

  * [ONS National Statistics Postcode Lookup (ONSNSPL)](https://geoportal.statistics.gov.uk/search?collection=Dataset&sort=name&tags=all(PRD_NSPL))
  * [ONS Postcode Directory (ONSPD)](https://geoportal.statistics.gov.uk/search?collection=Dataset&sort=name&tags=all(PRD_ONSPD))
  * [ONS UPRN Directory (UD)](https://geoportal.statistics.gov.uk/search?collection=Dataset&sort=name&tags=all(PRD_ONSUD))
  * [OS OpenUPRN](https://osdatahub.os.uk/downloads/open/OpenUPRN)

AddressBase has to be ordered and manually downloaded from the OS data portal, and a copy saved in the cache directory:

  * [OS AddressBase Premium](https://www.ordnancesurvey.co.uk/business-government/products/addressbase-premium)

# Building the guidance and database

We recommend working in [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/) before installing the python dependencies:

    $ make init
    $ make

Downloading the data and building the database and indexes can take more than an hour on an modern laptop.
To just build the guidance and content:

    $ make docs

You can explore the data in a browser using datasette:

    $ make serve

# Licence

The software in this project is open source and covered by the [LICENSE](LICENSE) file.

Data from [Office for National Statistics](https://www.ons.gov.uk/methodology/geography/licences) is licensed under the [Open Government Licence v.3.0](http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).

UPRNs and their locations are published here under the [Open Government Licence v.3.0](http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/) as set out in the [OS Open ID policy](https://www.ordnancesurvey.co.uk/business-government/tools-support/open-mastermap-programme/open-id-policy).

Otherwise all content and data in this repository is
[© Crown copyright](http://www.nationalarchives.gov.uk/information-management/re-using-public-sector-information/copyright-and-re-use/crown-copyright/)
and available under the terms of the [Open Government 3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/) licence.
