#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Not so random swipe.
"""

import asyncio
import selectors
import signal


import functools
from aiotinder.controllers.tinder import Tinder

try:
    import uvloop
except ImportError:
    pass
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


facebook_id = ""
facebook_token = ""



async def shutdown(loop: asyncio.events.AbstractEventLoop) -> None:
    await asyncio.sleep(0.1)
    loop.close()


async def random_swiper(tinder: Tinder) -> None:
    users = await tinder.prospective_matches()
    for user in users:
        value = hash(user.name)
        if value % 2 == 0:
            flag = await tinder.tinder.swipe_left(user._id)
            if flag:
                print("Name: {0}, Age: {1}, Swiped Left".format(user.name, user.age))
        else:
            flag = await tinder.tinder.swipe_right(user._id)
            if flag:
                print("Name: {0}, Age: {1}, Swiped Right".format(user.name, user.age))


def main() -> None:
    selector = selectors.SelectSelector()
    loop = asyncio.SelectorEventLoop(selector)
    asyncio.set_event_loop(loop)
    loop.set_debug(True)
    loop.add_signal_handler(signal.SIGINT, functools.partial(shutdown, loop))
    tinder = Tinder(facebook_id, facebook_token)
    loop.run_until_complete(random_swiper(tinder))


if __name__ == "__main__":
    main()
