django-oembed
=======================

This is a collection of tools for Django to allow for replacing links in text
with OEmbed.  This application also provides utilities to make this process not
prohibitively expensive CPU-wise.

Thanks for downloading a *Lift Interactive* fork of django-oembed!

Prerequisites
=============

- Python 2.3 or later
- Django 0.96 or later
- pip (any recent version should be fine)

Installation
============

Use pip to install:

    pip install git+git://github.com/l1f7/django-oembed.git@0.1.5

or

    pip install git+https://github.com/l1f7/django-oembed.git@0.1.5

Where 0.1.5 is the version tag (currently, there are 0.1.1, 0.1.2, and 0.1.5).
We forked django-oembed at 0.1.2, so if you don't want our changes
(see Changelog), use 0.1.2 instead.

Place 'oembed' in the INSTALLED_APPS tuple of your settings.py file like so:
    
    INSTALLED_APPS = (
        # ...
        'oembed',
    )

Then run ```manage.py syncdb```.

Usage
=====

Here is sample usage in a template:

    {% load oembed_tags %}
    ...
    {% oembed %}
        {% for link in links %}{{ link.href }}{% endfor %}
    {% endoembed %}

Any link.href inside the oembed tags will be replaced with an oEmbed object,
if possible.

The template tag takes two optional arguments:
    
    {% oembed 320x240 simple %}

- ```WIDTHxHEIGHT``` specifies the maximum width and height (whichever comes first for
your embed object)
- ```simple``` specifies that you would prefer to get back the most basic,
  unstyled embed object possible.  See Django Admin - Provider Rules for more
  information.

Django Admin Features
=====================

Provider Rules
--------------

These are the oEmbed providers which are supported by django-oembed.  Within
the Django Admin, you can create, update, and delete providers at your
convenience.

The ```regex``` field defines the match URL which will trigger the use of the
oEmbed URL defined in the ```endpoint``` field.  If your oEmbed provider
supports URL query parameters, you can append them to the endpoint in the form:

    http://endpoint.url/oembed?query1=value&query2=value

The ```format``` field defines the oEmbed response format.

The ```simple``` field (added in version 0.1.5) is a checkbox which tells
django-oembed that this Provider Rule will return a simpler, less stylized
embed object.

For example, you can have a rule named *Twitter Status*, whose
endpoint is:
```
https://api.twitter.com/1/statuses/oembed.json
```
and have another Twitter endpoint named *Twitter Status (Simple)* whose
endpoint is:
```
https://api.twitter.com/1/statuses/oembed.json?hide_media=true&hide_thread=true&omit_script=true
```
If in your oembed template tag you include ```simple``` as an
argument, django-oembed will use the Provider Rule whose ```simple``` parameter
is checked.

In the event that you forget to include a simple Provider Rule, django-oembed
will fall back to using the regular Provider Rule.

Stored oEmbeds
--------------

Instead of re-creating the embed object from scratch every time, if a URL
matches with the URL of a Stored oEmbed object, django-oembed will use the HTML
code in the Stored oEmbed's ```html``` field.  A Stored oEmbed can be created
for a regular and a ```simple``` embed.

Changelog
=========

0.1.5 (Where this fork begins)
------------------------------
- New optional ```simple``` argument for the ```{% oembed %}``` template tag
    - Falls back to a non-simple Provider Rule if no simple Provider Rule
      exists
- Improved Django Admin integration
    - Provider Rule list display shows provider name, ```simple``` parameter,
      and the endpoint URL.  The ```simple``` parameter can be changed right in
      the list view.
    - Stored oEmbed list display shows match, max width, max height, and the
      'simple' parameter.  The ```simple``` parameter can be changed right in
      the list view.
