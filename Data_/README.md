# IMDB Data Scrapping

## Technologies
Python 3.7

## Setup

For having the codes fully functional and running for you please make sure to have installed these packages beforehand:
```
pip install beautifulsoup4
pip install selenium
pip install lxml
```

## Operating instructions
For starting the project the source.py file should be run first. The output of this process will bring unique movie ids and its title that will be added to the main database.

#### Note: For demonstration purposes, only the first page (250 movies) will be scrapped. The rest of the code is commented.

Moving forward, the data for separate movies will be obtained running data.py file.

#### Note: Here also only 4 movies are scrapped. You can always customize the scrapping scope from codes.

## A file manifest (list of files included)

* chromdriver.exe
When scrapping Oscars data we will be using Selenium for which we need to have this file in the directory.
* data.db
We will be gathering the whole scrapped data to this database.
* oscars.db
To make sure the scrapping codes for Oscars is working primary keys should be available. Thus, this database includes already scrapped data with the whole scope of Movies and People.

#### Note: This file will be used for code demonstration part only. 

* init_sql.py
The main database structure and data management functionality can be modified here.
* source.py
Given the destination of the movie page from IMDB, the source will be scrapped.
* data.py
After successfully running the source.py file and getting the whole list of movies that need to be scrapped it's time to get the rest of the data. This process is fully handled in data.py file.
* oscars.py
Noting that Oscars page includes JS elements that require the utilization of Selenium rather than BeautifulSoup, this section of data scrapping is separated from the main scrapping block.
* modify.py
Before entering to the database some of the values need to be modified reflection of which is done by separate functions included in here.
* ratings.py
Actor ratings calculation method.