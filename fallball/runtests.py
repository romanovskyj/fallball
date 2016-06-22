#!/usr/bin/env python
import os
import sys
from imp import reload

import django
from django.conf import settings
from django.test.utils import get_runner

import fallball

# As parent directory has also 'fallball' name it needs to specify the package explicitly:
if __name__ is not '__main__':
    current_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.join(current_path, 'fallball'))
    reload(fallball)

os.environ['DJANGO_SETTINGS_MODULE'] = 'fallball.settings'
django.setup()

TestRunner = get_runner(settings)
test_runner = TestRunner()
failures = test_runner.run_tests(['fallballapp.tests'])
sys.exit(bool(failures))
