.PHONY: init data report clean clobber prune

# sources
ORGANISATION_CSV=var/organisation.csv
AddressBase_ZIP=cache/AB76GB_CSV.zip
AddressBase_HEADERS_CSV=cache/addressbase-premium-header-files.zip
AddressBase_CUSTODIANS_ZIP=cache/addressbase-local-custodian-codes.zip
CODEPO_ZIP=cache/codepo_gb.zip
ONSPD_ZIP=cache/ONSPD_MAY_2020_UK.zip
ONSUD_ZIP=cache/ONSUD_MAY_2020.zip
NSPL_ZIP=cache/NSPL_MAY_2020_UK.zip
OPENUPRN_ZIP=cache/OPENUPRN_2020_06.zip

DOWNLOADS=\
	$(ORGANISATION_CSV)\
	$(AddressBase_ZIP)\
	$(AddressBase_HEADERS_CSV)\
	$(AddressBase_CUSTODIANS_ZIP)\
	$(ONSPD_ZIP)\
	$(ONSUD_ZIP)\
	$(NSPL_ZIP)\
	$(OPENUPRN_ZIP)\
	$(CODEPO_ZIP)

AddressBase_DATA=\
	var/AddressBase/BLPU.csv\
	var/AddressBase/CLASSIFICATION.csv\
	var/AddressBase/DELIVERYPOINTADDRESS.csv\
	var/AddressBase/HEADER.csv\
	var/AddressBase/LPI.csv\
	var/AddressBase/METADATA.csv\
	var/AddressBase/ORGANISATION.csv\
	var/AddressBase/STREET.csv\
	var/AddressBase/STREETDESCRIPTOR.csv\
	var/AddressBase/SUCCESSOR.csv\
	var/AddressBase/TRAILER.csv\
	var/AddressBase/XREF.csv

# published data
DATA=\
	var/README.md\
	data/totals.json

# working data
# -- too big, or proprietary to publish
VAR=\
	$(AddressBase_DATA)\
	var/organisation.csv\
	var/uprn.csv\
	var/organisation.csv\
	var/osopenuprn.csv\
	var/codepo.csv\
	var/NSPL.csv\
	var/ONSPD.csv\
	var/ONSUD.csv\
	var/postcode.csv\
	var/custodian-lad-count.csv\
	var/postcode-uprn-count.csv\
	var/postcode-lad-uprn-count.csv\
	var/postcode-lad-count.csv

all:	data report

report:	report.md

report.md:	data/totals.json bin/report.py
	python3 bin/report.py < data/totals.json > $@

data:	$(DATA)

# working data index
var/README.md:	$(VAR) bin/index.sh
	bin/index.sh $(VAR) > $@

# totals 
data/totals.json:	var/uprn.csv bin/totals.py
	python3 bin/totals.py var/totals.csv > $@

# count of UPRNs for custodian/LAD combinations
# addressbase-custodian,ONSUD,ONSPD,count
var/custodian-lad-count.csv:	var/uprn.csv bin/custodian-lad-count.sh
	bin/custodian-lad-count.sh < var/uprn.csv > $@

# count of UPRNs for each postcode
# count,postcode
var/postcode-uprn-count.csv:	var/uprn.csv bin/postcode-uprn-count.sh
	bin/postcode-uprn-count.sh < var/uprn.csv > $@

# count of URRNs for LAD combinations
#postcode,ONSPD,ONSUD,count
var/postcode-lad-uprn-count.csv:	var/uprn.csv bin/postcode-lad-uprn-count.sh
	bin/postcode-lad-uprn-count.sh < var/uprn.csv > $@

# count of LADs for each postcode
var/postcode-lad-count.csv:	var/postcode-uprn-count.csv bin/postcode-lad-count.sh
	bin/postcode-lad-count.sh < var/postcode-uprn-count.csv > $@

# list of postcodes
# postcode,codepo,ONSPD,NSPL
var/postcode.csv:	var/NSPL.csv var/ONSPD.csv var/codepo.csv bin/postcode.py
	@mkdir -p data
	python3 bin/postcode.py

# uprn,postcode,addressbase-custodian,ONSUD,ONSPD
var/uprn.csv:	var/AddressBase/BLPU.csv var/ONSUD.csv bin/uprn.py
	@mkdir -p data
	time python3 bin/uprn.py

