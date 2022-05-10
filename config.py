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
    LUIS_APP_ID = "ccfaf05f-d1f8-4f77-afb5-348409f11bea"
    LUIS_API_KEY = "141cab2ee9d44fc8917c782b1919d9bf"
    # LUIS endpoint host name, "westus.api.cognitive.microsoft.com"
    LUIS_API_HOST_NAME = "westeurope.api.cognitive.microsoft.com"
    LUIS_AUTH_KEY = "4591d4b660a946cbab662484013781eb"  # Authoring Key
    LUIS_AUTH_ENDPOINT = "https://theone.cognitiveservices.azure.com/"  # Authoring Endpoint
    APPINSIGHTS_INSTRUMENTATION_KEY = "ec426a1e-af3f-4391-9d24-d3abdd7347d6"

