#!/usr/bin/env python
import os


class DefaultConfig:
    """Configuration for the bot."""

    PORT = 8000
    APP_ID = os.environ['APP_ID']
    APP_PASSWORD = os.environ['APP_PASSWORD']
    LUIS_APP_ID = os.environ['LUIS_APP_ID']
    LUIS_API_KEY = os.environ['LUIS_API_KEY']
    # LUIS endpoint host name, ie "westus.api.cognitive.microsoft.com"
    LUIS_API_HOST_NAME = os.environ['LUIS_API_HOST_NAME']
    LUIS_AUTH_KEY = os.environ['LUIS_AUTH_KEY']  # Authoring Key
    LUIS_AUTH_ENDPOINT = os.environ['LUIS_AUTH_ENDPOINT']  # Authoring Endpoint
    APPINSIGHTS_INSTRUMENTATION_KEY = os.environ['APPINSIGHTS_INSTRUMENTATION_KEY']

