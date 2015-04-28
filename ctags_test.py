#!/usr/bin/env python3

# Ctags output should be
# <symbol name> \t <filename> \t <vim command to find that line> \t <symbol type>

import unittest
import subprocess
import tempfile

CTAGS_CONF = 'ctags.conf'

def ctags_for(lang_suffix, code_sample):
    with tempfile.NamedTemporaryFile(mode='w', suffix=lang_suffix, delete=False) as f:
        f.write(code_sample)

    return f.name, _run_ctags(f.name)
    
def _run_ctags(sample_filename):
    out = subprocess.check_output(['ctags', 
        '--options=NONE', # ignore other configuration files
        '--options=' + CTAGS_CONF, 
        '-f-', 
        sample_filename])
    result = out.decode('utf-8')
    return result


class CoffeescriptTest(unittest.TestCase):

    def assertCtag(self, source_code, symbol, vim_search_cmd, symbol_type):
        filepath, ctags_out = ctags_for('.coffee', source_code)
        self.assertIn(
            '{symbol}\t{filepath}\t{vim_search_cmd}\t{symbol_type}'.format(**locals()),
            ctags_out)

    def test_class_method(self):
        self.assertCtag(
            '  create:  ->',
            'create',
            '/^  create:  ->/;"', 
            'm')

    def test_class_constructor(self):
        self.assertCtag(
            'class stratego.CamperAppEditor extends phaser.State',
            'CamperAppEditor',
            '/^class stratego.CamperAppEditor extends phaser.State/;"',
            'c')

    def test_local_function(self):
        self.assertCtag(
            'local_function = (gfx, focusObj) ->',
            'local_function',
            '/^local_function = (gfx, focusObj) ->/;"',
            'f')

    def test_global_function(self):
        self.assertCtag(
            'window.global_function = (gfx, focusObj) ->',
            'global_function',
            '/^window.global_function = (gfx, focusObj) ->/;"',
            'f')

    def test_pkg_function(self):
        self.assertCtag(
            'window.pkg.pkg_function = (gfx, focusObj) ->',
            'pkg_function',
            '/^window.pkg.pkg_function = (gfx, focusObj) ->/;"',
            'f')

    def test_module_function(self):
        self.assertCtag(
            'module.module_function = (a, b) ->',
            'module_function',
            '/^module.module_function = (a, b) ->/;"',
            'f')

    def test_exports_function(self):
        self.assertCtag(
            'exports.exports_function = (a, b) ->',
            'exports_function',
            '/^exports.exports_function = (a, b) ->/;"',
            'f')

class JavascriptTest(unittest.TestCase):

    def assertCtag(self, source_code, symbol, vim_search_cmd, symbol_type):
        filepath, ctags_out = ctags_for('.js', source_code)
        self.assertIn(
            '{symbol}\t{filepath}\t{vim_search_cmd}\t{symbol_type}'.format(**locals()),
            ctags_out)

    def test_local_function(self):
        self.assertCtag(
            'function B_local_function(a, b){}',
            'B_local_function',
            '/^function B_local_function(a, b){}/;"',
            'f')

    def test_object_method(self):
        self.assertCtag(
            '''
var object_class = {
  constructor: function(){}
  object_method: function(){}
}
            ''',
            'object_method',
            '/^  object_method: function(){}$/;"',
            'u')

    def test_assigned_function(self):
        self.assertCtag(
            'var assigned_function = function(){}',
            'assigned_function',
            '/^var assigned_function = function(){}/;"',
            'f')


if __name__=='__main__':
    unittest.main()
