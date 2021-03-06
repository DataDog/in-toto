#!/usr/bin/env python
"""
<Program Name>
  test_in_toto_mock.py

<Author>
  Shikher Verma <root@shikherverma.com>

<Started>
  June 12, 2017

<Copyright>
  See LICENSE for licensing information.

<Purpose>
  Test in_toto_mock command line tool.

"""
import os
import sys
import unittest
import argparse
import shutil
import tempfile
from mock import patch

from in_toto.in_toto_mock import main as in_toto_mock_main

import tests.common



class TestInTotoMockTool(tests.common.CliTestCase):
  """Test in_toto_mock's main() - requires sys.argv patching; and
  in_toto_mock- calls runlib and error logs/exits on Exception. """
  cli_main_func = staticmethod(in_toto_mock_main)

  @classmethod
  def setUpClass(self):
    """Create and change into temporary directory,
    dummy artifact and base arguments. """

    self.working_dir = os.getcwd()

    self.test_dir = tempfile.mkdtemp()
    os.chdir(self.test_dir)

    self.test_step = "test_step"
    self.test_link = self.test_step + ".link"
    self.test_artifact = "test_artifact"
    open(self.test_artifact, "w").close()


  @classmethod
  def tearDownClass(self):
    """Change back to initial working dir and remove temp test directory. """
    os.chdir(self.working_dir)
    shutil.rmtree(self.test_dir)

  def tearDown(self):
    try:
      os.remove(self.test_link)
    except OSError:
      pass


  def test_main_required_args(self):
    """Test CLI command with required arguments. """

    args = ["--name", self.test_step, "--", "python", "--version"]
    self.assert_cli_sys_exit(args, 0)

    self.assertTrue(os.path.exists(self.test_link))


  def test_main_wrong_args(self):
    """Test CLI command with missing arguments. """

    wrong_args_list = [
      [],
      ["--name", "test-step"],
      ["--", "echo", "blub"]]

    for wrong_args in wrong_args_list:
      self.assert_cli_sys_exit(wrong_args, 2)
      self.assertFalse(os.path.exists(self.test_link))


  def test_main_bad_cmd(self):
    """Test CLI command with non-existing command. """
    # TODO: Is it safe to assume this command does not exist, or should we
    # assert for it?
    args = ["-n", "bad-command", "--", "ggadsfljasdhlasdfljvzxc"]
    self.assert_cli_sys_exit(args, 1)


if __name__ == "__main__":
  unittest.main()
