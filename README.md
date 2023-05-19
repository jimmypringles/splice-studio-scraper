# splice studio scraper
A scraper for projects in Splice Studio as the service is being shut down in May.
Currently only scrapes Stereo Bounces & Stems, as the latest version of projects were already kept in sync using the Splice Studio app. 

# Installation
see requirements.txt for required packages.

# Usage
when run, it will prompt for:
- path: folder where the scrape artifacts will be created
- username: Splice username
- password: Splice password

It will then:
1. run the Studio call that will get all the projects, creating a directory for each
2. saves the project response payload as well as project artwork
3. saves each tag as an empty file with the tag as filename
4. run the timelines call for each project, creating a directory for each version
5. saves the stereo bounce of a timeline version
6. saves the stems of a timeline version

# what it doesn't do
- everything else