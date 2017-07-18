# Prowl

## What is Prowl?
Prowl is an email harvesting tool that scrapes Yahoo for Linkedin profiles associated to the users search terms and identifies job titles. It also identifies current job listings for the specififed organisation. 

### Backstory
[![Steelcon 2017 - Neil Lines - Samurai of the west](https://img.youtube.com/vi/3kHP5D7VZ_I/hqdefault.jpg)](https://youtu.be/3kHP5D7VZ_I?t=6h47m5s)
(CLICK TO WATCH)

## Install Instructions

* git clone https://github.com/pickfordmatt/prowl
* pip install -r requirements.txt

## Requirements
* BeautifulSoup
* GitPython

## Example usage
### Basic search
python prowl.py -c "Yahoo" -e "&lt;fn&gt;&lt;ln&gt;@yahoo.com"

### Exclude jobs
python prowl.py -c "Yahoo" -e "&lt;fn&gt;&lt;ln&gt;@yahoo.com" -nj

### Change search depth
python prowl.py -c "Yahoo" -e "&lt;fn&gt;&lt;ln&gt;@yahoo.com" -d "10" (smaller is less, larger is more pages to search)

