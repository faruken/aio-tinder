#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import signal
import sys

import functools
import warnings

from aiotinder.controllers.tinder import Tinder

warnings.simplefilter("always", ResourceWarning)

facebook_id = ""
facebook_token = ""


async def shutdown(loop: asyncio.events.AbstractEventLoop) -> None:
    await asyncio.sleep(0.1)
    loop.close()


async def result(tinder: Tinder) -> None:
    users = await tinder.prospective_matches()
    for user in users:
        print("Name: {0}, Age: {1}".format(user.name, user.age))


def main() -> None:
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.add_signal_handler(signal.SIGINT, functools.partial(shutdown, loop))
    tinder = Tinder(facebook_id, facebook_token)
    loop.run_until_complete(result(tinder))
    sys.exit(1)


if __name__ == "__main__":
    main()
