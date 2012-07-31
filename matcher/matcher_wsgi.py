SITE_DIR = '/opt/apps/site/matcher'
import site
site.addsitedir(SITE_DIR) 

import os
import sys
sys.path.append(SITE_DIR)

os.environ['DJANGO_SETTINGS_MODULE'] = 'matcher.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
