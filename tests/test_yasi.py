#!/usr/bin/env python
# coding: utf-8

# Disable pylint warnings on methods without docstrings and too many public methods
# pylint: disable=C0111,R0904

""" Test suite for yasi
"""

import os
import sys
import unittest

PROJECT_DIR = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
sys.path.insert(0, PROJECT_DIR)

import yasi


class UnitTests(unittest.TestCase):

    def test_find_line_ending_only_lf(self):
        source = 'First Line\n Second Line\n'
        self.assertEqual(yasi.LF, yasi.find_line_ending(source))

    def test_find_line_ending_only_crlf(self):
        source = 'First Line\r\n Second Line\r\n'
        self.assertEqual(yasi.CRLF, yasi.find_line_ending(source))

    def test_find_line_ending_only_cr(self):
        source = 'First Line\r Second Line\r'
        self.assertEqual(yasi.CR, yasi.find_line_ending(source))

    def test_find_line_ending_lf_with_cr_and_crlf(self):
        source = 'First Line\r Second Line\r\n Third Line\n Fourth Line \r\n'
        self.assertEqual(yasi.CRLF, yasi.find_line_ending(source))

    def test_find_line_ending_lf_with_crlf(self):
        source = 'First Line\n Second Line\r\n Third Line\n Fourth Line \r\n'
        self.assertEqual(yasi.CRLF, yasi.find_line_ending(source))

    def test_find_line_ending_cr_with_crlf(self):
        source = 'First Line\r Second Line\r\n Third Line\r Fourth Line \r\n'
        self.assertEqual(yasi.CRLF, yasi.find_line_ending(source))

    def test_find_line_ending_cr_with_lf(self):
        source = 'First Line\r Second Line\n Third Line\n Fourth Line \n\r'
        self.assertEqual(yasi.CR, yasi.find_line_ending(source))

    def test_find_line_ending_should_default_to_lf(self):
        source = 'Line without ending'
        self.assertEqual(yasi.LF, yasi.find_line_ending(source))

    def test_all_whitespace_spaces_only(self):
        source = '           '
        self.assertTrue(yasi.all_whitespace(source))

    def test_all_whitespace_no_whitespace(self):
        source = 'karamba!!'
        self.assertFalse(yasi.all_whitespace(source))

    def test_all_whitespace_empty_string(self):
        source = ''
        self.assertTrue(yasi.all_whitespace(source))

    def test_all_whitespace_tabs_and_spaces(self):
        source = '	    	    	    	    	    	    		'
        self.assertTrue(yasi.all_whitespace(source))

    def test_all_whitespace_tabs_only(self):
        source = '								'
        self.assertTrue(yasi.all_whitespace(source))

    def test_find_first_arg_pos1(self):
        source = "(     list 'one-sheep 'two-sheep )"
        self.assertEqual([11, 5], yasi.find_first_arg_pos(0, source))

    def test_find_first_arg_pos2(self):
        source = "(    list 'one-sheep 'two-sheep )"
        self.assertEqual([10, 4], yasi.find_first_arg_pos(0, source))

    def test_find_first_arg_pos3(self):
        source = "   (    list 'one-sheep 'two-sheep )"
        self.assertEqual([10, 4], yasi.find_first_arg_pos(3, source))

    def test_find_first_arg_pos_argument_in_next_line_no_trailing_space(self):
        source = '(    list'
        self.assertEqual([5, 4], yasi.find_first_arg_pos(0, source))

    def test_find_first_arg_pos_argument_in_next_line_no_spaces_before_func(self):
        source = '(list     '
        self.assertEqual([1, 0], yasi.find_first_arg_pos(0, source))

    def test_find_first_arg_pos_argument_is_func_call(self):
        source = '(list (* 12 13) (* 13 14)  '
        self.assertEqual([6, 0], yasi.find_first_arg_pos(0, source))

    def test_find_first_arg_pos_no_function1(self):
        source = '(        '
        self.assertEqual([1, 0], yasi.find_first_arg_pos(0, source))

    def test_find_first_arg_pos_no_function2(self):
        source = '('
        self.assertEqual([1, 0], yasi.find_first_arg_pos(0, source))

    def test_trim_separate_adjacent_opening_and_closing_brackets(self):
        source = ')('
        self.assertEqual(') (', yasi.trim(source))

    def test_trim_space_between_succeeding_opening_brackets(self):
        source = '( ( ( '
        self.assertEqual('((( ', yasi.trim(source))

    def test_trim_adjacent_function_and_argument_opening_bracket(self):
        source = '(print(+ 1 1))'
        self.assertEqual('(print (+ 1 1))', yasi.trim(source))

    def test_trim_space_between_succeeding_closing_brackets(self):
        source = ') ) ) '
        self.assertEqual('))) ', yasi.trim(source))

    def test_trim_spaces_before_closing_brackets(self):
        source = '(print 12    )'
        self.assertEqual('(print 12)', yasi.trim(source))

    def test_trim_extra_whitespace(self):
        source = "(print       'this)"
        self.assertEqual("(print 'this)", yasi.trim(source))

    def test_trim_leading_whitespace(self):
        source = '       (exit)'
        self.assertEqual('(exit)', yasi.trim(source))

    def test_trim_spaces_between_quote_and_opening_bracket_in_list_literal(self):
        source = "'        (12 13 14)"
        self.assertEqual("'(12 13 14)", yasi.trim(source))


class SystemTests(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()
