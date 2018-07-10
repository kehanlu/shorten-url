# Shorten URL

![](https://img.shields.io/badge/Django-2.0-blue.svg)

for more detail about shorten URL system you can check my blog: 
[短網址系統開發心得](https://deephank.tw/blog/shorten-url-system/)

- [Feature](#feature)
- [Quick start](#quick-start)
- [Merge to exist django project](#merge-to-exist-django-project)
- [Some screenshot](#screenshot)
- [reference](#ref)
- [Contribution](#contribution)

## Feature

### Fast generate
like goo.gl, paste a URL and click -> get shortened URL!

### Costom gernerate
enable custom title,description and thumbnail for facebook (and other social media) link preview.

![](https://i.imgur.com/4fs2IOR.png)

### Analysis
enable to track views.

![](https://i.imgur.com/zM90mPW.png)

## Quick start
> example site
```
$ git clone https://github.com/kehanlu/shorten_url
$ cd django

# should have django 2.0 enviroment 

$ python manage.py migrate
$ python manage.py runserver

# localhost:8000/links
# enjoy! 
```

## Merge to exist django project

> is quite easy!
> 

### move folder
put app & template folder to the right place

### run
```
$ python manage.py migrate
```

### modify some codes

**yoursite/settings.py**
```python
INSTALLED_APP = [
  # ...
  'links',
]

# finely set STATIC_URL and MEDIA_URL
# see django doc:
# https://docs.djangoproject.com/en/2.0/howto/static-files/
```


**links/views.py**
```python
# BASE should start with 'http://' or 'https://'
BASE_URL = 'https://yourdomain.com/links/'
BASE_SHORT_URL = 'https://yourdomain.com/u/'

# hash_salt for generate permanent url
HASH_SALT = 'meow'

# default value for custom url
DEFAULT_NAME = ''
DEFAULT_TITLE = ''
DEFAULT_DESCRIPTION = ''
```

**static/images/default_thumbnail.png**

put a image for default thumbnail!

## Screenshot
![](https://i.imgur.com/ea9lgOt.png)

![](https://i.imgur.com/XZnNHKo.png)

![](https://i.imgur.com/zM90mPW.png)

## ref

[bulma](http://bulma.io/) (CSS framework)

## Contribution

i have no idea now, maybe open an issue! tks