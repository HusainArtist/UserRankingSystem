DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.mysql',
       'NAME': 'userrankdatabase',
       'USER': 'root',
       'PASSWORD': 'testing',
       'HOST': 'localhost',
       'PORT': '3306',
       'connection': 'local',
       'become': False
   }
   # 'default': {
   #     'ENGINE': 'django.db.backends.mysql',
   #     'NAME': 'traansport2',
   #     'USER': 'root',
   #     'PASSWORD': 'testing',
   #     'HOST': 'localhost',
   #     'PORT': '3306',
   # }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_swagger',
    'rest_framework.authtoken',
    'Games',
    'storages',
]
ROOT_URLCONF = 'UserRankingSystem.urls'
WSGI_APPLICATION = 'UserRankingSystem.wsgi.application'