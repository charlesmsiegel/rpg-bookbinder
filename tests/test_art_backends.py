import json, os, sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "mcp_servers"))
from _lib import config, art_backends

WORKFLOW = {
  "3": {"class_type": "KSampler", "inputs": {"seed": "{SEED}", "positive": ["6", 0]}},
  "5": {"class_type": "EmptyLatentImage", "inputs": {"width": "{WIDTH}", "height": "{HEIGHT}"}},
  "6": {"class_type": "CLIPTextEncode", "inputs": {"text": "{PROMPT}"}},
  "7": {"class_type": "CLIPTextEncode", "inputs": {"text": "{NEGATIVE}"}}
}

class TestArtBackends(unittest.TestCase):
    def setUp(self):
        config.load(force_reload=True)
        self.wf = Path(tempfile.gettempdir()) / "bb_wf.json"
        self.wf.write_text(json.dumps(WORKFLOW), encoding="utf-8")
        self.profile = {"backend": "comfyui", "endpoint": "http://127.0.0.1:8188",
                        "workflow_file": str(self.wf), "style_prefix": "ink, ", "negative_prompt": ""}

    def test_token_substitution(self):
        payload = art_backends.build_comfyui_payload(self.profile, "a castle", "blurry", 512, 768, 42)
        s = json.dumps(payload)
        self.assertIn("a castle", s)
        self.assertIn("blurry", s)
        self.assertNotIn("{PROMPT}", s)
        self.assertNotIn("{WIDTH}", s)
        # numeric tokens became numbers
        self.assertEqual(payload["5"]["inputs"]["width"], 512)
        self.assertEqual(payload["3"]["inputs"]["seed"], 42)

    def test_missing_workflow_file_errors(self):
        p = dict(self.profile, workflow_file=str(self.wf) + ".nope")
        with self.assertRaises(ValueError) as cm:
            art_backends.build_comfyui_payload(p, "x", "", 512, 512, 1)
        self.assertIn("workflow_file", str(cm.exception))

    def test_workflow_without_prompt_token_errors(self):
        bad = Path(tempfile.gettempdir()) / "bb_wf_bad.json"
        bad.write_text(json.dumps({"6": {"inputs": {"text": "static"}}}), encoding="utf-8")
        with self.assertRaises(ValueError) as cm:
            art_backends.build_comfyui_payload(dict(self.profile, workflow_file=str(bad)), "x", "", 512, 512, 1)
        self.assertIn("{PROMPT}", str(cm.exception))

    def test_active_profile_resolves(self):
        prof = art_backends.active_profile()
        self.assertIn(prof["backend"], ("a1111", "comfyui", "manual"))

if __name__ == "__main__":
    unittest.main()
