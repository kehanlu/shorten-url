# Shorten url

![](https://img.shields.io/badge/Django-2.0-blue.svg) (以2.0開發，但應該可以相容到很久之前的版本)

1. 簡單生成如 goo.gl/xxxx 的短網址 `https://yourdomain.com/u/asdf`

2. 或是自訂網址 `https://yourdomain.com/links/hank_has_no_life` 的meta tag 使得在 FB、Line 等達到自訂縮圖、標題的效果。

3. 可以查看流量統計圖

- [Usage](#usage)
- [Installation](#installation)
- [Demo](#demo)
    - [快速生成](#fast-gernerate)
    - [自訂網址](#custom-gernerate)
    - [錯誤訊息](#錯誤訊息)
    - [全部的網址列表](#全部的網址列表)
    - [瀏覽統計圖](#瀏覽統計圖)

## Usage



## Installation

### 基本設定

```
$ python manage.py migrate
```

#### yoursite/settings.py

```python
INSTALLED_APP = [
  # ...
  'links',
]

# 並設定 STATIC_URL、MEDIA_URL 等等
```

#### yoursite/urls.py

```python
from django.urls import path, include
import links
urlpatterns = [
    # ...
    
    # links
    path('links/', include('links.urls')),
    path('u/<str:permanent_url>/', links.views.perm_url)
]
```


#### links/views.py

```python
# 短網址的 base *切記以 http...開頭*
BASE_URL = 'https://yourdomain.com/links/'
BASE_SHORT_URL = 'https://yourdomain.com/u/'

# 生成永久網址的 hash_salt
HASH_SALT = 'meow'

# 自訂轉址的預設值
DEFAULT_NAME = ''
DEFAULT_TITLE = ''
DEFAULT_DESCRIPTION = ''

```

#### static/images/default_thumbnail.png
自訂轉址的預設圖


## Demo

### Fast Gernerate
輸入網址，然後按下按鈕，大概等個 0.5 秒就跑出來了～
![](https://i.imgur.com/ea9lgOt.png)

### Custom Gernerate

可以額外設定網址名稱、標題、描述、縮圖

![](https://i.imgur.com/XZnNHKo.png)

![](https://i.imgur.com/YufDDpR.png)

### 錯誤訊息

![](https://i.imgur.com/D4o9D1S.png)


### 全部的網址列表

![](https://i.imgur.com/c4Mcli3.png)

### 瀏覽統計圖

![](https://i.imgur.com/zM90mPW.png)
