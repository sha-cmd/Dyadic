# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import json

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount

from config import DefaultConfig

from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
from msrest.authentication import CognitiveServicesCredentials

class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.
    
    async def on_message_activity(self, turn_context: TurnContext):
        await turn_context.send_activity(f"You said '{ turn_context.activity.text }'")
        # Production == slot name
        CONFIG = DefaultConfig()
        predictionKey = CONFIG.LUIS_KEY
        predictionEndpoint = CONFIG.LUIS_ENDPOINT
        app_id = CONFIG.LUIS_ID
        runtimeCredentials = CognitiveServicesCredentials(predictionKey)
        clientRuntime = LUISRuntimeClient(endpoint=predictionEndpoint, credentials=runtimeCredentials)
        predictionRequest = { "query" : f"{ turn_context.activity.text }" }
        predictionResponse = clientRuntime.prediction.get_slot_prediction(app_id, "Production", predictionRequest)
        print("Top intent: {}".format(predictionResponse.prediction.top_intent))
        print("Sentiment: {}".format (predictionResponse.prediction.sentiment))
        print("Intents: ")

        for intent in predictionResponse.prediction.intents:
            print("\t{}".format (json.dumps (intent)))
        print("Entities: {}".format (predictionResponse.prediction.entities))

    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")