# unpack AddressBase into a file for each record type
$(AddressBase_DATA):	 bin/unpack-addressbase.py $(AddressBase_ZIP) $(AddressBase_HEADERS_CSV)
	@mkdir -p var/
	python3 bin/unpack-addressbase.py $(AddressBase_HEADERS_CSV) $(AddressBase_ZIP)

# postcode,local-authority-district
var/NSPL.csv:	$(NSPL_ZIP)
	unzip -p $(NSPL_ZIP) 'Data/*.csv' | csvcut -c pcds,laua | sed -e '1{s/pcds,laua/postcode,local-authority-district/}' -e '/^pcds,/d' > $@

var/ONSPD.csv:	$(ONSPD_ZIP)
	unzip -p $(ONSPD_ZIP) 'Data/*.csv' | csvcut -c pcds,oslaua | sed -e '1{s/pcds,oslaua/postcode,local-authority-district/}' -e '/^pcds,/d' > $@

var/ONSUD.csv:	$(ONSUD_ZIP)
	unzip -p $(ONSUD_ZIP) 'Data/*.csv' | csvcut -c uprn,lad19cd | sed -e '1{s/uprn,lad19cd/uprn,local-authority-district/}' -e '1!{/^uprn,/d;}' > $@

var/codepo.csv:	$(CODEPO_ZIP)
	unzip -p $(CODEPO_ZIP) 'Data/CSV/*.csv' | csvcut -c 1,3,4,9 | sed -e '1i postcode,easting,northing,local-authority-district' > $@

# OS published CSV file contains an invalid BOM
var/osopenuprn.csv:	$(OPENUPRN_ZIP)
	unzip -p $(OPENUPRN_ZIP) '*.csv' | sed '1s/^\xEF\xBB\xBF//' | csvcut -c UPRN,LATITUDE,LONGITUDE | sed -e '1{s/UPRN,LATITUDE,LONGITUDE/uprn,latitude,longitude/}' > $@

download: $(DOWNLOADS)

# https://geoportal.statistics.gov.uk/datasets/ons-postcode-directory-may-2020
$(ONSPD_ZIP):
	@mkdir -p ./cache
	curl -qsL 'https://www.arcgis.com/sharing/rest/content/items/fb894c51e72748ec8004cc582bf27e83/data' > $@

# https://geoportal.statistics.gov.uk/datasets/ons-uprn-directory-may-2020
$(ONSUD_ZIP):
	@mkdir -p ./cache
	curl -qsL 'https://www.arcgis.com/sharing/rest/content/items/68879b4d8da545a395a8bc8b95572e7d/data' > $@

# https://geoportal.statistics.gov.uk/datasets/national-statistics-postcode-lookup-may-2020
$(NSPL_ZIP):
	@mkdir -p ./cache
	curl -qsL 'https://www.arcgis.com/sharing/rest/content/items/ab73ec2e38c04599b64b09b3fa1c3333/data' > $@

# https://osdatahub.os.uk/downloads/open/OpenUPRN
$(OPENUPRN_ZIP):
	@mkdir -p ./cache
	curl -qsL 'https://api.os.uk/downloads/v1/products/OpenUPRN/downloads?area=GB&format=CSV&redirect' > $@

# https://www.ordnancesurvey.co.uk/business-government/tools-support/addressbase-premium-support
$(AddressBase_HEADERS_CSV):
	@mkdir -p ./cache
	curl -qsL 'https://www.ordnancesurvey.co.uk/documents/product-support/support/addressbase-premium-header-files.zip' > $@

# https://www.ordnancesurvey.co.uk/business-government/tools-support/addressbase-premium-support
$(AddressBase_CUSTODIANS_ZIP):
	@mkdir -p ./cache
	curl -qsL 'https://www.ordnancesurvey.co.uk/documents/product-support/support/addressbase-local-custodian-codes.zip' > $@

$(CODEPO_ZIP):
	@mkdir -p ./cache
	curl -qsL 'https://api.os.uk/downloads/v1/products/CodePointOpen/downloads?area=GB&format=CSV&redirect' > $@

$(ORGANISATION_CSV):
	@mkdir -p ./data
	curl -qsL 'https://raw.githubusercontent.com/digital-land/organisation-dataset/master/collection/organisation.csv' > $@

init:
	pip3 install -r requirements.txt

clean:

clobber:

prune:
	rm -rf ./cache ./var ./data
