#!/usr/bin/env python
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Configuration for the bot."""

import os


class DefaultConfig:
    """Configuration for the bot."""

    PORT = 8000
    APP_ID = "cf9f2854-e02d-4158-9689-3cc7f023388c"
    APP_PASSWORD = "tona@b1Utw3)[H-wRJ|uh1-CE"
    LUIS_APP_ID = "e919dd6c-f4f9-4282-ae8c-d9d944d79940"
    LUIS_API_KEY = "0656ff5a0d2c4a28954eedb0cd696c23"
    # LUIS endpoint host name, ie "westus.api.cognitive.microsoft.com"
    LUIS_API_HOST_NAME = "westeurope.api.cognitive.microsoft.com"
    LUIS_AUTH_KEY = "0e20947b94844978bbf151bf90243ff0"  # Authoring Key
    LUIS_AUTH_ENDPOINT = "https://sidney.cognitiveservices.azure.com/"  # Authoring Endpoint
    APPINSIGHTS_INSTRUMENTATION_KEY = "ec426a1e-af3f-4391-9d24-d3abdd7347d6"
