# -*- coding: utf-8 -*-

"""API connector module for Tinder API.
"""

import warnings
from http import HTTPStatus
from typing import (AnyStr, Dict, List, TypeVar, Any)

import aiohttp
import ujson as json

from src.models.model import User
from src.controllers import exceptions
from src import settings

warnings.resetwarnings()

T = TypeVar("T", int, List)
G = TypeVar("G", bool, int, AnyStr, List)


class Api:
    """API
    """
    def __init__(self, facebook_id: AnyStr, facebook_token: AnyStr,
                 tinder_token: AnyStr = None) -> None:
        """
        :param facebook_id: Facebook ID
        :param facebook_token: Facebook Token
        :param tinder_token: Tinder Token
        """
        self.token = facebook_token
        self.id = facebook_id
        self.tinder_token = tinder_token
        self.headers = settings.HEADERS
        self.session = aiohttp.ClientSession(headers=self.headers)

    def __del__(self) -> None:
        """
        """
        self.session.close()

    def construct_url(self, path: AnyStr) -> AnyStr:
        """Construct given path with the Tinder API URL.
        :param path: Relative URL
        :return: Constructed full URL.
        """
        return "{0}{1}".format(settings.API_URL, path)

    async def request(self, method: AnyStr, path: AnyStr,
                      data: Dict[AnyStr, int] = None) -> Dict:
        """Make a request to the Tinder API.
        :param method: HTTP Method to make a request (GET, POST etc.)
        :param path: Relative URL to make the request.
        :param data: Data to to pass to the API.
        :return: JSON response.
        """
        payload = None
        if data is not None:
            payload = json.dumps(data)
        if not self.tinder_token:
            await self.authenticate()
        url = self.construct_url(path)
        async with self.session.request(method, url, headers=self.headers,
                                        data=payload) as response:
            if response.status != HTTPStatus.OK:
                raise exceptions.TinderConnectionException(
                    "Response status was {0}".format(response.status))
            return await response.json()

    async def authenticate(self) -> Dict[AnyStr, Dict[AnyStr, Any]]:
        """Authenticate with Tinder API. Once we get the `token` from Tinder,
        we use this token to sign the requests while making other
        requests (dislike, profile etc.)
        :return: JSON response.
        """
        payload = json.dumps({"facebook_id": self.id,
                              "facebook_token": self.token})
        url = self.construct_url("auth")
        async with self.session.post(url, data=payload) as response:
            if response.status != HTTPStatus.OK:
                raise exceptions.TinderConnectionException("Cannot connect to Tinder. Response: {0}".format(response.status))
            data = await response.json()
            if "token" not in data:
                raise exceptions.TinderAuthenticationException("Cannot get token")
            self.tinder_token = data.get("token")
            self.headers.update({"X-Auth-Token": self.tinder_token})
            return data

    async def profile(self) -> Dict[AnyStr, G]:
        """User profile (This is your profile)
        :return: User's profile settings.
        """
        return await self.request("get", "profile")

    async def swipe_left(self, user: User) -> Dict[AnyStr, int]:
        """Swipe left (to be not interested with the person with the given `uid`).
        :param uid: User Id to pass to the API.
        :param group:
        :return: JSON response.
        """
        # if group:
        #     return await self.request("get", "group/pass/{0}".format(uid))
        return await self.request("get", "pass/{0}?content_hash={1}".format(user._id, user.content_hash))

    async def common_connections(self, uid: AnyStr) -> Dict[AnyStr, G]:
        return await self.request("get", "user/{0}/common_connections".format(uid))

    async def swipe_right(self, uid: AnyStr) -> Dict[AnyStr, int]:
        """Swipe right (to like the person with the given `uid`)
        :param uid: User Id.
        :return: JSON Response.
        """
        return await self.request("get", "like/{0}".format(uid))

    async def prospective(self, locale: AnyStr = "en-US") -> Dict[AnyStr, T]:
        """Get recommended users from Tinder.
        :param locale: Locale setting.
        :return: JSON response.
        """
        return await self.request("get", "user/recs?locale={0}".format(locale))
