"""ConfigurationParser tests."""

from operator import itemgetter
from mock import patch
import sys

from pydocstyle.config import ConfigurationParser


def _false(_):
    return False


def _none(*_):
    return None


@patch('os.path.isdir', side_effect=_false)
@patch.object(ConfigurationParser, '_get_config_file_in_folder', _none)
@patch.object(sys, 'argv', ['pydocstyle', '/path/to/a/file.py'])
def test_default_match(isdir_function):
    """Test default match config."""
    conf = ConfigurationParser()
    conf.parse()
    list(conf.get_files_to_check())
    assert conf._cache['/path/to/a'].match == '(?!test_).*\\.py'


@patch('os.path.isdir', side_effect=_false)
@patch.object(ConfigurationParser, '_get_config_file_in_folder', _none)
@patch.object(sys, 'argv', ['pydocstyle', '/path/to/a/file.py'])
def test_match_file(isdir_function):
    """Test matching a file with the default config."""
    conf = ConfigurationParser()
    conf.parse()
    assert (list(map(itemgetter(0), (conf.get_files_to_check())))
            == ['/path/to/a/file.py'])


@patch('os.path.isdir', side_effect=_false)
@patch.object(ConfigurationParser, '_get_config_file_in_folder', _none)
@patch.object(sys, 'argv', ['pydocstyle', '/path/to/a/test_file.py'])
def test_skip_test_file(isdir_function):
    """Test skipping a test file (`test_*`) with the default config."""
    conf = ConfigurationParser()
    conf.parse()
    assert list(map(itemgetter(0), (conf.get_files_to_check()))) == []
