# -*- coding: utf-8 -*-

"""Tinder module.
"""
from typing import (AnyStr, List)

from aiotinder.models.model import User
from aiotinder.controllers.api import Api


class Tinder:
    """Tinder API response handler.
    """
    def __init__(self, facebook_id: AnyStr, facebook_token: AnyStr) -> None:
        """
        :param facebook_id: Facebook Id
        :param facebook_token: Facebook Token
        """
        self.facebook_id = facebook_id
        self.facebook_token = facebook_token
        self.tinder = Api(facebook_id, facebook_token)

    def __repr__(self) -> AnyStr:
        """
        """
        return "<Tinder(facebook_id: {0})>".format(self.facebook_id)

    async def prospective_matches(self, locale: AnyStr = "en-US") -> List[User]:
        """Returns a list of recommended matches.

        Note: API also returns recommended groups but this is ignored on purpose. Feel free
        to submit a pull request if you implement.

        :return: List of users.
        """
        response = await self.tinder.prospective(locale)
        res = []
        for result in response["results"]:
            if result.get("type") == "user":
                res.append(User(**result.get("user")))
        return res
