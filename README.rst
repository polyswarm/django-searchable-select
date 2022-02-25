django-searchable-select
========================

.. figure:: https://coveralls.io/repos/github/and3rson/django-searchable-select/badge.svg

A better and faster multiple selection widget with suggestions for Django.

What is this?
=============

This plugin provides a replacement for standard multi-choice select on
Django admin pages.

You can use this as custom widget for ``ManyToManyField``.

Features
========

-  Filtering is performed on server side and thus significantly improves
   performance.
-  Uses ``Twitter Typeahead`` to provide suggestion completion.
-  Works **great** with ManyToMany fields that can be chosen from
   thousands of thousands of choices, e. g. ``User - City`` relations.

Before
~~~~~~

.. figure:: https://habrastorage.org/files/dd9/f17/87e/dd9f1787e0dd4e05826fdde08e270609.png
   :alt: Before

   Before

After
~~~~~

.. figure:: https://habrastorage.org/files/db2/c87/460/db2c87460992470e9d8e19da307c169d.png
   :alt: Before

   Before

Installation
============

1. Install ``django-searchable-select``.

   .. code:: sh

       $ pip install django-searchable-select

2. Add ``'searchableselect'`` to your settings.

   .. code:: python

       # settings.py

       INSTALLED_APPS = (
           # ...
           'searchableselect',
           # ...
       )

3. Add URL pattern required for the suggesting engine to your root
   ``urls.py``.

   .. code:: python

       # urls.py

       urlpatterns = patterns(
           '',
           # ...
           re_path('^searchableselect/', include('searchableselect.urls')),
           # ...
       )

4. Use the widget in your model admin class:

   .. code:: python

       from django import models, forms
       from searchableselect.widgets import SearchableSelect
       from models import Traveler

       class TravelerForm(forms.ModelForm):
           class Meta:
               model = Traveler
               exclude = ()
               widgets = {
                   'cities_visited': SearchableSelect(model='cities.City', search_field='name', many=True, limit=10)
               }


       class TravelerAdmin(admin.ModelAdmin):
           form = TravelerForm

       admin.site.register(Traveler, TravelerAdmin)

   Remember to **always** initialize ``SearchableSelect`` with three
   keyword arguments: ``model``, ``search_field`` and ``many``.

   -  ``model`` is the string in form ``APP_NAME.MODEL_NAME``
      representing your model in the project, e. g. ‘cities.City’
   -  ``search_field`` is the field within model that will be used to
      perform filtering, e. g. ‘name’
   -  ``many`` must be ``True`` for ``ManyToManyField`` and ``False``
      for ``ForeignKey``.
   -  ``limit`` (optional) specifies the maximum count of entries to retrieve.
   -  ``load_on_empty`` (optional, default ``False``) whether to show the
      first options available (up to limit) when the input gets the focus
      and it's empty.
   -  ``display_deleted`` (optional, default ``True``) display elements in
      the "chips" section even if they were deleted from the "foreign" model.

Example app
===========

Just run the project from `example` directory, head to http://127.0.0.1:8000, login as ``admin``/``admin`` and try adding Cats!

The ``lookup_field`` argument and ``ArrayField``
================================================

*(New)*

There is one more argument that can be passed to the ``SearchableSelect`` constructor,
the ``lookup_field``, that by default is ``pk`` (the primary key whatever the
name is). The field chosen from the model is the one that will be returned as result.
This is specially useful with the
`ArrayField <https://docs.djangoproject.com/en/4.0/ref/contrib/postgres/fields/#django.contrib.postgres.fields.ArrayField>`_,
where we may want to store string values from another table, but not the ids.

Example
~~~~~~~

You have a ``Blog`` model that has multiple "tags", and you have
a table with all the valid tags, but you don't want a **many-to-many**
relation because it is inefficient, so instead you use a
`Array field from Postgres <https://www.postgresql.org/docs/current/arrays.html>`_,
where you store only the "label" of the tags, not the ids.

So the mapping is as follow:

.. code:: python

   class Blog(models.Model):
       tags = ArrayField(models.CharField(max_length=255), blank=True, default=list)

And the mapping of the table where you have all the possible tags:

.. code:: python

   class Tag(models.Model):
       label = models.CharField(unique=True, max_length=255)
       def __str__(self):
           return self.label

So now the configuration in the Admin to query the tags and store the values
from the ``label`` field instead of the primary key value would be as follow:

.. code:: python

   class BlogForm(forms.ModelForm):
       class Meta:
           model = Blog
           exclude = ()
           widgets = {
               'tags': SearchableSelect(
                   model='blogs.Tag', search_field='label', lookup_field='label', many=True, limit=10),
           }

   @admin.register(Blog)
   class BlogAdmin(admin.ModelAdmin):
       form = BlogForm


Supported versions
==================

- Python 3.5+ and Django 2.2, 3.0, 3.2 or 4.0.

Known issues
============

-  Not tested with empty fields.

Contributing
============

I’m looking forward to bug reports and any kind of contribution.

License
=======

You are free to use this where you want as long as you keep the author
reference. Please see LICENSE for more info.
