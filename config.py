#!/usr/bin/env python
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Configuration for the bot."""

import os


class DefaultConfig:
    """Configuration for the bot."""

    PORT = 3978
    APP_ID = "e27587f8-332e-4207-87eb-94ac5a02cbdb"
    APP_PASSWORD = "b.e8Q~hoxcaSndsqxaTVOVc4y-M5YpeglFXbPa0X"
    LUIS_APP_ID = "c5a9c03c-654b-43cc-b113-f2a80a849554"
    LUIS_API_KEY = "da69cdddb90f4046b807cf9b7a2e6eb2"
    # LUIS endpoint host name, ie "westus.api.cognitive.microsoft.com"
    LUIS_API_HOST_NAME = "northeurope.api.cognitive.microsoft.com/"
    LUIS_KEY = "708b8499902a49d6902bdfae011bca08"  # Authoring Key
    LUIS_ENDPOINT = "https://sofistica.cognitiveservices.azure.com/"  # Authoring Endpoint
    APPINSIGHTS_INSTRUMENTATION_KEY = "696fdbb2-d595-4695-8acb-70385c5be202"
