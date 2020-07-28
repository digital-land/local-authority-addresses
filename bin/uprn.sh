#!/bin/sh

csvcut -c "UPRN,POSTCODE_LOCATOR,LOCAL_CUSTODIAN_CODE,LONGITUDE,LATITUDE" - |

    # remove headers
    # fix broken real number values replacing "-." with "-0."
    sed -e '1d' -e 's/-\./-0./' | {

        # add headers
        echo "uprn,postcode,addressbase-custodian,longitude,latitude"

        # sort by UPRN
        sort -k1,1 -t, 
    }
