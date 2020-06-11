"""Tests for path.py"""
import pytest
from pipenv.vendor.vistir.path import set_write_bit
import os
from stat import S_IREAD, S_IRGRP, S_IROTH

@pytest.fixture
def readonly_file(tmp_path):
    file = tmp_path / "file.txt"
    file.write_text(u'Text file contents')
    file.resolve()
    string_file = str(file)
    os.chmod(string_file, S_IREAD|S_IRGRP|S_IROTH)
    yield file

def test_set_write_bit(readonly_file):
    string_readonly_file = str(readonly_file)
    # Don't check os.W_OK by os.access
    # since this returns False when runnning by root user
    # like in docker container.
    # assert not os.access(string_readonly_file, os.W_OK)
    assert os.stat(string_readonly_file).st_mode == 0o100444
    set_write_bit(string_readonly_file)
    assert os.stat(string_readonly_file).st_mode in [0o100777, 0o100666]
    assert os.access(string_readonly_file, os.W_OK)
    readonly_file.write_text(u'Overwrite!')
