# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from enum import Enum


class Question(Enum):
    NAME = 1
    OR_CITY = 2
    DST_CITY = 3
    STR_DATE = 4
    END_DATE = 5
    BUDGET = 6
    NONE = 7


class ConversationFlow:
    def __init__(
        self, last_question_asked: Question = Question.NONE,
    ):
        self.last_question_asked = last_question_asked
