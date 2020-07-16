# sources
ORGANISATION_CSV=var/organisation.csv
AB_ZIP=cache/AB76GB_CSV.zip
AB_HEADERS_CSV=cache/addressbase-premium-header-files.zip
AB_CUSTODIANS_ZIP=cache/addressbase-local-custodian-codes.zip
CODEPO_ZIP=cache/codepo_gb.zip
ONSPD_ZIP=cache/ONSPD_MAY_2020_UK.zip
ONSUD_ZIP=cache/ONSUD_MAY_2020.zip
NSPL_ZIP=cache/NSPL_MAY_2020_UK.zip
OPENUPRN_ZIP=cache/OPENUPRN_2020_06.zip

DOWNLOADS=\
	$(ORGANISATION_CSV)\
	$(AB_ZIP)\
	$(AB_HEADERS_CSV)\
	$(AB_CUSTODIANS_ZIP)\
	$(ONSPD_ZIP)\
	$(ONSUD_ZIP)\
	$(NSPL_ZIP)\
	$(OPENUPRN_ZIP)\
	$(CODEPO_ZIP)

all:	download unpack-addressbase var/addresses.csv counts.txt

counts.txt:	var/BLPU.csv
	wc -l var/*.csv > $@

unpack-addressbase:	var/BLPU.csv

var/BLPU.csv:	 bin/unpack-addressbase.py $(AB_ZIP) $(AB_HEADERS_CSV)
	@mkdir -p var/
	python3 bin/unpack-addressbase.py $(AB_HEADERS_CSV) $(AB_ZIP)

var/addresses.csv:	var/ONSUD.csv var/ONSPD.csv var/NSPL.csv var/CODEPO.csv

var/NSPL.csv:	$(NSPL_ZIP)
	unzip -p $(NSPL_ZIP) 'Data/*.csv' | csvcut -c pcds,laua | sed -e '1{s/pcds,laua/postcode,local-authority-district/}' -e '/^pcds,/d' > $@

var/ONSPD.csv:	$(ONSPD_ZIP)
	unzip -p $(ONSPD_ZIP) 'Data/*.csv' | csvcut -c pcds,oslaua | sed -e '1{s/pcds,oslaua/postcode,local-authority-district/}' -e '/^pcds,/d' > $@

var/ONSUD.csv:	$(ONSUD_ZIP)
	unzip -p $(ONSUD_ZIP) 'Data/*.csv' | csvcut -c uprn,lad19cd | sed -e '1{s/uprn,lad19cd/uprn,local-authority-district/}' -e '1!{/^uprn,/d;}' > $@

var/CODEPO.csv:	$(CODEPO_ZIP)
	unzip -p $(CODEPO_ZIP) 'Data/CSV/*.csv' | csvcut -c 1,3,4,9 | sed -e '1i postcode,northing,easting,local-authority-district' > $@

download: $(DOWNLOADS)

# https://geoportal.statistics.gov.uk/datasets/ons-postcode-directory-may-2020
$(ONSPD_ZIP):
	curl -qsL 'https://www.arcgis.com/sharing/rest/content/items/fb894c51e72748ec8004cc582bf27e83/data' > $@

# https://geoportal.statistics.gov.uk/datasets/ons-uprn-directory-may-2020
$(ONSUD_ZIP):
	curl -qsL 'https://www.arcgis.com/sharing/rest/content/items/68879b4d8da545a395a8bc8b95572e7d/data' > $@

# https://geoportal.statistics.gov.uk/datasets/national-statistics-postcode-lookup-may-2020
$(NSPL_ZIP):
	curl -qsL 'https://www.arcgis.com/sharing/rest/content/items/ab73ec2e38c04599b64b09b3fa1c3333/data' > $@

# https://osdatahub.os.uk/downloads/open/OpenUPRN
$(OPENUPRN_ZIP):
	curl -qsL 'https://api.os.uk/downloads/v1/products/OpenUPRN/downloads?area=GB&format=CSV&redirect' > $@

# https://www.ordnancesurvey.co.uk/business-government/tools-support/addressbase-premium-support
$(AB_HEADERS_CSV):
	curl -qsL 'https://www.ordnancesurvey.co.uk/documents/product-support/support/addressbase-premium-header-files.zip' > $@

# https://www.ordnancesurvey.co.uk/business-government/tools-support/addressbase-premium-support
$(AB_CUSTODIANS_ZIP):
	curl -qsL 'https://www.ordnancesurvey.co.uk/documents/product-support/support/addressbase-local-custodian-codes.zip' > $@

$(CODEPO_ZIP):
	curl -qsL 'https://api.os.uk/downloads/v1/products/CodePointOpen/downloads?area=GB&format=CSV&redirect' > $@

$(ORGANISATION_CSV):
	curl -qsL 'https://raw.githubusercontent.com/digital-land/organisation-dataset/master/collection/organisation.csv' > $@

init:

clean:

clobber:

prune:
