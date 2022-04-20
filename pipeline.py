"""Ce fichier permet de communiquer directement à l’instance LUIS sur Az, les données via son API REST.
La gestion des entités et des intentions est automatisable à 95%. Les features des entités doivent-être portées à
connaissance de LUIS dans le code de ce fichier, via l’API REST et n’est pas résilient en cas de changement, ou d’ajout,
de noms dans les données d’entraînement."""

import logging
import pandas as pd

from azure.cognitiveservices.language.luis.authoring import LUISAuthoringClient
from msrest.authentication import CognitiveServicesCredentials

from botbuilder.core import (
    BotFrameworkAdapterSettings,
    TurnContext,
    BotFrameworkAdapter,
)

from config import DefaultConfig

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
data = pd.read_json('data/data_train.json', orient='records')
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


