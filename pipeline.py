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
data = pd.read_json('data/data.json', orient='records')
enlst = []
inlst = []
inlst = data['intentName'].value_counts().index.tolist()
enlst = set([value[0]['entityName'] for index, value in data['entityLabels'].iteritems() if value])
# Add prebuilt extractor
try:
    client.model.add_prebuilt(app_id, versionId, prebuilt_extractor_names=["geographyV2"])
except:
    pass
try:
    client.model.add_prebuilt(app_id, versionId, prebuilt_extractor_names=["datetimeV2"])
except:
    pass
try:
    client.model.add_prebuilt(app_id, versionId, prebuilt_extractor_names=["number"])
except:
    pass
# Add intents
for intentName in inlst:
    try:
        client.model.add_intent(app_id, versionId, intentName)
    except:
        continue
# Add entity with features
entityWithFeatures =  {'or_city': 'geographyV2',
 'dst_city': 'geographyV2',
 'str_date': 'datetimeV2',
 'end_date': 'datetimeV2'}
for entityName, prebuiltExtractorName in entityWithFeatures.items():
    try:
        modelId = client.model.add_entity(app_id, versionId, name=entityName)
        modelObject = client.model.get_entity(app_id, versionId, modelId)
        prebuiltFeatureRequiredDefinition = { "model_name": prebuiltExtractorName, "is_required": True }
        client.features.add_entity_feature(app_id, versionId, pizzaQuantityId, prebuiltFeatureRequiredDefinition)
    except: 
        continue

enlst = ['action',
         'budget',
         'category',
         'dep_time_dst',
         'dep_time_or',
         'duration',
         'count',
         'count_amenities',
         'count_category',
         'count_dst_city',
         'count_name',
         'count_seat',
         'n_adults',
         'n_children',
         'seat',
         'price',
         'gst_rating',
         'intent',
         'max_duration',
         'min_duration',
         'name',
         'ref_anaphora']

for entityName in enlst:
    try:
        modelId = client.model.add_entity(app_id, versionId, name=entityName)
    except: 
        continue

for it, sample in data.iterrows():
    try:
        labeledExampleUtteranceWithMLEntity = sample.to_dict()
        client.examples.add(app_id, versionId, labeledExampleUtteranceWithMLEntity, {"enableNestedChildren": True})
    except:
        pass
# print("Labeled Example Utterance:", labeledExampleUtteranceWithMLEntity)

# Add an example for the entity.
# Enable nested children to allow using multiple models with the same name.
# The quantity subentity and the phraselist could have the same exact name if this is set to True


