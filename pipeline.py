import json
import logging
import pandas as pd
import sys
import time
import traceback
import uuid

from datetime import datetime

from azure.cognitiveservices.language.luis.authoring import LUISAuthoringClient
from azure.cognitiveservices.language.luis.authoring.models import ApplicationCreateObject
from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
from msrest.authentication import CognitiveServicesCredentials
from functools import reduce

from aiohttp import web
from aiohttp.web import Request, Response, json_response
from botbuilder.core import (
    BotFrameworkAdapterSettings,
    TurnContext,
    BotFrameworkAdapter,
)
from botbuilder.core.integration import aiohttp_error_middleware
from botbuilder.schema import Activity, ActivityTypes

from bot import MyBot
from config import DefaultConfig
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.ext.azure.log_exporter import AzureEventHandler

################################################################
logger = logging.getLogger(__name__)
#logger.addHandler(AzureEventHandler(connection_string='InstrumentationKey=<your_key>'))
logger.setLevel(logging.INFO)
logger.info('Hello, World!')
################################################################


CONFIG = DefaultConfig()

# Create adapter.
# See https://aka.ms/about-bot-adapter to learn more about how bots work.
SETTINGS = BotFrameworkAdapterSettings(CONFIG.APP_ID, CONFIG.APP_PASSWORD)
#print(CONFIG.APP_ID, CONFIG.APP_PASSWORD)
ADAPTER = BotFrameworkAdapter(SETTINGS)
# LUIS adapter
authoringKey = CONFIG.LUIS_KEY
authoringEndpoint = CONFIG.LUIS_ENDPOINT
app_id = CONFIG.LUIS_ID
client = LUISAuthoringClient(authoringEndpoint, CognitiveServicesCredentials(authoringKey))
versionId = "0.1"

# Define labeled example
#client.model.add_intent(app_id, versionId, 'inform')
data = pd.read_json('notebooks/data.json', orient='records')
enlst = []
inlst = []
inlst = data['intentName'].value_counts().index.tolist()
enlst = set([value[0]['entityName'] for index, value in data['entityLabels'].iteritems() if value])
client.model.add_prebuilt(app_id, versionId, prebuilt_extractor_names=["geographyV2"])
client.model.add_prebuilt(app_id, versionId, prebuilt_extractor_names=["datetimeV2"])
for intentName in inlst:
    try:
        client.model.add_intent(app_id, versionId, intentName)
    except:
        continue
for entityName, prebuiltExtractorName in enlst.items():
    try:
        modelId = client.model.add_entity(app_id, versionId, name=entityName)


labeledExampleUtteranceWithMLEntity = data.iloc[0].to_dict()

print("Labeled Example Utterance:", labeledExampleUtteranceWithMLEntity)

# Add an example for the entity.
# Enable nested children to allow using multiple models with the same name.
# The quantity subentity and the phraselist could have the same exact name if this is set to True
client.examples.add(app_id, versionId, labeledExampleUtteranceWithMLEntity, { "enableNestedChildren": True })

