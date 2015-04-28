#!/usr/bin/env python3

# Ctags output should be
# <symbol name> \t <filename> \t <vim command to find that line> \t <symbol type>

import unittest
import subprocess
import pathlib

CTAGS_CONF = '_ctags'

def _run_ctags(sample_filename):
    out = subprocess.check_output(['ctags', 
        '--options=NONE', # ignore other configuration files
        '--options=' + CTAGS_CONF, 
        '-f', '-', 
        sample_filename])
    result = out.decode('utf-8')
    print('--- ctags output for', sample_filename, '---\n', result)
    return result


class CoffeescriptTest(unittest.TestCase):

    def assertHasSymbol(self, symbol, vim_search_cmd, symbol_type):
        self.assertIn(
            '{symbol}\tsample.coffee\t{vim_search_cmd}\t{symbol_type}'.format(**locals()),
            self.ctags_out)

    def setUp(self):
        self.ctags_out = _run_ctags('sample.coffee')

    def test_class_method(self):
        self.assertIn(
            'create\tsample.coffee\t/^  create:  ->$/;"\tm',
            self.ctags_out)

    def test_class_constructor(self):
        self.assertIn(
            'CamperAppEditor\tsample.coffee\t/^class stratego.CamperAppEditor extends phaser.State$/;"\tc',
            self.ctags_out)

    def test_local_function(self):
        self.assertHasSymbol(
            'local_function',
            '/^local_function = (gfx, focusObj) ->$/;"',
            'f')

    def test_global_function(self):
        self.assertHasSymbol(
            'global_function',
            '/^window.global_function = (gfx, focusObj) ->$/;"',
            'f')

    def test_pkg_function(self):
        self.assertHasSymbol(
            'pkg_function',
            '/^window.pkg.pkg_function = (gfx, focusObj) ->$/;"',
            'f')

    def test_module_function(self):
        self.assertHasSymbol(
            'module_function',
            '/^module.module_function = (a, b) ->$/;"',
            'f')

    def test_exports_function(self):
        self.assertHasSymbol(
            'exports_function',
            '/^exports.exports_function = (a, b) ->$/;"',
            'f')

class JavascriptTest(unittest.TestCase):

    def setUp(self):
        self.ctags_out = _run_ctags('sample.js')

    def test_local_function(self):
        self.assertIn(
            'B_local_function\tsample.js\t/^function B_local_function(a, b){}$/;"\tf',
            self.ctags_out)

    def test_object_class_constructor(self):
        self.assertIn(
            'object_method\tsample.js\t/^  object_method: function(){}$/;"\tu',
            self.ctags_out)

if __name__=='__main__':
    unittest.main()
