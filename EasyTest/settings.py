"""
Django settings for EasyTest project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
from celery.schedules import crontab
from celery.schedules import timedelta

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0y=3effs=f2e3wqz^sbqt(@d@&+*6*r^86(!p1f8n$ygumkk!i'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = False
DEBUG = True

ALLOWED_HOSTS = ['*', '39.105.136.231', '127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'base',
    'guest',
    'mocks',
    'djcelery',
    'bootstrap3',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'EasyTest.urls'

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
        },
    },
]

WSGI_APPLICATION = 'EasyTest.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
"""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': "127.0.0.1",
        'NAME': "easytest",
        'USER': "easytest",
        'PASSWORD': "123456",
        'PORT': "3306",
    }
}

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

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

# 页面展示时间比数据库时间快8h
USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

# session 设置
SESSION_COOKIE_AGE = 60 * 300  # 30分钟
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # 关闭浏览器，则COOKIE失效

# 上传
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # 对应文件夹
if not os.path.exists(MEDIA_ROOT): os.mkdir(MEDIA_ROOT)
MEDIA_URL = '/media/'  # 对应上线后的url

STATIC_URL = '/static/'
STATIC_ROOT = '/var/static/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

# 配置缓存
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PICKLE_VERSION": -1,  # 使用其他版本的pickle
            "CONNECTION_POOL_KWARGS": {"max_connections": 100},  # 连接池的最大连接数
            "SERIALIZER": "django_redis.serializers.json.JSONSerializer",  # json 序列化数据
        }
    }
}
# 将 django-redis 作为 session 储存后端
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# 自定义配置
REDIS = {
    'host': 'localhost',
    'port': '6379',
    # 'password': 123456,
    'db': '2',
}

# log
# 导入模块
import time

cur_path = os.path.dirname(os.path.realpath(__file__))  # log_path是存放日志的路径
log_path = os.path.join(os.path.dirname(cur_path), 'logs')
if not os.path.exists(log_path): os.mkdir(log_path)  # 如果不存在这个logs文件夹，就自动创建一个

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        # 日志格式
        'standard': {
            'format': '[%(asctime)s] [%(filename)s:%(lineno)d] [%(module)s:%(funcName)s] '
                      '[%(levelname)s]- %(message)s'},
        'simple': {  # 简单格式
            'format': '%(levelname)s %(message)s'
        },
    },
    # 过滤
    'filters': {
    },
    # 定义具体处理日志的方式
    'handlers': {
        # 默认记录所有日志
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(log_path, 'all-{}.log'.format(time.strftime('%Y-%m-%d'))),
            'maxBytes': 1024 * 1024 * 5,  # 文件大小
            'backupCount': 5,  # 备份数
            'formatter': 'standard',  # 输出格式
            'encoding': 'utf-8',  # 设置默认编码
        },
        # 输出错误日志
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(log_path, 'error-{}.log'.format(time.strftime('%Y-%m-%d'))),
            'maxBytes': 1024 * 1024 * 5,  # 文件大小
            'backupCount': 5,  # 备份数
            'formatter': 'standard',  # 输出格式
            'encoding': 'utf-8',  # 设置默认编码
        },
        # 控制台输出
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        # 输出info日志
        'info': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(log_path, 'info-{}.log'.format(time.strftime('%Y-%m-%d'))),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'standard',
            'encoding': 'utf-8',  # 设置默认编码
        },
    },
    # 配置用哪几种 handlers 来处理日志
    'loggers': {
        # 类型 为 django 处理所有类型的日志， 默认调用
        'django': {
            'handlers': ['default', 'console'],
            'level': 'INFO',
            'propagate': False
        },
        # log 调用时需要当作参数传入
        'log': {
            'handlers': ['error', 'info', 'console', 'default'],
            'level': 'INFO',
            'propagate': True
        },
    }
}

import djcelery

djcelery.setup_loader()
BROKER_URL = 'redis://127.0.0.1:6379/0'
# broker_pool_limit=None
# BROKER_POOL_LIMIT=None
CELERY_IMPORTS = ('base.tasks')
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
# CELERY_ENABLE_UTC = False
# DJANGO_CELERY_BEAT_TZ_AWARE = False
CELERYBEAT_SCHEDULE = {  # 定时器策略
    # 定时任务一：　每隔30s运行一次
    # u'测试定时器1': {
    #     "task": "base.tasks.hello_world",
    #     # "schedule": crontab(minute='*/2'),  # or 'schedule':   timedelta(seconds=3),
    #     "schedule": timedelta(seconds=30),
    #     "args": (),
    # },
}

LOGIN_URL = '/login_action/'

SWAGGER_SETTINGS = {
    # 基础样式
    'SECURITY_DEFINITIONS': {
        "basic": {
            'type': 'basic'
        }
    },
    # 如果需要登录才能够查看接口文档, 登录的链接使用restframework自带的.
    'LOGIN_URL': 'rest_framework:login',
    'LOGOUT_URL': 'rest_framework:logout',
    # 'DOC_EXPANSION': None,
    # 'SHOW_REQUEST_HEADERS':True,
    # 'USE_SESSION_AUTH': True,
    # 'DOC_EXPANSION': 'list',
    # 接口文档中方法列表以首字母升序排列
    'APIS_SORTER': 'alpha',
    # 如果支持json提交, 则接口文档中包含json输入框
    'JSON_EDITOR': True,
    # 方法列表字母排序
    'OPERATIONS_SORTER': 'alpha',
    'VALIDATOR_URL': None,
}

