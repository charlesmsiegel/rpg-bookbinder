import sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "mcp_servers"))
from _lib import config, content_ops

class TestBannedTerms(unittest.TestCase):
    def _tmp(self, text):
        f = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8")
        f.write(text); f.close()
        return f.name

    def setUp(self):
        config.load(force_reload=True)

    def test_wildcard_phrase_caught(self):
        p = self._tmp("It's not magic, it's science.\n")
        out = content_ops.check_banned_terms(p)
        self.assertIn("banned phrase", out.lower())
        self.assertIn("line 1", out.lower())

    def test_banned_name_caught(self):
        p = self._tmp("The sorceress Elara waited.\n")
        out = content_ops.check_banned_terms(p)
        self.assertIn("Elara", out)

    def test_sparingly_threshold(self):
        # 'tapestry' allowed 1 per 10k words; 3 uses in a tiny file must flag
        p = self._tmp("tapestry one. tapestry two. tapestry three.\n")
        out = content_ops.check_banned_terms(p)
        self.assertIn("tapestry", out.lower())
        self.assertIn("use-sparingly", out.lower())

    def test_clean_file_passes(self):
        p = self._tmp("Plain, honest prose about a city at night.\n")
        out = content_ops.check_banned_terms(p)
        self.assertIn("no violations", out.lower())

if __name__ == "__main__":
    unittest.main()
