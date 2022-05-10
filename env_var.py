#!/usr/bin/python

import sys
import os

os.environ['APP_ID'] = sys.argv[1]
os.environ['APP_PASSWORD'] = sys.argv[2]
os.environ['LUIS_APP_ID'] = sys.argv[3]
os.environ['LUIS_API_KEY'] = sys.argv[4]
os.environ['LUIS_API_HOST_NAME'] = sys.argv[5]
os.environ['LUIS_AUTH_KEY'] = sys.argv[6]
os.environ['LUIS_AUTH_ENDPOINT'] = sys.argv[7]
os.environ['APPINSIGHTS_INSTRUMENTATION_KEY'] = sys.argv[8]