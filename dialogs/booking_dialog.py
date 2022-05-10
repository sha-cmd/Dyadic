# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Flight booking dialog."""
import logging

from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import ConfirmPrompt, TextPrompt, PromptOptions
from botbuilder.core import MessageFactory, BotTelemetryClient, NullTelemetryClient
from botbuilder.schema import InputHints
from .cancel_and_help_dialog import CancelAndHelpDialog
from config import DefaultConfig
from opencensus.ext.azure.log_exporter import AzureLogHandler

CONFIG = DefaultConfig()
logger = logging.getLogger(__name__)

logger.addHandler(AzureLogHandler(
    connection_string='InstrumentationKey=' + CONFIG.APPINSIGHTS_INSTRUMENTATION_KEY)
)

# Number of try
global n
n = 0
global nb_of_errors  # Counter of errors
nb_of_errors = 0
global limit_of_errors  # Set the limit for errors
limit_of_errors = 2


class BookingDialog(CancelAndHelpDialog):
    """Flight booking implementation."""

    def __init__(
        self,
        dialog_id: str = None,
        telemetry_client: BotTelemetryClient = NullTelemetryClient(),
    ):
        super(BookingDialog, self).__init__(
            dialog_id or BookingDialog.__name__, telemetry_client
        )
        self.telemetry_client = telemetry_client
        text_prompt = TextPrompt(TextPrompt.__name__)
        text_prompt.telemetry_client = telemetry_client

        waterfall_dialog = WaterfallDialog(
            WaterfallDialog.__name__,
            [
                self.destination_step,
                self.origin_step,
                self.budget_step,
                self.str_date_step,
                self.end_date_step,
                self.confirm_step,
                self.final_step,
            ],
        )
        waterfall_dialog.telemetry_client = telemetry_client

        self.add_dialog(text_prompt)
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(waterfall_dialog)

        self.initial_dialog_id = WaterfallDialog.__name__

    async def destination_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Prompt for destination."""
        booking_details = step_context.options

        if booking_details.destination is None:
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("To what city would you like to travel?")
                ),
            )  # pylint: disable=line-too-long,bad-continuation

        return await step_context.next(booking_details.destination)

    async def origin_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Prompt for origin city."""
        booking_details = step_context.options

        # Capture the response to the previous step's prompt
        booking_details.destination = step_context.result
        if booking_details.origin is None:
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("From what city will you be travelling?")
                ),
            )  # pylint: disable=line-too-long,bad-continuation

        return await step_context.next(booking_details.origin)

    async def budget_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Prompt for flight budget."""
        booking_details = step_context.options

        # Capture the response to the previous step's prompt
        booking_details.origin = step_context.result
        if booking_details.budget is None:
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("How much will you spend for all in that travel?")
                ),
            )  # pylint: disable=line-too-long,bad-continuation

        return await step_context.next(booking_details.budget)

    async def str_date_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Prompt for start date."""
        booking_details = step_context.options

        # Capture the response to the previous step's prompt
        booking_details.budget = step_context.result
        if booking_details.str_date is None:
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("When must your travel begin?")
                ),
            )  # pylint: disable=line-too-long,bad-continuation

        return await step_context.next(booking_details.str_date)

    async def end_date_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Prompt for end date."""
        booking_details = step_context.options

        # Capture the response to the previous step's prompt
        booking_details.str_date = step_context.result
        if booking_details.end_date is None:
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("When do you want to stop your journey?")
                ),
            )  # pylint: disable=line-too-long,bad-continuation

        return await step_context.next(booking_details.end_date)

    async def confirm_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Confirm the information the user has provided."""
        booking_details = step_context.options

        # Capture the results of the previous step
        booking_details.end_date = step_context.result
        msg = (
            f"Please confirm, I have you traveling to: {booking_details.destination}"
            f" from: {booking_details.origin} on: {booking_details.str_date}."
            f" and {booking_details.end_date} for {booking_details.budget} dollars"
        )

        # Offer a YES/NO prompt.
        return await step_context.prompt(
            ConfirmPrompt.__name__, PromptOptions(prompt=MessageFactory.text(msg))
        )

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        # Number of try
        global n
        global nb_of_errors
        """Complete the interaction and end the dialog."""
        name = "Inquiry"
        entities_dict = {}
        booking_details = step_context.options
        entities_dict['destination'] = booking_details.destination
        entities_dict['origin'] = booking_details.origin
        entities_dict['budget'] = booking_details.budget
        entities_dict['str_date'] = booking_details.str_date
        entities_dict['end_date'] = booking_details.end_date

        if step_context.result:
            return await step_context.end_dialog(booking_details)
        else:
            n += 1  # Check if the user have tried a custom number of time
            custom_nb_time = 3
            if n < custom_nb_time:
                miss_out_on = f"I misunderstand your query, we can try {custom_nb_time - n} time more?"
                message = MessageFactory.text(miss_out_on, miss_out_on, InputHints.ignoring_input)
                await step_context.context.send_activity(message)
            else:
                n = 0
                nb_of_errors += 1
                if nb_of_errors == limit_of_errors:
                    logger.critical('LUIS has exceeded authorized limit of errors.')  # AppInsights
                miss_out_on = "I have noticed my lack of understanding, please come back after I’ll get upgraded?"
                message = MessageFactory.text(miss_out_on, miss_out_on, InputHints.ignoring_input)
                name = "Bad Inquiry"
                self.telemetry_client.track_trace(name, properties=entities_dict, severity='WARNING')
                await step_context.context.send_activity(message)
        return await step_context.end_dialog()
