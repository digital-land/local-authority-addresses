---
title: Finding the local authority for an address
---

This guidance is intended to help people building a government or other public service determine the local authority which an individual property or premises resides.


## Using the postcode

The postcode alone is insufficent information to find the local authority for many addresses.

The Office for National Statistics (ONS) publishes the National Statistics Postcode Lookup ([NSPL](https://geoportal.statistics.gov.uk/search?collection=Dataset&sort=name&tags=all(PRD_NSPL))) and ONS Postcode Directory (ONSPD) [datasets](https://www.ons.gov.uk/methodology/geography/geographicalproducts/postcodeproducts), which may be used to find a local authority district for a postcode when compiling statistics.

Similarly, Ordnance Survey (OS) publishes [Code Point Open](https://www.ordnancesurvey.co.uk/business-government/products/code-point-open), as open data, which is used in a number of third-party services such as [Mapit](https://mapit.mysociety.org/) and [Find that Postcode](https://findthatpostcode.uk/).

Code Point Open and ONSPD find the centre point of the set of addresses with the same postcode, and place that within a single local authority boundary. Whereas NSPL matches the postcode centre point to a lower geography, and uses a hierarchy of geographies to assign the postcode to a local authority.

This means that each postcode is assigned a single local authority. Unfortunately, nearly 387,000 or [1.2% of addresses](https://github.com/digital-land/local-authority-postcodes/blob/master/report.md) in England are in a different local authority district to the one assigned to the postcode by ONSPD. This includes more than 550 English addresses which are attributed to a Scottish or Welsh local authority when using the postcode alone. NSPL has similar issues.

Sources such as ONSPD and NSUL are designed for grouping data containing addresses when compiling statistics. They don’t indicate where addresses with the same postcode are in different local authority districts.


## Asking the user to provide the local authority

A service asking for information may ask the user to choose the local authority from a list of local authorities.

This approach places a burden on the user, and does not work well for many people or in many situations. Asking a user to provide the local authority is difficult for users providing information about a different address to where they live, and is particularly unreliable where the address is close to a local authority boundary. In such cases the user will either need to search for the answer elsewhere. The user will often resort to guessing an answer.


## Use the UPRN

To reliably direct a user to their local authority, or send data associated with a place to a local authority, you should use a gazetteer to find the [Unique Property Reference Number (UPRN)](https://www.gov.uk/government/publications/open-standards-for-government/identifying-property-and-street-information) for the address. You can then use the gazetteer, or another dataset to find the local authority for the UPRN.


### Using a gazetteer

Local authorities who have a statutory duty to number and name streets, maintain a [Local Land and Property Gazetteer (LLPG)](https://en.wikipedia.org/wiki/Local_Land_and_Property_Gazetteer). These are compiled by [GeoPlace LLP](https://www.geoplace.co.uk/) into the National Land and Property Gazetteer (NLPG), which is marketed by OS as a suite of [AddressBase](https://www.ordnancesurvey.co.uk/business-government/products/addressbase) products.

The data from one of the AddressBase products can be incorporated into your service, though this will require operational support as the data changes frequently, and is updated every 6 weeks. It is currently difficult to automate the process of ordering and updating a new copy of AddressBase data into a local database.

A service may be able to use [OS Places](https://developer.ordnancesurvey.co.uk/os-places-api), [Surrey Digital Services Address Lookup](https://surreydigitalservices.github.io/sds-addresses/), or one of the other APIs offered by companies on the Digital Marketplace. The privacy of the user and sensitivity of the addresses being looked-up should be considered when using a third-party API.


### Ask the user to select an address

A service with a user interface should follow the [address lookup pattern](https://design-system.service.gov.uk/patterns/addresses/) from the GOV.UK design system to help the user select an address from an address gazetteer.

A service asking a user for an address may have to resort to accepting lines of text for new-builds, and other places not yet listed in the gazetteer, in which case the text address will need to be matched by a separate, possibly manual process.

_Whilst we are aware of Geoplace LLP’s [find my address](https://www.findmyaddress.co.uk/search) service, the [OS Places API](https://developer.ordnancesurvey.co.uk/os-places-api), and [Surrey Digital Services ](https://surreydigitalservices.github.io/sds-addresses/)service,  there is no single, accessible address platform similar to GOV.UK Notify or Pay, which be quickly and cheaply used in government services which we can recommend._


### Match a text address to a gazetteer

Many historical datasets and registers contain text addresses without the UPRN. In such cases, each text address will need to be matched to the addresses in the gazetteer in order to find the corresponding UPRN.

A text address can be written in lots of different ways, with establishment, street, and place names often containing abbreviations, aliases, [exonyms, and endonyms](https://en.wikipedia.org/wiki/Exonym_and_endonym), all of which may change over time. These features, combined with typos and spelling mistakes make searching for an address in a gazetteer a relatively difficult task, subject to imprecision and error.


### Address matching precision

Searching a gazetteer with an imprecise text address may return multiple entries. For example, a number of business units in a shopping centre, or all the residential flats in an apartment block may share the same postal delivery, or street address, but will each have a separate entry in the gazetteer with a different UPRN.

It is not necessary to have a precise match of an address to a UPRN if it is only being used to find the local authority. But if the UPRN is to be used as an identifier to link to other datasets, then there will be a proportion of text addresses which will be ambiguous and imprecise.


### Providing feedback on failed matches

A service may require a manual process for dealing with failed matches, and possibly the ability to later contact the user, to resolve an issue with their address.

Missing addresses or other issues with the gazetteer should be reported back to the address custodian. Holders of a [Public Sector Geospatial Agreement (PSGA)](https://www.ordnancesurvey.co.uk/business-government/public-sector-geospatial-agreement) or other OS account may use the [TellOS](https://www.ordnancesurvey.co.uk/tellos/) form to report an issue with a UPRN.

_It is not clear how best to provide a custodian feedback on issues with lots of addresses at once._


### Bulk address matching services

Matching large datasets to a gazetteer is a specialist activity, requiring clerical work to make decisions on ambiguous and unknown addresses. ONS, GeoPlace and a number of other [companies listed on G-Cloud](https://www.digitalmarketplace.service.gov.uk/g-cloud/search) offer services to help match text addresses in bulk datasets.


### Find the local authority district from the UPRN

ONS periodically publishes a [National Statistics UPRN Lookup (NSUL)](https://geoportal.statistics.gov.uk/datasets/national-statistics-uprn-lookup-march-2020) dataset, a set of CSV files which can be used to translate a UPRN to various statistical geography codes, including the local authority district (LAD).

Alternatively, use AddressBase to find the custodian for the UPRN. [The Digital Land organisation dataset](https://digital-land.github.io/organisation/) has a mapping to find the organisation, and Local Authority District from the AddressBase custodian code.


## Finding the organisation, forum or hub for a local authority district

The LAD code identifies the jurisdiction of the local authority. A new code is issued when the boundary changes.

Digital Land provides a translation from the AddressBase custodian, and LAD code to GOV.UK [local-authority-eng](https://www.registers.service.gov.uk/registers/local-authority-eng) register identifier and other datasets on the Digital Land [organisation](https://digital-land.github.io/organisation/) pages.
