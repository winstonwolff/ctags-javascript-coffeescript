import os.path
import subprocess
import tempfile
import re
import unittest

class CTagsTester:
    '''
    Run ctags using, capture output, and check for symbols in the resulting tags list

    Ctags output should be
    <symbol name> \t <filename> \t <vim command to find that line> \t <symbol type>
    '''

    def __init__(self, testcase, lang_suffix, ctags_conf_fname, source_code):
        self.testcase = testcase
        self.testcase.assertTrue(os.path.exists(ctags_conf_fname), "Expect {} to exist".format(ctags_conf_fname))
        self.filepath, self.ctags_out = self._ctags_for(lang_suffix, ctags_conf_fname, source_code)

    def check(self, expect_symbol, expect_symbol_type, expect_vim_search_cmd=None):
        # should produce this line in the 'tags' file
        with self.testcase.subTest(expect_symbol=expect_symbol, expect_vim_search_cmd=expect_vim_search_cmd):
            expected_line = '^{symbol}\\t{filepath}\\t{search_cmd}\\t{symbol_type}'.format(
                symbol = re.escape(expect_symbol), 
                filepath = re.escape(self.filepath),
                search_cmd = re.escape(expect_vim_search_cmd) if expect_vim_search_cmd else '[^\t]*',
                symbol_type = re.escape(expect_symbol_type))
            err_msg = "\n--- Expect this line:\n    {}\n--- to be in ctags output:\n{}\n---\n".format(expected_line, indent(self.ctags_out, 4))
            search_successful = re.search(expected_line, self.ctags_out, re.MULTILINE)
            self.testcase.assertIsNotNone(search_successful, err_msg)

        # Check that only one line for the symbol was produced
        with self.testcase.subTest(expect_symbol_is_unique=expect_symbol):
            lines = self.ctags_out.split('\n')
            occurances = [line for line in lines if line.startswith(expect_symbol + '\t')]
            num_found = len(occurances)
            err_msg = "\n--- Expect '{}' to appear once but found {} in ctags output:\n{}\n---\n".format(
                expect_symbol, num_found, indent(self.ctags_out, 4))
            self.testcase.assertEqual(1, num_found, err_msg )

    @staticmethod
    def _ctags_for(lang_suffix, ctags_conf_fname, code_sample):
        '''Run ctags and return [temporary source file's filename, output]'''
        with tempfile.NamedTemporaryFile(mode='w', suffix=lang_suffix, delete=False) as f:
            f.write(code_sample)

        return f.name, CTagsTester._run_ctags(ctags_conf_fname, f.name)
        
    @staticmethod
    def _run_ctags(ctags_conf_fname, sample_filename):
        '''Run ctags and return output as string'''
        out = subprocess.check_output(['ctags', 
            '--options=NONE', # ignore other configuration files
            '--options=' + ctags_conf_fname, 
            '-f-', 
            sample_filename], 
            stderr=subprocess.STDOUT  # Hide this message: "No options will be read from files or environment"
        )
        result = out.decode('utf-8')
        return result

def indent(s, num_spaces):
    spaces = ' ' * num_spaces
    lines = s.split('\n')
    indentedLines = [spaces + l for l in lines]
    return '\n'.join(indentedLines)

