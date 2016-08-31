# Pr0wl

## Install Instructions

* git clone https://github.com/pickfordmatt/prowl
* apt-get install python-pip python-lxml xvfb
* pip install dnspython Beautifulsoup4 Gitpython pyvirtualdisplay

## Requirements
* Firefox

## Example Usage
### Basic Search
python prowl.py -c "Yahoo" -e "&lt;fn&gt;&lt;ln&gt;@yahoo.com"

### Deep Search
python prowl.py -c "Yahoo" -e "&lt;fn&gt;&lt;ln&gt;@yahoo.com" -p "&lt;Linkedin Profile URL&gt;" -s "au"



