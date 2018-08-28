# Item Catalog - Udacity

### Full Stack Web Development ND

_______________________

## About

This project consists in a webserver which connects with a database of  
predefined sports categories, including user created items for each one.

Only registered users can add items whereas only the item creator can edit  
and delete it.

For this purpose a third-party signin has been implemented, in this case  
Google Oauth2.

The web server is written in Python with Flask micro-framework. Using  
SQLAlchemy for the database creation and interaction.

It displays request responses in Html which includes CSS, Javascript, jQuery and AJAX.


## Prerequisites

* [Python 3](https://www.python.org/downloads/)  
Download for Windows, run `brew install python3` on Mac  
or `sudo apt-get install python3` on Linux

* [VirtualBox 3](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)  
Necessary download and install to use vagrant on it

* [Vagrant](https://www.vagrantup.com/downloads.html)  
Install, then in terminal change directory to the vagrant folder,  
run `vagrant up` to initialize, run `vagrant ssh` after to log in


## Installation

After installing all the necessary specified below and run vagrant ssh.

Change directory again to vagrant. Then change directory to catalog.

Run `python database-setup.py` to initialize database with categories.

Run  `python item-catalog.py` to enable the web server.

You can access in your web browser with "localhost:8000".


## Additional Comments

To erase database delete created files: itemcatalog.db and database_setup.pyc.

Authenticate with google to interact with items, action buttons will only  

appear if you are allowed to do that actions.

In case you access manually (not from main page) to a server page to try to  

do some action you are not allowed, it won't do the action on database.
