#!/usr/bin/env python3

# Ctags output should be
# <symbol name> \t <filename> \t <vim command to find that line> \t <symbol type>

import unittest
import _ctags_tester

CTAGS_CONF = 'ctags.conf'


class CoffeescriptTest(unittest.TestCase):

    def ctags_tester(self, source_code):
        return _ctags_tester.CTagsTester(self, '.coffee', CTAGS_CONF, source_code)

    def test_class_method(self):
        c = self.ctags_tester('  create:  ->')
        c.check(
            expect_symbol='create',
            expect_vim_search_cmd='/^  create:  ->/;"', 
            expect_symbol_type='m')

    def test_at_class_method(self):
        c = self.ctags_tester('  @_setWorkspaceXml: (workspace, codeXml) ->')
        c.check(
            expect_symbol='_setWorkspaceXml',
            expect_vim_search_cmd='/^  @_setWorkspaceXml: (workspace, codeXml) ->/;"', 
            expect_symbol_type='m')

    def test_class_constructor(self):
        c = self.ctags_tester('class stratego.CamperAppEditor extends phaser.State')
        c.check(
            expect_symbol='CamperAppEditor',
            expect_vim_search_cmd='/^class stratego.CamperAppEditor extends phaser.State/;"',
            expect_symbol_type='c')

    def test_local_function(self):
        c = self.ctags_tester('local_function = (gfx, focusObj) ->')
        c.check(
            expect_symbol='local_function',
            expect_vim_search_cmd='/^local_function = (gfx, focusObj) ->/;"',
            expect_symbol_type='f')

    def test_global_function(self):
        c = self.ctags_tester('window.global_function = (gfx, focusObj) ->')
        c.check(
            expect_symbol='global_function',
            expect_vim_search_cmd='/^window.global_function = (gfx, focusObj) ->/;"',
            expect_symbol_type='f')

    def test_pkg_function(self):
        c = self.ctags_tester('window.pkg.pkg_function = (gfx, focusObj) ->')
        c.check(
            expect_symbol='pkg_function',
            expect_vim_search_cmd='/^window.pkg.pkg_function = (gfx, focusObj) ->/;"',
            expect_symbol_type='f')

    def test_module_function(self):
        c = self.ctags_tester('module.module_function = (a, b) ->')
        c.check(
            expect_symbol='module_function',
            expect_vim_search_cmd='/^module.module_function = (a, b) ->/;"',
            expect_symbol_type='f')

    def test_exports_function(self):
        c = self.ctags_tester('exports.exports_function = (a, b) ->')
        c.check(
            expect_symbol='exports_function',
            expect_vim_search_cmd='/^exports.exports_function = (a, b) ->/;"',
            expect_symbol_type='f')


class JavascriptTest(unittest.TestCase):

    def ctags_tester(self, source_code):
        return _ctags_tester.CTagsTester(self, '.js', CTAGS_CONF, source_code)

    def test_global_function(self):
        c = self.ctags_tester('function global_function(a, b){}\n')
        c.check(
            expect_symbol='global_function',
            expect_vim_search_cmd='/^function global_function(a, b){}$/;"',
            expect_symbol_type='f')

    def test_object_method(self):
        c = self.ctags_tester('''
var object_class = {
  constructor: function(){}
  object_method: function(){}
}
            ''')
        c.check(
            expect_symbol='object_method',
            expect_vim_search_cmd='/^  object_method: function(){}$/;"',
            expect_symbol_type='f')

    def test_assigned_function(self):
        c = self.ctags_tester('var assigned_function = function(){}\n')
        c.check(
            expect_symbol='assigned_function',
            expect_vim_search_cmd='/^var assigned_function = function(){}$/;"',
            expect_symbol_type='f')

    def test_function_in_namespace(self):
        c = self.ctags_tester('Phaser.Sprite = function (game, x, y, key, frame) {\n')
        c.check(
            expect_symbol='Sprite',
            expect_vim_search_cmd='/^Phaser.Sprite = function (game, x, y, key, frame) {$/;"',
            expect_symbol_type='f')


if __name__=='__main__':
    unittest.main()
