import logging
import pandas as pd
import time

from azure.cognitiveservices.language.luis.authoring import LUISAuthoringClient
from msrest.authentication import CognitiveServicesCredentials

from botbuilder.core import (
    BotFrameworkAdapterSettings,
    TurnContext,
    BotFrameworkAdapter,
)

from config import DefaultConfig

CONFIG = DefaultConfig()

# Create adapter.
# See https://aka.ms/about-bot-adapter to learn more about how bots work.
SETTINGS = BotFrameworkAdapterSettings(CONFIG.APP_ID, CONFIG.APP_PASSWORD)
#print(CONFIG.APP_ID, CONFIG.APP_PASSWORD)
ADAPTER = BotFrameworkAdapter(SETTINGS)
# LUIS adapter
authoringKey = CONFIG.LUIS_AUTH_KEY
authoringEndpoint = CONFIG.LUIS_AUTH_ENDPOINT
app_id = CONFIG.LUIS_APP_ID
client = LUISAuthoringClient(authoringEndpoint, CognitiveServicesCredentials(authoringKey))
versionId = "0.1"

# Publication
client.apps.update_settings(app_id, is_public=True)
responseEndpointInfo = client.apps.publish(app_id, versionId, is_staging=False, region='westeurope')


