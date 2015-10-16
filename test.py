#!/usr/bin/env python3

# Ctags output should be
# <symbol name> \t <filename> \t <vim command to find that line> \t <symbol type>

import unittest
import subprocess
import tempfile
import re

CTAGS_CONF = 'ctags.conf'


class CTagsTestCase(unittest.TestCase):

    def assertCtag(self, source_code, symbol, vim_search_cmd, symbol_type):
        filepath, ctags_out = ctags_for(self.lang_suffix(), source_code)

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
            source_code='  create:  ->',
            symbol='create',
            vim_search_cmd='/^  create:  ->/;"', 
            symbol_type='m')

    def test_at_class_method(self):
        self.assertCtag(
            source_code='  @_setWorkspaceXml: (workspace, codeXml) ->',
            symbol='_setWorkspaceXml',
            vim_search_cmd='/^  @_setWorkspaceXml: (workspace, codeXml) ->/;"', 
            symbol_type='m')

    def test_class_constructor(self):
        self.assertCtag(
            source_code='class stratego.CamperAppEditor extends phaser.State',
            symbol='CamperAppEditor',
            vim_search_cmd='/^class stratego.CamperAppEditor extends phaser.State/;"',
            symbol_type='c')

    def test_local_function(self):
        self.assertCtag(
            source_code='local_function = (gfx, focusObj) ->',
            symbol='local_function',
            vim_search_cmd='/^local_function = (gfx, focusObj) ->/;"',
            symbol_type='f')

    def test_global_function(self):
        self.assertCtag(
            source_code='window.global_function = (gfx, focusObj) ->',
            symbol='global_function',
            vim_search_cmd='/^window.global_function = (gfx, focusObj) ->/;"',
            symbol_type='f')

    def test_pkg_function(self):
        self.assertCtag(
            source_code='window.pkg.pkg_function = (gfx, focusObj) ->',
            symbol='pkg_function',
            vim_search_cmd='/^window.pkg.pkg_function = (gfx, focusObj) ->/;"',
            symbol_type='f')

    def test_module_function(self):
        self.assertCtag(
            source_code='module.module_function = (a, b) ->',
            symbol='module_function',
            vim_search_cmd='/^module.module_function = (a, b) ->/;"',
            symbol_type='f')

    def test_exports_function(self):
        self.assertCtag(
            source_code='exports.exports_function = (a, b) ->',
            symbol='exports_function',
            vim_search_cmd='/^exports.exports_function = (a, b) ->/;"',
            symbol_type='f')

class JavascriptTest(CTagsTestCase):

    def lang_suffix(self):
        return '.js'

    def test_global_function(self):
        self.assertCtag(
            source_code='function global_function(a, b){}\n',
            symbol='global_function',
            vim_search_cmd='/^function global_function(a, b){}$/;"',
            symbol_type='f')

    def test_object_method(self):
        self.assertCtag(
            source_code='''
var object_class = {
  constructor: function(){}
  object_method: function(){}
}
            ''',
            symbol='object_method',
            vim_search_cmd='/^  object_method: function(){}$/;"',
            symbol_type='f')

    def test_assigned_function(self):
        self.assertCtag(
            source_code='var assigned_function = function(){}\n',
            symbol='assigned_function',
            vim_search_cmd='/^var assigned_function = function(){}$/;"',
            symbol_type='f')

    def test_function_in_namespace(self):
        self.assertCtag(
            source_code='Phaser.Sprite = function (game, x, y, key, frame) {\n',
            symbol='Sprite',
            vim_search_cmd='/^Phaser.Sprite = function (game, x, y, key, frame) {$/;"',
            symbol_type='f')

def indent(s, num_spaces):
    spaces = ' ' * num_spaces
    lines = s.split('\n')
    indentedLines = [spaces + l for l in lines]
    return '\n'.join(indentedLines)

def ctags_for(lang_suffix, code_sample):
    '''Run ctags and return [temporary source file's filename, output]'''
    with tempfile.NamedTemporaryFile(mode='w', suffix=lang_suffix, delete=False) as f:
        f.write(code_sample)

    return f.name, _run_ctags(f.name)
    
def _run_ctags(sample_filename):
    '''Run ctags and return output as string'''
    out = subprocess.check_output(['ctags', 
        '--options=NONE', # ignore other configuration files
        '--options=' + CTAGS_CONF, 
        '-f-', 
        sample_filename])
    result = out.decode('utf-8')
    return result


if __name__=='__main__':
    unittest.main()
