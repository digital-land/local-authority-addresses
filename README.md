# Finding the local authority for an address

The aim of this analysis is to complete the following statements to support our guidance on how to find the local authority for an address:

  * X% of postcodes in England overlap a local authority boundary, affecting Y% of addresses.
  * POSTCODE has addresses with the largest number of different custodians (LA1, LA2, ..)
  * POSTCODE has the largest number of addresses differing to ONSPD (X in LA1, Y in LA2)

# Data sources

The following data sources are downloaded by the build process:

  * [ONS National Statistics Postcode Lookup (ONSNSPL)](https://geoportal.statistics.gov.uk/search?collection=Dataset&sort=name&tags=all(PRD_NSPL))
  * [ONS Postcode Directory (ONSPD)](https://geoportal.statistics.gov.uk/search?collection=Dataset&sort=name&tags=all(PRD_ONSPD))
  * [ONS UPRN Directory (UD)](https://geoportal.statistics.gov.uk/search?collection=Dataset&sort=name&tags=all(PRD_ONSUD))
  * [OS OpenUPRN](https://osdatahub.os.uk/downloads/open/OpenUPRN)

AddressBase has to be ordered and manually downloaded from the OS data portal, and a copy saved in the cache directory:

  * [OS AddressBase Premium](https://www.ordnancesurvey.co.uk/business-government/products/addressbase-premium)

# Methodology

AddressBase is used to find the postcode for an individual UPRN.

NSPL and ONSPD both assign a single local authority district to a postcode, the difference being [the method used](https://www.ons.gov.uk/methodology/geography/geographicalproducts/postcodeproducts) to relate a postcode to a local authority. ONSPD uses a geospatial method to match a central location for the postcode within the local authority district boundary, whilst NSPL ensures statistics are consistent in their geographical hierarchy.

# Building the report

We recommend working in [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/) before installing the python dependencies:

    $ make init
    $ make

# Licence

The software in this project is open source and covered by the [LICENSE](LICENSE) file.

Data from [Office for National Statistics](https://www.ons.gov.uk/methodology/geography/licences) is licensed under the [Open Government Licence v.3.0](http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).

UPRNs and their locations are published here under the [Open Government Licence v.3.0](http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/) as set out in the [OS Open ID policy](https://www.ordnancesurvey.co.uk/business-government/tools-support/open-mastermap-programme/open-id-policy).

Otherwise all content and data in this repository is
[© Crown copyright](http://www.nationalarchives.gov.uk/information-management/re-using-public-sector-information/copyright-and-re-use/crown-copyright/)
and available under the terms of the [Open Government 3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/) licence.
