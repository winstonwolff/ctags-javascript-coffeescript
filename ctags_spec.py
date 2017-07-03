#!/usr/bin/env python3

# Rewritten tests using [expectorant](https://github.com/winstonwolff/expectorant)

import unittest
import tempfile
import re
import os.path
import subprocess
import tempfile
from expectorant import *

CTAGS_CONF = 'ctags.conf'

@describe('ctags for CoffeeScript')
def _():

    SCENARIOS = (
    #   (code                                                   symbol                 type),
        ('  @_privateClassMethod: (workspace, codeXml) ->',      '_privateClassMethod', 'm'),

        ('class package.SampleClass extends base.class',        'SampleClass', 'c'),
        ('SampleClass = React.createClass',                     'SampleClass', 'v'),
        ('exports.SampleClass = React.createClass',             'SampleClass', 'v'),
        ('exports.SampleClass = SampleClass = React.createClass', 'SampleClass', 'v'),
        ('exports.SampleClass = R.createClass',                 'SampleClass', 'v'),

        ('local_function = (gfx, focusObj) ->',                 'local_function', 'f'),
        ('window.global_function = (gfx, focusObj) ->',         'global_function', 'f'),
        ('window.pkg.pkg_function = (gfx, focusObj) ->',        'pkg_function', 'f'),
        ('module.module_function = (a, b) ->',                  'module_function', 'f'),
        ('exports.exports_function = (a, b) ->',                'exports_function', 'f'),
    )

    @it('finds symbols like {1} in source like "{0}"', repeat=SCENARIOS)
    def _(source, expect_symbol, expect_symbol_type):

        tag_output = run_ctags('.coffee', CTAGS_CONF, source)

        print(">>> SOURCE:\n", source, "\n--- OUTPUT:\n", tag_output, "\n<<<", sep="")

        matches = symbol_and_type_matches(tag_output, expect_symbol, expect_symbol_type)
        expect(len(matches)) == 1

        matches = symbol_matches(tag_output, expect_symbol)
        expect(len(matches)) == 1

    @it('finds two symbols when defined twice')
    def _():
        source = '''
            exports.double_func = (a, b) ->
            exports.double_func = (c, d) ->'''
        tag_output = run_ctags('.coffee', CTAGS_CONF, source)

        matches = symbol_and_type_matches(tag_output, 'double_func', 'f')

        expect(len(matches)) == 2

@describe('ctags for JavaScript')
def _():
    scope = None
    @before
    def _():
        nonlocal scope
        scope = Scope()

    @context('with functions defined in several forms')
    def _():

        @before
        def _():
            scope.source = '''
                function global_function(a, b){}

                var object_class = {
                  constructor: function(){}
                  object_method: function(){}
                }

                var assigned_function = function(){}

                Namespace.namespaced_func = function (game, x, y, key, frame) {}
                '''
            scope.tag_output = run_ctags('.js', CTAGS_CONF, scope.source)

        @it('finds global_function')
        def _():
            expect(len(symbol_and_type_matches(scope.tag_output, 'global_function', 'f'))) == 1

        @it('finds object_method')
        def _():
            expect(len(symbol_and_type_matches(scope.tag_output, 'object_method', 'f'))) == 1

        @it('finds assigned_function')
        def _():
            expect(len(symbol_and_type_matches(scope.tag_output, 'assigned_function', 'f'))) == 1

        @it('finds namespaced_func')
        def _():
            expect(len(symbol_and_type_matches(scope.tag_output, 'namespaced_func', 'f'))) == 1

    @context('with variables, arrays, and objects')
    def _():

        @before
        def _():
            scope.source = '''
var myarray = [1, 2];
var myobject = {a: 1};
var myvar = 1;
var myfunc = function(){};

    var indented_array = [1, 2];
    var indented_object = {a: 1};
    var indented_var = 1;
    var indented_func = function(){};
                '''
            scope.tag_output = run_ctags('.js', CTAGS_CONF, scope.source)

        @it('finds arrays')
        def _():
            expect(len(symbol_and_type_matches(scope.tag_output, 'myarray', 'a'))) == 1

        @it('finds objects')
        def _():
            expect(len(symbol_and_type_matches(scope.tag_output, 'myobject', 'o'))) == 1

        @it('finds variables')
        def _():
            expect(len(symbol_and_type_matches(scope.tag_output, 'myvar', 'r'))) == 1

        @it('finds functions')
        def _():
            expect(len(symbol_and_type_matches(scope.tag_output, 'myfunc', 'f'))) == 1

        @it('finds indented_array')
        def _():
            expect(len(symbol_and_type_matches(scope.tag_output, 'indented_array', 'a'))) == 1

        @it('finds indented_object')
        def _():
            expect(len(symbol_and_type_matches(scope.tag_output, 'indented_object', 'o'))) == 1

        @it('finds indented_var')
        def _():
            expect(len(symbol_and_type_matches(scope.tag_output, 'indented_var', 'r'))) == 1

        @it('finds indented_func')
        def _():
            expect(len(symbol_and_type_matches(scope.tag_output, 'indented_func', 'f'))) == 1

    @context('with jquery style bindings')
    def _():
        pass


    @context('with rspec style Jasmine or Mocha tests')
    def _():
        pass

@describe('ctags for SCSS')
def _():
    pass


def symbol_and_type_matches(ctags_output, expect_symbol, expect_symbol_type):
    '''
    Matcher for ctags output
    '''
    expected_line = '^{symbol}\\t[^\\t]*\\t[^\\t]*\\t{symbol_type}'.format(
            symbol = re.escape(expect_symbol),
            symbol_type = re.escape(expect_symbol_type))
    matches = re.findall(expected_line, ctags_output, re.MULTILINE)
    return matches

def symbol_matches(ctags_output, expect_symbol):
    '''
    Matcher for ctags output
    '''
    expected_line = '^{symbol}'.format(symbol = re.escape(expect_symbol))
    matches = re.findall(expected_line, ctags_output, re.MULTILINE)
    return matches


def run_ctags(lang_suffix, ctags_conf_fname, code_sample):
    '''
    Run ctags and return output as string
    '''

    with tempfile.NamedTemporaryFile(mode='w', suffix=lang_suffix, delete=False) as f:
        f.write(code_sample)

    out = subprocess.check_output(['ctags',
        '--options=NONE', # ignore other configuration files
        '--options=' + ctags_conf_fname,
        '-f-',
        f.name],
        stderr=subprocess.STDOUT  # Hide message: "No options will be read from files or environment"
    )

    result = out.decode('utf-8')
    return result
