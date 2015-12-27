#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 Doug Hellmann.  All rights reserved.
"""Starting a task from within a coroutine and waiting for it
"""
#end_pymotw_header

import asyncio
import functools
import logging
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format='%(message)s',
    stream=sys.stderr,
)
LOG = logging.getLogger('')


async def outer(loop):
    LOG.debug('in outer')
    task = loop.create_task(task_func())
    complete, pending = await asyncio.wait([task], loop=loop, timeout=1)
    result = '{} completed and {} pending'.format(
        len(complete), len(pending),
    )
    # Cancel remaining tasks so they do not generate errors as we exit
    # without finishing them.
    for t in pending:
        t.cancel()
    return result


async def task_func():
    LOG.debug('in task_func')
    await asyncio.sleep(2)
    return 'the result'



event_loop = asyncio.get_event_loop()

LOG.debug('creating task')
task = event_loop.create_task(outer(event_loop))

try:
    LOG.debug('entering event loop')
    event_loop.run_until_complete(task)
finally:
    LOG.debug('closing event loop')
    event_loop.close()

LOG.debug('task result: %r' % (task.result(),))
