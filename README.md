# Django Front Data

### A reusable dependency free django front data apps

Sometimes we need to fetch unstructured data from back-end to front-end such as navbar. But this is boring task as you
have to design database for every type of data. We can avoid this by using a good JSON editor. This package contains a
good JSON editor for admin panel. Also this package has built-in serializers and django rest api support.

## Installation

<ol>
<li>
Install the package

`pip install django-front-data`
</li>
<li>
Add into yours settings INSTALLED_APPS

`front_data',`
</li>
<li>If you have django rest framework installed you can add package urls to your
URL config

`path('front-data/', include('front_data.urls'))`

###### You can only use front_data.urls if you have djangorestframework installed

</li>
</ol>

## Settings

### DEFAULT_SITE_DATA

You can use this setting to automatically add template. examples:

<pre>DEFAULT_SITE_DATA = [
    {
        "name": "nav-bar",
        "data": [],
        "templates": [
            {
                "text": "Navbar",
                "value": {
                    "text": "",
                    "link": ""
                }
            }
        ]
    }
]
</pre>
Above example will create front data instance named `navbar` when you start
your server. It will skip if there is already `navbar` instance in
database. This will also create a template named `navBar`. See 
template section about what you can do with template.