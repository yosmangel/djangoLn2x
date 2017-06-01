# This file is exec'd from settings.py, so it has access to and can
# modify all the variables in settings.py.

# If this file is changed in development, the development server will
# have to be manually restarted because changes will not be noticed
# immediately.

DEBUG = False

# Make these unique, and don't share it with anybody.
SECRET_KEY = "+79yadv9jv$t0d788_x7goe7#*kl_ba)9l+m^p3+cu7c9kbuh@"
NEVERCACHE_KEY = "etel4ji_nynh53e_3=a^g6!&eo3o$z&6em%4*xmaj)ou=0)pfg"

DATABASES = {
    "default": {
        # Ends with "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        # DB name or path to database file if using sqlite3.
        "NAME": "djangoln2x",
        # Not used with sqlite3.
        "USER": "lallen",
        # Not used with sqlite3.
        "PASSWORD": "uI2Ey5pmkKo8",
        # Set to empty string for localhost. Not used with sqlite3.
        "HOST": "djangoln2x121216.cu8hgrvxgs06.eu-central-1.rds.amazonaws.com",
        # Set to empty string for default. Not used with sqlite3.
        "PORT": "5432",
    },
}

###################
# DEPLOY SETTINGS #
###################

# Domains for public site
ALLOWED_HOSTS = ["ln2x.com", "www.ln2x.com", "52.28.190.217",]

# These settings are used by the default fabfile.py provided.
# Check fabfile.py for defaults.

# FABRIC = {
#     "DEPLOY_TOOL": "rsync",  # Deploy with "git", "hg", or "rsync"
#     "SSH_USER": "",  # VPS SSH username
#     "HOSTS": [""],  # The IP address of your VPS
#     "DOMAINS": ALLOWED_HOSTS,  # Edit domains in ALLOWED_HOSTS
#     "REQUIREMENTS_PATH": "requirements.txt",  # Project's pip requirements
#     "LOCALE": "en_US.UTF-8",  # Should end with ".UTF-8"
#     "DB_PASS": "",  # Live database password
#     "ADMIN_PASS": "",  # Live admin user password
#     "SECRET_KEY": SECRET_KEY,
#     "NEVERCACHE_KEY": NEVERCACHE_KEY,
# }

STATICFILES_DIRS = (
        '/home/ubuntu/production/ln2xsite/static/',
    )

SITE_TITLE = "LiquidNexxus - LN2X"
SITE_TAGLINE = "The Global Leader in Payment Systems, Compliance, Risk and Security Training."

LOCALE_PATHS = [
            os.path.join(BASE_DIR, 'locale'),
    ]

CORS_ORIGIN_ALLOW_ALL = True

X_FRAME_OPTIONS = 'ALLOW'

ADMINS = [('Stephane', 'stephanep@liquidnexxus.com'),
          ('Alexandre', 'abrouail@liquidnexxus.com'),]

CSRF_COOKIE_HTTPONLY = True

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "https://ln2xdjangostaticfiles.s3-eu-west-1.amazonaws.com/static/"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, STATIC_URL.strip("/"))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = STATIC_URL + "media/"

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, *MEDIA_URL.strip("/").split("/"))

DEFAULT_FILE_STORAGE = 's3utils.MediaS3BotoStorage'
STATICFILES_STORAGE = 's3utils.StaticS3BotoStorage'

AWS_ACCESS_KEY_ID = "AKIAJZ34KXUB2KWT5I5Q"
AWS_SECRET_ACCESS_KEY = "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"
AWS_STORAGE_BUCKET_NAME = "ln2xdjangostaticfiles"
AWS_S3_HOST = 's3-eu-west-1.amazonaws.com'

