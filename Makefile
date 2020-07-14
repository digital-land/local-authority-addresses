# sources
AB_ZIP=cache/AB76GB_CSV.zip
AB_HEADERS_CSV=cache/addressbase-premium-header-files.zip
ONSPD_ZIP=cache/ONSPD_MAY_2020_UK.zip
ONSUD_ZIP=cache/ONSUD_MAY_2020.zip
NSPL_ZIP=cache/NSPL_MAY_2020_UK.zip
OPENUPRN_ZIP=cache/OPENUPRN_2020_06.zip

DOWNLOADS=\
	$(AB_ZIP)\
	$(AB_HEADERS_CSV)\
	$(ONSPD_ZIP)\
	$(ONSUD_ZIP)\
	$(NSPL_ZIP)\
	$(OPENUPRN_ZIP)

all:	unpack-addressbase counts.txt

counts.txt:	unpack-addressbase
	wc -l var/*.csv > $@

unpack-addressbase:	var/BLPU.csv

var/BLPU.csv:	 bin/unpack-addressbase.py $(AB_ZIP) $(AB_HEADERS_CSV)
	@mkdir -p var/
	python3 bin/unpack-addressbase.py $(AB_HEADERS_CSV) $(AB_ZIP)

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

$(AB_HEADERS_CSV):
	curl -qsL 'https://www.ordnancesurvey.co.uk/documents/product-support/support/addressbase-premium-header-files.zip' > $@

init:

clean:

clobber:

prune:
