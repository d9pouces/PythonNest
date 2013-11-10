# -*- coding: utf-8 -*-
"""
Sample test module corresponding to the :mod:`pythonnest.translation` module.

A complete documentation can be found at :mod:`unittest`.

"""
import sys
import unittest
from pythonnest.translation import translation
__author__ = "flanker"
# __copyright__ = "Copyright 2013, 19pouces.net"
# __credits__ = "flanker"
# __maintainer__ = "flanker"
# __email__ = "flanker@19pouces.net"
__all__ = ['TranslationTest']


class TranslationTest(unittest.TestCase):
    """Base test cases for the sample function provided in
    :func:`pythonnest.sample.sample_function`."""
    # pylint: disable=R0904

    def test_translation(self):
        """Test the sample_function with two arguments."""
        __trans = translation('pythonnest', languages=['xx_XX'], fallback=True)
        _ = __trans.gettext
        test_str = '[ƒ——!test_string!—–]'
        if sys.version_info[0] == 2:
            _ = __trans.ugettext
            test_str = test_str.decode('utf-8')
        self.assertEqual(_('test_string'), test_str)

if __name__ == '__main__':
    unittest.main()