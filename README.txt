Dogs and ducks
--------------

Mapping social media data against river pollution data to establish links between human activity and pollution

Created at Riverhack, Oxford Hackspace October 2016


Installation
------------

The mapping application runs under a Vagrant virtual machine. Check out the repository, and run:

    vagrant up
    vagrant ssh

At the VM command line:

    source ~/.virtualenvs/riverhack/bin/activate
    cd /vagrant/
    ./manage.py createsuperuser
    ./manage.py runserver 0.0.0.0:8000

log in to http://localhost:8000/admin/
from http://localhost:8000/admin/mapping/determinand/ , add the determinand:
    ID URL: http://environment.data.gov.uk/water-quality/def/determinands/0180
    Label: Orthophosphate
    Notation: 0180

On the command line:

    ./manage.py load_sampling_points
    ./manage.py load_measurements
    ./manage.py load_photos data/flickr1.csv
    ./manage.py load_photos data/flickr2.csv
    ./manage.py runserver 0.0.0.0:8000

visit:
    http://localhost:8000/all/ for all data
    http://localhost:8000/summer/ for Summer 2013 data
    http://localhost:8000/winter/ for Winter 2013/14 data
