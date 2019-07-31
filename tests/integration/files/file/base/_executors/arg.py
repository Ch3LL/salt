# -*- coding: utf-8 -*-
import logging
log = logging.getLogger(__name__)

def __virtual__():
    log.critical('Loading arg executor')
    return True


def execute(*args, **kwargs):
    # we use the dunder to assert the loader is provided minionmods
    log.critical('Running arg executor')
    return __salt__['test.arg']('test.arg fired')
