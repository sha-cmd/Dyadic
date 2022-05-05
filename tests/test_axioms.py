from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
from msrest.authentication import CognitiveServicesCredentials



def query_luis_test():
    app_id = "cf9f2854-e02d-4158-9689-3cc7f023388c"
    predictionKey = "0656ff5a0d2c4a28954eedb0cd696c23"
    predictionEndpoint = "https://westeurope.api.cognitive.microsoft.com/"
    predictionRequest = {"query": "I want a flight from Paris to London, on 22th may 2022 and return on 25th may 2022, for an amount of 75 dollars."}
    typ_list = ["budget", "dst_city", "or_city", "builtin.datetimeV2.date", "builtin.datetimeV2.date",
                "builtin.geographyV2.city", "builtin.geographyV2.city", "builtin.number", "builtin.number", "builtin.number"]
    ent_list = ["75", "london ,", "paris", "22th may 2022", "25th may 2022",
                "paris", "london", "2022", "2022", "75"]
    runtimeCredentials = CognitiveServicesCredentials(predictionKey)
    clientRuntime = LUISRuntimeClient(endpoint=predictionEndpoint, credentials=runtimeCredentials)
    predictionResponse = clientRuntime.prediction.resolve(app_id, query=predictionRequest)
    for x in range(len(predictionResponse.entities)):
        assert typ_list[x] == str(predictionResponse.entities[x].type)
        assert ent_list[x] == predictionResponse.entities[x].entity