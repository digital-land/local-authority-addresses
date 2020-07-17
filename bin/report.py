#!/usr/bin/env python3

# X% of postcodes in England overlap a local authority boundary, affecting Y% of addresses.
# POSTCODE has addresses with the largest number of different custodians (LA1, LA2, ..)
# POSTCODE has the largest number of addresses differing to ONSPD (X in LA1, Y in LA2)

import sys
import json

if __name__ == "__main__":
    
    total = json.load(sys.stdin)

    total["different-percent"] = 100 * total["different"] / total["england"]

    print(f"""There are {total["all"]:,} UPRNs listed in AddressBase,
{total["england"]:,} of which are in England.
{total["missing-onsud"]:,} of these UPRNs are missing from ONSUD and
{total["missing-onspd"]:,} have a postcode which is not listed in ONSPD.

{total["same"]:,} UPRNs have an ONSUD entry where the Local Authority District
which matches the one assigned to the postcode in ONSPD, but in
{total["different"]:,} cases they differ, representing {total["different-percent"]:.2f}% of addresses in England.

There are 
{total["adopted"]:,} Welsh and Scottish UPRNs where the ONSPD assigned Local Authority District is in England,
and there are
{total["exiled"]:,} English UPRNs where the ONSPD assigned Local Authority District in Scotland or Wales.
""".format(total=total))
