#!/usr/bin/env python3

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

    def test_functions(self):
        c = self.ctags_tester('''
function global_function(a, b){}

var object_class = {
  constructor: function(){}
  object_method: function(){}
}

var assigned_function = function(){}

Namespace.namespaced_func = function (game, x, y, key, frame) {}
            ''')
        c.check(
            expect_symbol='global_function',
            expect_vim_search_cmd='/^function global_function(a, b){}$/;"',
            expect_symbol_type='f')
        c.check(
            expect_symbol='object_method',
            expect_vim_search_cmd='/^  object_method: function(){}$/;"',
            expect_symbol_type='f')
        c.check(
            expect_symbol='assigned_function',
            expect_vim_search_cmd='/^var assigned_function = function(){}$/;"',
            expect_symbol_type='f')
        c.check(
            expect_symbol='namespaced_func',
            expect_vim_search_cmd='/^Namespace.namespaced_func = function (game, x, y, key, frame) {}$/;"',
            expect_symbol_type='f')


    def test_var(self):
        c = self.ctags_tester('''
var myarray = [1, 2];
var myobject = {a: 1};
var myvar = 1;
var myfunc = function(){};
            ''')
        c.check(
            expect_symbol='myarray',
            expect_vim_search_cmd='/^var myarray = [1, 2];$/;"',
            expect_symbol_type='a')
        c.check(
            expect_symbol='myobject',
            expect_vim_search_cmd='/^var myobject = {a: 1};$/;"',
            expect_symbol_type='o')
        c.check(
            expect_symbol='myvar',
            expect_vim_search_cmd='/^var myvar = 1;$/;"',
            expect_symbol_type='r')
        c.check(
            expect_symbol='myfunc',
            expect_vim_search_cmd='/^var myfunc = function(){};$/;"',
            expect_symbol_type='f')

    def test_jquery(self):
        c = self.ctags_tester('''
            $("#foo").bind("dollar_bind_event", function() {
            jQuery('#foo').bind("jquery_bind_event", function() {
            $(bar).bind("var_bind_event", function() {
            ''')
#             $("#foo").click('click_event', function() {
#             $("#foo").dblclick('click_event', function() {
#             $("#foo").focus('click_event', function() {
#             $("#foo").focusin('click_event', function() {
#             $("#foo").focusout('click_event', function() {
#             $("#foo").hover('click_event', function() {
#             $("#foo").keydown('click_event', function() {
#             $("#foo").keypress('click_event', function() {
#             $("#foo").keyup('click_event', function() {
#             ''')
        c.check(
            expect_symbol='"#foo".dollar_bind_event',
            expect_symbol_type='f')
        c.check(
            expect_symbol="'#foo'.jquery_bind_event",
            expect_symbol_type='f')
        c.check(
            expect_symbol="bar.var_bind_event",
            expect_symbol_type='f')


if __name__=='__main__':
    unittest.main()
