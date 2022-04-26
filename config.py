#!/usr/bin/env python
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Configuration for the bot."""

import os


class DefaultConfig:
    """Configuration for the bot."""

    PORT = 3978
    APP_ID = "8a173d35-e05f-45f7-a982-3da8307c7514"
    APP_PASSWORD = "b.e8Q~hoxcaSndsqxaTVOVc4y-M5YpeglFXbPa0X"
    LUIS_APP_ID = "c5a9c03c-654b-43cc-b113-f2a80a849554"
    LUIS_API_KEY = "708b8499902a49d6902bdfae011bca08"
    # LUIS endpoint host name, ie "westus.api.cognitive.microsoft.com"
    LUIS_API_HOST_NAME = "sofistica.cognitiveservices.azure.com"
    APPINSIGHTS_INSTRUMENTATION_KEY = "696fdbb2-d595-4695-8acb-70385c5be202"
