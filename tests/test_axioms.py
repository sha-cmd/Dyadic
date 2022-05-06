"""Fichier de tests utilisant une requête et une prédiction. La validation de cette prédiction est effectué
par l’assertion d’une sortie vers un dictionnaire de valeurs pré-établi par l’évaluateur"""

from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
from msrest.authentication import CognitiveServicesCredentials
from aiounittest.case import AsyncTestCase


class LuisTest(AsyncTestCase):
    """Fonction utilisant le format de tests générable par la commande pytest tests/ à la racine du projet.
    Le fichier pytest.ini permet de configurer notamment la gestion de la réponse asynchrone."""

    async def test_query_luis(self):
        app_id = "b60bdae3-2c61-4641-8e67-555460e637dc"
        predictionKey = "41d9afa00a284c538575ad4926339639"
        predictionEndpoint = "https://westeurope.api.cognitive.microsoft.com/"
        predictionRequest = {
            "query": "I want a flight from Paris to London, on 22th may 2022"
                     " and return on 25th may 2022, for an amount of 75 dollars."}
        ent_dict = {"75": "budget", "london": ["dst_city", "builtin.geographyV2.city"],
                    "paris": ["or_city", "builtin.geographyV2.city"],
                    "22th may 2022": "builtin.datetimeV2.date",
                    "25th may 2022": "builtin.datetimeV2.date",
                    "2022": "builtin.number", "2022": "builtin.number", "75": "builtin.number"}
        runtimeCredentials = CognitiveServicesCredentials(predictionKey)
        clientRuntime = LUISRuntimeClient(endpoint=predictionEndpoint, credentials=runtimeCredentials)
        predictionResponse = clientRuntime.prediction.resolve(app_id, query=predictionRequest)
        for x in range(len(predictionResponse.entities)):
            entity = ent_dict[predictionResponse.entities[x].entity.replace(',', '').rstrip(' ')]  # Luis capture "london ," as "london
            if not type(entity) == list:
                assert predictionResponse.entities[x].type == entity
            elif type(entity) == list:
                assert predictionResponse.entities[x].type in entity
