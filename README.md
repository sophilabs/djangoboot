# djangoboot

[![No Maintenance Intended](http://unmaintained.tech/badge.svg)](http://unmaintained.tech/)

Is a web application intended to explore templates for `django-admin.py` projects/apps and `cookiecutter`.

Try it: http://djangoboot.com


## Authors

* [Sebastian Nogara](http://github.com/snogaraleal)
* [Pablo Ricco](http://github.com/pricco)

## Credits and Thanks

* This project was created for the [DjangoDash](http://djangodash.com/) competition.
* Thanks to [Sophilabs](http://sophilabs.com) team for the place and food!
* Thanks to [2Scoops](https://django.2scoops.org/) for inspiring us with the idea.
  [Buy the book!](http://www.amazon.com/Two-Scoops-Django-Best-Practices/dp/1481879707/ref=sr_1_2?ie=UTF8&qid=1366166104&sr=8-2&tag=cn-001-20)


## Installation

    git clone git@github.com:sophilabs/djangoboot.git
    cd djangoboot
    virtualenv ~/envs/djangoboot --distribute
    source ~/envs/djangoboot/bin/activate
    pip install -r requirements/development.txt
    cd app
    #Create your postgres database first
    python manage.py syncdb --migrate
    python manage.py runserver
  
### Solr

    wget http://mirrors.sonic.net/apache/lucene/solr/4.4.0/solr-4.4.0.tgz
    tar --extract --file=solr-4.4.0.tgz
    cd solr-4.4.0/example
    cp -R <djangoboot-path>/solr solr-4.4.0/example/solr/boots
    java -jar start.jar


