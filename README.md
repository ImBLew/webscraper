# Webscrapers

Collection of webscrapers I've made

## WebscraperPOC

#### DEPRICATED

Designed for use with a proprietary system - variables would be read from input to create parse string to do webscraping

Project scrapped due to impracticality

## WebscraperATC

Webscraper for scraping ATC codes off WHOCC.no

TODO: Implement crawl delay

The design of this web scraper is a recursive function following the ATC code levels down to the individual drug names.

The data collected is stored in 'collected_parse', to be turned into a dataframe with the respective column names.
The webscraper cycles through each of the 14 ATC codes one by one, sending them to the recursive scraper as its 'base url'.
In the recursive scrape, the html from the page is parsed with BeautifulSoup.


#### SITE SPECIFIC INFORMATION:

The information we're looking for (ATC levels and drug tables) are all located within \<div id='content'\> tags. This allows the scraper to easily narrow its scope to just search for the tags we want.

If we're at the ATC code where the drug names are, there will be an unordered list ('ul'), which allows us to call off the rest of the search, build the ATC level path (based on \<b\> tags that do not have a \<p\> tag parent), and add the information collected to the dataframe.

At any other point, we're able to locate the next links based on the \<b\> tags that DO have \<p\> tags as parents by parsing out their hrefs.
  
  
