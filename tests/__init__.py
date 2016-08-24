# -*- coding: utf-8 -*-

from typing import (NamedTuple, AnyStr)

import ujson as json
from aiotinder import settings

MockTinderResponse = NamedTuple("MockTinderResponse",
                                [("payload", AnyStr),
                                 ("status", int)])


def mock_http_calls(*args, **kwargs) -> MockTinderResponse:
    auth_url = "{0}{1}".format(settings.API_URL, "auth")
    recs_url = "{0}{1}".format(settings.API_URL, "user/recs?locale=en-US")
    pass_url = "pass/{0}?content_hash={1}".format("311312", "EeaalrkC3434")
    like_url = "like/{0}?content_hash={1}".format("311312", "EeaalrkC3434")
    mapp = {
        auth_url: json.dumps({"token": "cd2b0101-f01c-4761-a1c6-d8609a1a8f41"}),
        recs_url: json.dumps(
            {"results": [{"_id": "1231312321", "name": "MLady"}]}),
        pass_url: json.dumps({"status": 200}),
        like_url: json.dumps({"status": 200})
    }
    response = mapp.get(args[0])
    if mapp.get(args[0]) is not None:
        return MockTinderResponse(response, 200)
    return MockTinderResponse(json.dumps({"error": None}), 404)
