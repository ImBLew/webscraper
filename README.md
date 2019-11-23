# Webscrapers

Collection of webscrapers I've made

## WebscraperPOC

#### DEPRICATED

Designed for use with a proprietary system - variables would be read from input to create parse string to do webscraping.

Project scrapped due to impracticality.

## WebscraperATC

Webscraper for scraping ATC codes off WHOCC.no

TODO: Implement crawl delay

The design of this web scraper is a recursive function following the ATC code levels down to the individual drug names.

The data collected is stored in 'collected_parse', to be turned into a dataframe with the respective column names.
The webscraper cycles through each of the 14 ATC codes one by one, sending them to the recursive scraper as its 'base url'.
In the recursive scrape, the html from the page is parsed with BeautifulSoup.


#### SITE SPECIFIC INFORMATION:

The information we're looking for (ATC levels and drug tables) are all located within \<div id='content'\> tags. This allows the scraper to easily narrow its scope to just search for the tags we want.

We first start out by checking we're not at an end point where we'd find an ATC code. If we're at the ATC code information, there will be an unordered list ('ul'), which allows us to call off the rest of the search, build the ATC level path, and add the information collected to the 'collected_parse' for the dataframe. The ATC level path is easy to build, because the links that were followed to reach the end point will be \<b\> tags that do not have a \<p\> tag parent.

Since we've already checked if we're at the end and not found anything, that means we're on a page that has further ATC level links. We can generate the list of links to follow based on \<b\> tags that have \<p\> taks as their parents. The href links returned by doing this only has the subdirectory information, so we need to generate the domain information to make the requests.
  
  
