# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


class BookingDetails:
    def __init__(
        self,
        init_text: str = None,
        destination: str = None,
        origin: str = None,
        str_date: str = None,
        end_date: str = None,
        budget: str = None
    ):
        self.init_text = init_text
        self.destination = destination
        self.origin = origin
        self.str_date = str_date
        self.end_date = end_date
        self.budget = budget
