# AddressBase Premium collection and dataset

TBD: move this collection to the digital land pipeline

# Analysis

  * X% of postcodes in England overlap a local authority boundary, affecting Y% of addresses.
  * POSTCODE has addresses with the largest number of different custodians (LA1, LA2, ..)
  * POSTCODE has the largest number of addresses differing to ONSPD (X in LA1, Y in LA2)

# Data sources

  https://www.ordnancesurvey.co.uk/business-government/products/addressbase-premium
  https://geoportal.statistics.gov.uk/search?collection=Dataset&sort=name&tags=all(PRD_NSPL)
  https://geoportal.statistics.gov.uk/search?collection=Dataset&sort=name&tags=all(PRD_ONSPD)
  https://geoportal.statistics.gov.uk/search?collection=Dataset&sort=name&tags=all(PRD_ONSUD)

# Building the report

We recommend working in [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/) before installing the python dependencies:

    $ make init
    $ make

# Licence

The software in this project is open source and covered by LICENSE file.

Individual datasets copied into this repository may have specific [copyright](collection/attribution/) and [licensing](collection/licence/),
otherwise all content and data in this repository is
[© Crown copyright](http://www.nationalarchives.gov.uk/information-management/re-using-public-sector-information/copyright-and-re-use/crown-copyright/)
and available under the terms of the [Open Government 3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/) licence.
