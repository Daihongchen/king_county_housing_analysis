# King County Housing Analysis

The goal of this project was to provide a baseline model for explaining variations in housing prices within King County.
In particular, we wanted to provide Real Estate Agents and home owners with a model including 4 features of homes that
most largely determine the sale price. This would then allow them to emphasize those particular features in their sales pitch
and maximize the value they get from selling their home.

## Environment Setup

Our environment.yml file can be found in the home page of this repo and should be installed prior to executing any code, as the libraries contained therein are necessary for execution.

## Data Collection, Storage, and Aggregation

First and foremost, we needed to collect our data. King County housing information can be found here: https://info.kingcounty.gov/assessor/DataDownload/default.aspx>

For the purposes of this project, we downloaded the Real Property Sales.zip, Residential Building.zip, Parcel.zip, and Lookup.zip

The documentation for this data can be found on the same website under .DOC files, which should be thoroughly reviewed prior to performing any statistical analysis. 

#### Storage

In order to perform analysis on our dataset we first needed it stored in a form capable of being manipulated. Even though the files came in CSV form, we attempted to move them to a PostgreSQL database, and after some difficulty were able to being querying that database for analysis. Please see the Readme in /data/ for a reference on how this was done, as well as the code under create_tables.ipynb for how to properly clean the data. 

(we also performed analysis directly from the CSVs for time-efficiency purposes: please see 01_kyle_dataprep.ipynb in the exploratory folder for reference)

#### Aggregation
After reviewing documentation, it became apparent that Real Property Sales included all real estate sales data for King County over several decades. Since we wanted our findings to be relevant for people selling their homes today, our first order of business was to filter for sales from 2019. Having completed that, it was time to join the Parcel and Residential Building data with the sales data in such a way that parcel and building information was tied to the sales data for a specific home.

Joining the data relied heavily on the Major and Minor real estate identifiers. The descriptions of these identifiers can be found here:
https://www5.kingcounty.gov/sdc/Metadata.aspx?Layer=parcel#AttributeInfo

Successfully joining the data required adding the Major and Minor columns together in such a way as to produce a "Ten character concatenation of the Major and Minor field", with leading zeroes for Major and Minor keys that were less than 6 and 4 digits long, respectively. Upon creation of the new column, which we called "HID" for House ID, we were able to join the tables so that each sale had an associated set of columns detailing both the features of the building and parcel of land. 

Having successfully collected and aggregated our data, it was time to explore the data and begin data prep.

## Data Exploration & Preparation

Our primary concern was in regard to single-family homes, so an initial filter was set for where "PropertyType" is equal to 11, 12, 13, or 14. This setting allowed us to remove all properties that were not single-family homes, multi-family homes, townhouses, or condominiums.

After filtering for property type we wanted to get a sense of how the sales price data was distributed. Having plotted the SalePrice column in a histogram, it became apparent that many of the values were set to 0 (which effectively means the house was given as a gift, and the sale was set to 0 for ownership transferal purposes). Upon removing data points where SalePrice was 0, we began to think about home prices in general in King County. After some deliberation, we decided to remove all sales below 50,000 US Dollars (this number was chosen arbitrarily and further investigation in data distribution should be done for more concrete analysis).

There were a few specific questions we wanted to answer based on commonly held beliefs about real estate value. Specifically, we wanted to investigate 1) if the presence of a porch increases sale price, 2) if the presence of waterfront increases sale price, 3) if the total square footage of the home increases sale price, and 4) if the presence of a nuisance decreases sale price. 

#### Feature Engineering

Square Footage of the home was easy to analyze because it already existed as a column in the dataset, which was labeled 'SqFtTotLiving', but the other claims were more difficult to assess and required some feature engineering on our part. 

The real estate claims regarding porches, waterfront property, and presence of nuisances are phrased binarily, and in order to answer those questions we needed binary variables (i.e. ones that were 'either or'). We generated the is_porch feature by adding the values of 'SqFtOpenPorch' and 'SqFtEnclosedPorch' then testing for whether or not the sum was above 0; thereby indicating the presence of a porch. The same process was done for 'AirportNoise', 'TrafficNoise', 'PowerLines', and 'OtherNuisance' to assess the presence of nuisances, while 'is_waterfront' was created by testing if 'WfntLocation' was any number greater than 0, which indicated that the property belonged to a waterfront of some kind within King County.

At this point, we had enough filters to begin analysis.

## Data Analysis and Model Testing

Using Statsmodels, we started by performing a linear regression using only the Square Footage feature (as we believed size of the home would be a good overall indicator of sale price). We found that Square Footage alone was able to account for roughly 35% of the variance among sale prices, as this was indicated by an R^2 value of roughly (.350).

Adding to that, we wanted to include our assessment of the other real estate claims listed above. Waterfront property had a coefficient of 1,460,000 USD which indicates that properties on the water are, on average, that much more expensive compared to houses not on the water; this is further characterized with a p-value of 0.00, which indicates a statistically significant effect.

Properties with a porch did not differ on a statistically significant level from properties without porches; the effect size was roughly 2000 USD for having a porch, but the p-value was around .8 which is not statistically sound.

The presence of a nuisance, of some kind, when run through linear regression by itself, was found to have a negative coefficient of -400 USD, and a non-statistically significant p-value of 0.8. However, when run through a model with other features, the coefficient increased to 40,000 with a p-value of 0.00. This could be interpreted as nuisance presence being a proxy for density (e.g. the closer you get to the city center, the more nuisances there will be, but the property value will still be increasing). While insignificant in-and-of itself, nuisance presence helps explain sales price when used in concert with other variables.

## Final Model

Our final model ultimately included Total Square Feet, Lake Washington View Quality, Waterfront Property, Square footage of Garage, and Square Footage of the Porch. 

The reason we included porch size is because in the cases where there WAS a porch, the coefficient was large, accounting for about 214 USD per square foot. 

The coefficient for Lake Washington View Quality was also fairly large - 360,000 - which accounts for 360,000 USD per increase in quality gradient. 

Waterfront property was also at a premium with a coefficient of 860,000, accounting for an 860,000 USD increase simply by being on the water. 

Square Footage of the living space also greatly influenced sale price with a coefficient of 360, accounting for a 360 USD increase per square foot. 

Finally, we added Garage Square Footage with a coefficient of -247, accounting for a decrease of 247 USD per square foot. We included this final item because we found it interesting that an increase in garage size account for a decrease in value. We interpreted this as indicating a premium value placed on actual living space in an area where living space is so expensive (i.e. people don't want a garage when they could have an extra room instead).

Ultimately, we were able to account for 48.2% of the variance in housing prices, all while keeping the colinearity measurements under 2 for each feature in the model (anything under 5 is considered viable). z

## Hypothesis Conclusions
Alpha: .05

Null Hypothesis 1: Higher square footage does not increase sale price.
Conclusion: We succeed in rejecting the Null Hypothesis. p_val = 0.00

Null Hypothesis 2: Having a porch does not increase sale price.
Conclusion: We fail to reject the Null Hypothesis. p_val = .8

Null Hypothesis 3: Having a waterfront property does not increase sale price.
Conclusion: We succeed in rejecting the Null Hypothesis. p_val = 0.00

Null Hypothesis 4: Having a nuisance does not decrease sale price.
Conclusion: We fail to reject the null hypothesis because the coefficient is in the positive direction. p_val = 0.00

## Assumption Tests