REST_FRAMEWORK = {
    # 下面这一行表示接口文档的访问权限, AllowAny不做权限限制.
    # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.AllowAny',),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    # 'PAGE_SIZE': 10,
    'PAGINATE_BY': 10,
}

# simpleui 设置

# 首页配置
# SIMPLEUI_HOME_PAGE = 'https://www.baidu.com'
# 首页标题
# SIMPLEUI_HOME_TITLE = '百度一下你就知道'
# 首页图标,支持element-ui的图标和fontawesome的图标
# SIMPLEUI_HOME_ICON = 'el-icon-date'

# 设置simpleui 点击首页图标跳转的地址
# SIMPLEUI_INDEX = 'https://www.88cto.com'

# 首页显示服务器、python、django、simpleui相关信息
# SIMPLEUI_HOME_INFO = True

# 首页显示快速操作
# SIMPLEUI_HOME_QUICK = True

# 首页显示最近动作
# SIMPLEUI_HOME_ACTION = True

# 自定义SIMPLEUI的Logo
# SIMPLEUI_LOGO = 'https://avatars2.githubusercontent.com/u/13655483?s=60&v=4'

# 登录页粒子动画，默认开启，False关闭
# SIMPLEUI_LOGIN_PARTICLES = False

# 让simpleui 不要收集相关信息
# SIMPLEUI_ANALYSIS = True

# 自定义simpleui 菜单
SIMPLEUI_CONFIG = {
    # 在自定义菜单的基础上保留系统模块
    'system_keep': False,
    'menus': [
        {
            'app': ' auth',
            'name': '账户管理',
            # 'icon': 'fas fa-user-shield',
            'models': [{
                'name': '用户',
                'icon': 'fa fa-user',
                'url': 'auth/user/'
            }, {
                'name': '组',
                'icon': 'fas fa-users-cog',
                'url': 'auth/group/'
            }
            ]
        },
        {
            'app': ' base',
            'name': '测试平台',
            # 'icon': 'fas fa-user-shield',
            'models': [
                {
                    'name': '项目管理',
                    # 'icon': 'fa fa-product-hunt fa-fw',
                    'url': 'base/project/'
                },
                {
                    'name': '测试环境',
                    # 'icon': 'fa fa-product-hunt fa-fw',
                    'url': 'base/environment/'
                },
                {
                    'name': '接口管理',
                    # 'icon': 'fa fa-product-hunt fa-fw',
                    'url': 'base/interface/'
                },
                {
                    'name': '测试用例',
                    # 'icon': 'fa fa-product-hunt fa-fw',
                    'url': 'base/case/'
                },
                {
                    'name': '测试计划',
                    # 'icon': 'fa fa-product-hunt fa-fw',
                    'url': 'base/plan/'
                },
                {
                    'name': '签名管理',
                    # 'icon': 'fa fa-product-hunt fa-fw',
                    'url': 'base/sign/'
                },
                {
                    'name': '测试报告',
                    # 'icon': 'fa fa-product-hunt fa-fw',
                    'url': 'base/report/'
                }, {
                    'name': '发布会',
                    # 'icon': 'fa fa-product-hunt fa-fw',
                    'url': 'base/event/'
                }, {
                    'name': '发布会嘉宾',
                    # 'icon': 'fa fa-product-hunt fa-fw',
                    'url': 'base/guest/'
                },
            ]
        },
        {
            'app': 'djcelery',
            'name': '定时任务',
            'icon': 'fas fa-user-shield',
            'models': [{
                'name': 'Crontabs',
                # 'icon': 'fa fa-user',
                'url': 'djcelery/crontabschedule/'
            }, {
                'name': 'Intervals',
                # 'icon': 'fa fa-user',
                'url': 'djcelery/intervalschedule/'
            }, {
                'name': 'Periodic tasks',
                # 'icon': 'fa fa-user',
                'url': 'djcelery/periodictask/'
            }, {
                'name': ' Tasks',
                # 'icon': 'fa fa-user',
                'url': 'djcelery/taskstate/'
            }, {
                'name': 'Workers',
                # 'icon': 'fa fa-user',
                'url': 'djcelery/workerstate/'
            },
            ]
        },
    ]
}
# 是否显示默认图标，默认=True
# SIMPLEUI_DEFAULT_ICON = False

# 图标设置，图标参考：
SIMPLEUI_ICON = {
    # '测试平台': 'fab fa-apple',
    # '账户管理': 'fas fa-user-tie'
}

# 指定simpleui 是否以脱机模式加载静态资源，为True的时候将默认从本地读取所有资源，即使没有联网一样可以。适合内网项目
# 不填该项或者为False的时候，默认从第三方的cdn获取

SIMPLEUI_STATIC_OFFLINE = True
