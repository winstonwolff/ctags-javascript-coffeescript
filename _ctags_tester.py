import unittest
import subprocess
import tempfile
import re

class CTagsTester:
    '''
    Run ctags using, capture output, and check for symbols in the resulting tags list
    '''

    def __init__(self, testcase, lang_suffix, ctags_conf_fname, source_code):
        self.testcase = testcase
        self.filepath, self.ctags_out = self._ctags_for(lang_suffix, ctags_conf_fname, source_code)

    def check(self, expect_symbol, expect_vim_search_cmd, expect_symbol_type):
        with self.testcase.subTest(expect_symbol=expect_symbol, expect_symbol_type=expect_symbol_type):
            # should produce this line in the 'tags' file
            expected_line = '{expect_symbol}\t{self.filepath}\t{expect_vim_search_cmd}\t{expect_symbol_type}'.format(**locals())
            self.testcase.assertTrue( expected_line in self.ctags_out,
                "Expected:\n    {}\nnot found in:\n{}".format(expected_line, indent(self.ctags_out, 4)))

        # Check that only one line for the symbol was produced
        with self.testcase.subTest(expect_symbol=expect_symbol):
            occurances = re.findall('{}\\t'.format(expect_symbol), self.ctags_out)
            self.testcase.assertEqual(1, len(occurances), 
                "expected symbol to appear once but found multiple:\n{}".format(indent(self.ctags_out, 4)))

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
            sample_filename], stderr=subprocess.STDOUT)
        result = out.decode('utf-8')
        return result

def indent(s, num_spaces):
    spaces = ' ' * num_spaces
    lines = s.split('\n')
    indentedLines = [spaces + l for l in lines]
    return '\n'.join(indentedLines)

