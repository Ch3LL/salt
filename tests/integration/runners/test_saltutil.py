# -*- coding: utf-8 -*-
'''
Tests for the state runner
'''

# Import Python Libs
from __future__ import absolute_import, print_function, unicode_literals
import logging
import os
import shutil
import textwrap

# Import Salt Testing Libs
from tests.support.runtests import RUNTIME_VARS
from tests.support.case import ShellCase

# Import Salt Libs
import salt.utils.files

log = logging.getLogger(__name__)


class SyncRunnerTest(ShellCase):
    '''
    Test the sync runner.
    '''
    def setUp(self):
        self.auth_dir = os.path.join(RUNTIME_VARS.TMP_STATE_TREE, '_auth')
        if os.path.exists(self.auth_dir):
            shutil.rmtree(self.auth_dir)
        os.mkdir(self.auth_dir)

        content = textwrap.dedent('''\
            # -*- coding: utf-8 -*-
            #
            # This file exists just to test auth module sync for masters.
            ''')

        with salt.utils.files.fopen(os.path.join(self.auth_dir, 'nullauth.py'), 'w') as fp_:
            fp_.write(content)

    def tearDown(self):
        cache_auth = os.path.join(RUNTIME_VARS.TMP_ROOT_DIR, 'cache')
        if os.path.exists(self.auth_dir):
            shutil.rmtree(self.auth_dir)
        for root, dirs, files in os.walk(cache_auth):
            if '_auth' in root:
                shutil.rmtree(root)

    def test_sync_auth_includes_auth(self):
        '''
        '''
        ret_output = self.run_run('saltutil.sync_auth')
        assert '- auth.nullauth' in [ret_entry.strip() for ret_entry in ret_output]
        # Clean up?
        os.unlink(os.path.join(self.master_opts['root_dir'], 'extension_modules', 'auth', 'nullauth.py'))

    def test_sync_all_includes_auth(self):
        '''
        '''
        ret_output = self.run_run('saltutil.sync_all')
        assert '- auth.nullauth' in [ret_entry.strip() for ret_entry in ret_output]
        # Clean up?
        os.unlink(os.path.join(self.master_opts['root_dir'], 'extension_modules', 'auth', 'nullauth.py'))
