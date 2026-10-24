"""Do not fall back to vulnerable glyph dependencies on an old interpreter."""
import unittest
from unittest.mock import patch

import setup_tools


class GlyphRuntimeTests(unittest.TestCase):
    def test_python310_refused_before_environment_changes(self):
        with patch.object(setup_tools.sys, 'version_info', (3, 10)), \
                patch.object(setup_tools.venv, 'EnvBuilder') as builder, \
                patch.object(setup_tools.subprocess, 'run') as run:
            with self.assertRaisesRegex(SystemExit, 'Python 3.11'):
                setup_tools.main()
            builder.assert_not_called()
            run.assert_not_called()
