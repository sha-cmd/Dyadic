# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


class UserProfile:
    def __init__(self, name: str = None, or_city: str = None,
                 dst_city: str = None, str_date: str = None,
                 end_date: str = None, budget: int = 0):
        self.name = name
        self.or_city = or_city
        self.dst_city = dst_city
        self.str_date = str_date
        self.end_date = end_date
        self.budget = budget
