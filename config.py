#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "Environment variable does not exist")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "Environment variable does not exist")
    SUB_ID = os.environ.get("MicrosoftSubscribeId", "Environment variable does not exist")
    LUIS_ID = os.environ.get("MicrosoftLUISId", "Environment variable does not exist")

