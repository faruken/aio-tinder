# -*- coding: utf-8 -*-

"""API connector module for Tinder API.
"""
import asyncio

import warnings
from http import HTTPStatus
from typing import (AnyStr, Dict, List, TypeVar, Any)

import aiohttp
import ujson as json

from aiotinder import settings
from aiotinder.controllers import exceptions
from aiotinder.models.model import User

warnings.resetwarnings()

T = TypeVar("T", int, List)
G = TypeVar("G", bool, int, AnyStr, List)


class Api:
    """API
    """

    def __init__(self, facebook_id: AnyStr, facebook_token: AnyStr,
                 tinder_token: AnyStr = None,
                 loop: asyncio.events.AbstractEventLoop = None,
                 headers: Dict[str, str] = None) -> None:
        """
        :param facebook_id: Facebook ID
        :param facebook_token: Facebook Token
        :param tinder_token: Tinder Token
        """
        self.token = facebook_token
        self.id = facebook_id
        self.tinder_token = tinder_token
        self.headers = headers or settings.HEADERS
        self.loop = loop or asyncio.get_event_loop()
        self.session = aiohttp.ClientSession(headers=self.headers, loop=self.loop)

    def __del__(self) -> None:
        """
        """
        self.session.close()

    @staticmethod
    def construct_url(path: AnyStr) -> AnyStr:
        """Construct given path with the Tinder API URL.
        :param path: Relative URL
        :return: Constructed full URL.
        """
        return "{0}{1}".format(settings.API_URL, path)

    async def request(self, method: AnyStr, path: AnyStr,
                      data: Dict[AnyStr, Any] = None) -> Dict:
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
        url = Api.construct_url(path)
        async with self.session.request(method, url, headers=self.headers,
                                        data=payload) as response:
            if response.status != HTTPStatus.OK:
                message = "Response status was {0}".format(response.status)
                raise exceptions.TinderConnectionException(message)
            return await response.json()

    async def authenticate(self) -> Dict[AnyStr, Dict[AnyStr, Any]]:
        """Authenticate with Tinder API. Once we get the `token` from Tinder,
        we use this token to sign the requests while making other
        requests (dislike, profile etc.)
        :return: JSON response.
        """
        payload = json.dumps({"facebook_id": self.id,
                              "facebook_token": self.token})
        url = Api.construct_url("auth")
        async with self.session.post(url, data=payload) as response:
            if response.status != HTTPStatus.OK:
                message = "Connection error: {0}".format(response.status)
                raise exceptions.TinderConnectionException(message)
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
        return await self.request("get", "profile?include=spotify")

    async def swipe_left(self, user: User) -> Dict[AnyStr, int]:
        """Swipe left (to be not interested with the person with the given `uid`).
        :param user: User object.
        :param group:
        :return: JSON response.
        """
        # if group:
        #     return await self.request("get", "group/pass/{0}".format(uid))
        url_path = "pass/{0}?content_hash={1}".format(user._id, user.content_hash)
        return await self.request("get", url_path)

    async def message(self, match_id: str, message: str) -> Dict[AnyStr, G]:
        """Send message to the match.
        :param match_id: Match Id.
        :param message: Message.
        :return: JSON Response.
        """
        url_path = "user/matches/{0}".format(match_id)
        return await self.request("post", url_path, data={"message": message})

    async def meta(self, path: str = None) -> Dict[AnyStr, G]:
        """Meta information. Possible optional `path` would be superlike info.
        :param path: Additional meta path such as superlike info.
        :return: JSON Response.
        """
        if path:
            return await self.request("get", "meta/{0}".format(path))
        return await self.request("get", "meta")

    async def common_connections(self, uid: AnyStr) -> Dict[AnyStr, G]:
        """Common connections with the user with the given `uid`.
        :param uid: User Id.
        :return: JSON Response.
        """
        url_path = "user/{0}/common_connections".format(uid)
        return await self.request("get", url_path)

    async def spotify_popular(self) -> Dict[AnyStr, G]:
        """Get popular songs from Spotify
        :return: JSON Response.
        """
        url_path = "v2/profile/spotify/popular"
        return await self.request("get", url_path)

    async def spotify_theme(self, song_id: str,
                            delete: bool = False) -> Dict[AnyStr, T]:
        """Add or delete spotify anthem from profile
        :param song_id: Spotify Song ID to add
        :param delete: If it's set `True`, then we delete the anthem.
        :return: JSON Response.
        """
        url_path = "v2/profile/spotify/theme"
        if delete:
            return await self.request("delete", url_path)
        return await self.request("put", url_path, data={"id": song_id})

    async def share(self, user: User) -> Dict[AnyStr, G]:
        """Share a user with someone on your contact list.
        :param user: User
        :return: JSON Response.
        """
        url_path = "user/{0}/share".format(user._id)
        return await self.request("post", url_path)

    async def superlike(self, user: User) -> Dict[AnyStr, G]:
        """Superlike a user.
        :param user: User
        :return: JSON Response.
        """
        url_path = "like/{0}/super/".format(user._id)
        return await self.request("post", url_path,
                                  data={"content_hash": user.content_hash})

    async def swipe_right(self, user: User) -> Dict[AnyStr, int]:
        """Swipe right (to like the person with the given `uid`)
        :param user: User object.
        :return: JSON Response.
        """
        url_path = "like/{0}?content_hash={1}".format(user._id, user.content_hash)
        return await self.request("get", url_path)

    async def prospective(self, locale: AnyStr = "en-US") -> Dict[AnyStr, T]:
        """Get recommended users from Tinder.
        :param locale: Locale setting.
        :return: JSON response.
        """
        return await self.request("get", "recs/social?locale={0}".format(locale))
