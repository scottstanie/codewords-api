"""
WOLFHOUND MULTI-SITE SETTINGS
This file us used for site setup and multi-site configuration.

"""

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define your sites here:

SITES = {
    'default': {
        'SITE_ID': 1,
        'SITE_NAME': 'Codenames',
        'SITE_DOMAIN': 'codenames.scottstaniewicz.com',
        'SECRET_KEY': 'k0uthv^x*30^q3@k8=@k5oc=k)yd3vgnv#nezob#w7z8+lg6^6',

        # Below are test keys for OAuth authentication through django-allauth.
        # They only work on http://localhost:8000/ or through a specific Ngrok proxy.
        # Uncomment below if you wish to use these test keys.
        # Please DO NOT use them in production.

        'FACEBOOK_KEY': '1774359446126514',
        'FACEBOOK_SECRET': '0f3bd26f79670a492521a4cf10c1f16e',

        # The following are database settings for your app.
        # For more info on databases in Django, see:
        # https://docs.djangoproject.com/en/1.9/ref/settings/#databases

        # For Postgres, replace the related lines under DATABASE:
        # DB_ENGINE = 'django.db.backends.postgresql_psycopg2'
        # DB_NAME = 'yourappdbname'
        # etc.

        # DATABASE is the production database, used when DB_ENV = 'prod'
        # LOCAL_DATABASE is used when DB_ENV = 'dev'
        # There is no need to touch the settings for LOCAL_DATABASE.

        'DATABASE': {
            'DB_ENGINE': 'django.db.backends.postgresql_psycopg2',
            'DB_NAME': '', # DB Name, ex. wolfhound
            'DB_USER': '', # DB User
            'DB_PASSWORD': '', # DB Password
            'DB_HOST': '', # DB Address,
            'DB_PORT': '' # DB Port, ex. 5432
        },
        'LOCAL_DATABASE': {
            'DB_ENGINE': 'django.db.backends.sqlite3',
            'DB_NAME': os.path.join(BASE_DIR, 'wolfhound_dev_database.db'),
            'DB_USER': '',
            'DB_PASSWORD': '',
            'DB_HOST': '',
            'DB_PORT': ''
        }
    }
}


def generate_cors_whitelist(site_dict):
    domain_list = ['localhost:4200', 'localhost:3000']
    for key in site_dict.keys():
        domain_list.append(site_dict[key]['SITE_DOMAIN'])
    return tuple(domain_list)
