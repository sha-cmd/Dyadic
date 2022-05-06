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
    LUIS_APP_ID = "b60bdae3-2c61-4641-8e67-555460e637dc"
    LUIS_API_KEY = "41d9afa00a284c538575ad4926339639"
    # LUIS endpoint host name, ie "westus.api.cognitive.microsoft.com"
    LUIS_API_HOST_NAME = "westeurope.api.cognitive.microsoft.com"
    LUIS_AUTH_KEY = "c343d2bd55a3499b8f345894394d70b5"  # Authoring Key
    LUIS_AUTH_ENDPOINT = "https://silicon.cognitiveservices.azure.com/"  # Authoring Endpoint
    APPINSIGHTS_INSTRUMENTATION_KEY = "ec426a1e-af3f-4391-9d24-d3abdd7347d6"
