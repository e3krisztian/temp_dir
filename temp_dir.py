'''
Change into newly created temporary directory for executing a block of code.

Intended as a tool to ease "integration" testing.

Similar functionality can be found at

- test.test_support.temp_cwd
  (http://docs.python.org/3/library/test.html#test.support.temp_cwd)
  in the Python distribution

    - temp_cwd is quite close to this module,
      unfortunately it is not in the standard library,
      but packaged together with the regression tests.
      temp_cwd's source shows some special cases
      and runs the code in a directory that can be guessed

- tempdir (https://bitbucket.org/another_thomas/tempdir)

- tempdirs (https://github.com/thelinuxkid/tempdirs)
    - for creating any number of temporary directories

- path.py (https://github.com/jaraco/path.py/blob/master/path.py)
    - tempdir at the end of the file

'''

import tempfile
import shutil
import os
import functools
import contextlib


@contextlib.contextmanager
def in_temp_dir():
    """ Change into a temporary directory for the duration of the block.

    On exit the original working directory is restored and the temporary
    directory is removed.

    with in_temp_dir():
        tempfile = open("tempfile", "w")
        ...
    """
    original_directory = os.getcwd()
    temporary_directory = tempfile.mkdtemp()
    os.chdir(temporary_directory)
    try:
        yield temporary_directory
    finally:
        try:
            os.chdir(original_directory)
        finally:
            shutil.rmtree(temporary_directory)


def within_temp_dir(func):
    """ Make the decorated function execute in a temporary directory.

    Create & change into a temporary directory, when the decorated function
    is called.
    On exit the original working directory is restored and the temporary
    directory is removed.

    @within_temp_dir
    def f():
        tempfile = open("tempfile", "w")
        ...
    """

    @functools.wraps(func)
    def decorated(*args, **kwargs):
        with in_temp_dir():
            return func(*args, **kwargs)

    return decorated
