#!/usr/bin/env python
"""Implements bot Activity handler."""

from botbuilder.core import (
    ActivityHandler,
    ConversationState,
    UserState,
    TurnContext,
    BotTelemetryClient,
    NullTelemetryClient,
)
from botbuilder.dialogs import Dialog, DialogExtensions


class DialogBot(ActivityHandler):
    """Main activity handler for the bot."""

    def __init__(
            self,
            conversation_state: ConversationState,
            user_state: UserState,
            dialog: Dialog,
            telemetry_client: BotTelemetryClient,
    ):
        if isinstance(conversation_state, type(None)):
            raise Exception(
                "[DialogBot]: Missing parameter. conversation_state is required"
            )
        if isinstance(user_state, type(None)):
            raise Exception("[DialogBot]: Missing parameter. user_state is required")
        if isinstance(dialog, type(None)):
            raise Exception("[DialogBot]: Missing parameter. dialog is required")

        self.conversation_state = conversation_state
        self.user_state = user_state
        self.dialog = dialog
        self.telemetry_client = telemetry_client

    async def on_message_activity(self, turn_context: TurnContext):
        await DialogExtensions.run_dialog(
            self.dialog,
            turn_context,
            self.conversation_state.create_property("DialogState"),
        )

        # Save any state changes that might have occured during the turn.
        await self.conversation_state.save_changes(turn_context, False)
        await self.user_state.save_changes(turn_context, False)

    @property
    def telemetry_client(self) -> BotTelemetryClient:
        """
        Gets the telemetry client for logging events.
        """
        return self._telemetry_client

    # pylint:disable=attribute-defined-outside-init
    @telemetry_client.setter
    def telemetry_client(self, value: BotTelemetryClient) -> None:
        """
        Sets the telemetry client for logging events.
        """
        if isinstance(value, type(None)):
            self._telemetry_client = NullTelemetryClient()
        else:
            self._telemetry_client = value
