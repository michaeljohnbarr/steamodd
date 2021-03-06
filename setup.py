"""
Copyright (c) 2010-2013, Anthony Garcia <anthony@lagg.me>
Distributed under the ISC License (see LICENSE)
"""

from distutils.core import setup, Command
from distutils.errors import DistutilsOptionError
from unittest import TestLoader, TextTestRunner
import os
import steam

class run_tests(Command):
    description = "Run the steamodd unit tests"

    user_options = [
            ("key=", 'k', "Your API key")
            ]

    def initialize_options(self):
        self.key = None

    def finalize_options(self):
        if not self.key:
            raise DistutilsOptionError("API key is required")
        else:
            os.environ["STEAM_API_KEY"] = self.key

    def run(self):
        tests = TestLoader().discover("tests")
        TextTestRunner(verbosity = 2).run(tests)

setup(name = "steamodd",
      version = steam.__version__,
      description = "High level Steam API implementation with low level reusable core",
      packages = ["steam"],
      author = steam.__author__,
      author_email = steam.__contact__,
      url = "https://github.com/Lagg/steamodd",
      classifiers = [
          "License :: OSI Approved :: ISC License (ISCL)",
          "Intended Audience :: Developers",
          "Operating System :: OS Independent",
          "Programming Language :: Python"
          ],
      license = steam.__license__,
      cmdclass = {"run_tests": run_tests})
