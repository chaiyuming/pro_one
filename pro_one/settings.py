"""
Django settings for pro_one project.

Generated by 'django-admin startproject' using Django 2.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#5lpwlw0u9&lti6%+*#ol3tokp)(x&m-d5n=a*112v=x)o(-5)'

# SECURITY WARNING: don't run with debug turned on in production!
# 当产品上线时，True用当改为Flase；
DEBUG = True
# []中应当填服务器的地址
ALLOWED_HOSTS = ['127.0.0.1','47.99.114.195']



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'apps.news',
    'apps.pro_one_auth',
    'apps.course',
    'apps.payinfo',
    'apps.cms',
    'apps.ueditor',
    'rest_framework',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pro_one.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
# 这样配置之后，就不需要再在每个模板页面的顶部加"{% load static %}"了。在需要的地方直接写 {% static "xxx.yyy" %} 就可以了。系统已经把这个标签“全局化”了。
            'builtins':['django.templatetags.static'],
        },
    },
]

WSGI_APPLICATION = 'pro_one.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_item',
        # 填数据库的普通用户名，需要自己创建
        'USER':'pyvip',
        'PASSWORD':'cym19911206',
        # 'USER':'admin',
        # 'PASSWORD':'Root110qwe',
        'HOST': '47.99.114.195',
        'PORT': '3306',
    }
}

# 一定要添加，重写的User模型
# AUTH_USER_MODEL:这个属性是django内置的，他会主动的到这个文件中来查找这个属性，如果找到了，那么就会使用这个属性指定的模型
#来作为USER对象，AUTH_USER_MODEL是一个字符串，它的规则是"appname.Modelname",如果我们设置了AUTH_USER_MODEL，那么项目的makemigrations命令以及migrate命令必须在设置完所有的东西完才能执行。
AUTH_USER_MODEL='pro_one_auth.User'


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
# 失去一定要更改，固定写法，代表上海时区
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

#静态文件设置
STATICFILES_DIRS=(
    os.path.join(BASE_DIR,'static'),
)

# 配置media路径，在django中一般会将文件存放在media中，media可以在任何文件夹中，不一定在项目文件中。
MEDIA_URL='/media/'
MEDIA_ROOT=os.path.join(BASE_DIR,'media')

# 七牛云相关配置
QINIU_ACCESS_KEY="5ixiJHJFv_euNuH47dr2SCN4wWcGOyJA7RDVKEHt"
QINIU_SECRET_KEY="FMfUTWJwPkyGkJkQMb2fA_Dy1E2OASYETUs6TThC"
QINIU_BUCKET_NAME='cym-1991'
QINIU_DOMAIN='http://pbfsh0l77.bkt.clouddn.com/'

#1、 配置服务器的ueditor
UEDITOR_UPLOAD_TO_SERVER = True
UEDITOR_UPLOAD_PATH =MEDIA_ROOT
UEDITOR_CONFIG_PATH = os.path.join(BASE_DIR,'static','ueditor','config.json')

# 2、上传到qiniu的ueditor配置
UEDITOR_QINIU_ACCESS_KEY=QINIU_ACCESS_KEY
UEDITOR_QINIU_SECRET_KEY=QINIU_SECRET_KEY
UEDITOR_QINIU_BUCKET_NAME=QINIU_BUCKET_NAME
UEDITOR_QINIU_DOMAIN=QINIU_DOMAIN
UEDITOR_UPLOAD_TO_QINIU=True

#定义首页每页新闻有多少条新闻
ONE_PAGE__NEWS_COUNT=2

# 课程播放USER_ID（AccessKey），以及USER_KEY设置
# BAIDU_CLOUD_USER_ID='0b602bb65aa5423da147451689d2caf6'
# BAIDU_CLOUD_USER_KEY='55b29e8b974447a8'
# 控制台->用户中心->用户ID
BAIDU_CLOUD_USER_ID = '5b8849ddc6504318abcea39fe620948e'
# 点播VOD->全局设置->发布设置->安全设置->UserKey
BAIDU_CLOUD_USER_KEY = 'c228d166497b400d'