# Independent analysis of COVID-19 data

Starting with rolling sums of weekly death counts to see if the data matches what people say about it.

## Dataset

Weekly death counts by jurisdiction and cause group pulled from the CDC website at https://data.cdc.gov/NCHS/Weekly-counts-of-death-by-jurisdiction-and-cause-o/u6jv-9ijr

## Approach

Keeping it simple to start
1. Group by jurisdiction and week end date only, just sum all cause groups for now
2. Separate states/jurisdictions from the country as a whole
3. Calculate rolling sums of 2, 4, 13, 26, and 52 weeks for some insight into the gravity of the current situation.

TODO:
1. Add trend line
2. Adjust for population growth
3. Add data prior to 2015
4. Start looking into cause groups
5. Try and find ICU capacity data and compare with flu 2018
