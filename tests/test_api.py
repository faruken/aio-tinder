# -*- coding: utf-8 -*-

from unittest import (TestCase, mock)

import pytest
import warnings

from aiotinder import settings
from aiotinder.controllers.api import Api
from tests import mock_http_calls

warnings.simplefilter("ignore", ResourceWarning)


class TestAPI(TestCase):
    def setUp(self):
        self.facebook_id = "1001001010"
        self.facebook_token = "EAAGmasgkjfdgFD2349DFSfksd"
        self.api = Api(self.facebook_id, self.facebook_token)

    def test_construct_url(self):
        path = "user/recs?locale=en-US"
        res = "{0}{1}".format(settings.API_URL, path)
        self.assertEqual(res, self.api.construct_url(path))

    @pytest.mark.asyncio
    @mock.patch("aiotinder.controllers.api.Api.authenticate",
                side_effect=mock_http_calls)
    async def test_authenticate(self, mock_auth):
        res = await self.api.authenticate()
        self.assertIsNotNone(res.get("token"))
