# -*- coding: utf-8 -*-
'''
Tests for the state runner
'''

# Import Python Libs
from __future__ import absolute_import, print_function, unicode_literals
import logging
import os

# Import Salt Testing Libs
from tests.support.case import ShellCase

log = logging.getLogger(__name__)


class SyncRunnerTest(ShellCase):
    '''
    Test the sync runner.
    '''
    def test_sync_all_includes_auth(self):
        '''
        '''
        ret_output = self.run_run('saltutil.sync_all')
