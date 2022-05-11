#!/usr/bin/env python
"""Fichier de tests utilisant une requête et une prédiction. La validation de cette prédiction est effectué
par l’assertion d’une sortie vers un dictionnaire de valeurs pré-établies par l’évaluateur"""

import os

from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
from msrest.authentication import CognitiveServicesCredentials


async def query_luis_test(luisappid, luisapikey, luisapihostname):
    app_id = luisappid
    predictionKey = luisapikey
    predictionEndpoint = "https://" + luisapihostname
    predictionRequest = {
        "query": "I want a flight from Paris to London, on 22th may 2022"
                 " and return on 25th may 2022, for an amount of 75 dollars."}
    ent_dict = {"75": ["budget", "builtin.number"], "london": ["dst_city", "builtin.geographyV2.city"],
                "paris": ["or_city", "builtin.geographyV2.city"],
                "22th may 2022": "builtin.datetimeV2.date",
                "25th may 2022": "builtin.datetimeV2.date",
                "2022": "builtin.number", "2022": "builtin.number"}
    runtimeCredentials = CognitiveServicesCredentials(predictionKey)
    clientRuntime = LUISRuntimeClient(endpoint=predictionEndpoint, credentials=runtimeCredentials)
    predictionResponse = clientRuntime.prediction.resolve(app_id, query=predictionRequest)
    for x in range(len(predictionResponse.entities)):
        entity = ent_dict[predictionResponse.entities[x].entity.replace(',', '').rstrip(' ')]  # Luis capture "london ," as "london
        if not type(entity) == list:
            assert predictionResponse.entities[x].type == entity
        elif type(entity) == list:
            assert predictionResponse.entities[x].type in entity
