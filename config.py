#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = "Remediator\$Remediator"
    APP_PASSWORD = "lbRM2Nh21rDlQ7SoC6fyJLrPpZfqxbhsga4noW93b5XQim9ybnbRePy1Z410"
    LUIS_KEY = os.environ.get("MicrosoftSubscribeId", "Environment variable does not exist")
    LUIS_ID = os.environ.get("MicrosoftLUISId", "Environment variable does not exist")
    LUIS_ENDPOINT = os.environ.get("MicrosoftLUISEndpoint", "Environment variable does not exist")

