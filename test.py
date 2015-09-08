#!/usr/bin/env python3

# Ctags output should be
# <symbol name> \t <filename> \t <vim command to find that line> \t <symbol type>

import unittest
import subprocess
import tempfile
import re

CTAGS_CONF = 'ctags.conf'

def indent(s, num_spaces):
    spaces = ' ' * num_spaces
    lines = s.split('\n')
    indentedLines = [spaces + l for l in lines]
    return '\n'.join(indentedLines)

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


class CTagsTestCase(unittest.TestCase):

    def assertCtag(self, source_code, symbol, vim_search_cmd, symbol_type):
        filepath, ctags_out = ctags_for(self.lang_suffix(), source_code)
        print('ctags_out=', ctags_out)

        expected_line = '{symbol}\t{filepath}\t{vim_search_cmd}\t{symbol_type}'.format(**locals())
        self.assertTrue( expected_line in ctags_out,
            "Expected:\n    {}\nnot found in:\n{}".format(expected_line, indent(ctags_out, 4)))

        occurances = re.findall('{}\\t'.format(symbol), ctags_out)
        self.assertEqual(1, len(occurances), 
            "expected symbol to appear once but found multiple:\n{}".format(indent(ctags_out, 4)))


class CoffeescriptTest(CTagsTestCase):

    def lang_suffix(self):
        return '.coffee'

    def test_class_method(self):
        self.assertCtag(
            '  create:  ->',
            'create',
            '/^  create:  ->/;"', 
            'm')

    def test_at_class_method(self):
        self.assertCtag(
            '  @_setWorkspaceXml: (workspace, codeXml) ->',
            '_setWorkspaceXml',
            '/^  @_setWorkspaceXml: (workspace, codeXml) ->/;"', 
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

class JavascriptTest(CTagsTestCase):

    def lang_suffix(self):
        return '.js'

    def test_global_function(self):
        self.assertCtag(
            'function global_function(a, b){}\n',
            'global_function',
            '/^function global_function(a, b){}$/;"',
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
            'f')

    def test_assigned_function(self):
        self.assertCtag(
            'var assigned_function = function(){}\n',
            'assigned_function',
            '/^var assigned_function = function(){}$/;"',
            'f')

    def test_function_in_namespace(self):
        self.assertCtag(
            'Phaser.Sprite = function (game, x, y, key, frame) {\n',
            'Sprite',
            '/^Phaser.Sprite = function (game, x, y, key, frame) {$/;"',
            'f')

if __name__=='__main__':
    unittest.main()
