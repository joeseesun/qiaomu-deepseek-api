import importlib.util
import os
import tempfile
import unittest
import wave
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

spec = importlib.util.spec_from_file_location(
    "deepseek_api", Path(__file__).resolve().parents[1] / "scripts" / "deepseek_api.py")
api = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api)


class Boundaries(unittest.TestCase):
    def test_public_url_rejects_credentials_and_private_addresses(self):
        for url in ("http://user:pass@example.com", "http://127.0.0.1",
                    "https://192.168.1.4", "http://[::1]", "https://a.local"):
            with self.subTest(url=url), self.assertRaises(api.APIError):
                api.public_url(url)
        self.assertEqual(api.public_url("https://api-docs.deepseek.com/"), "https://api-docs.deepseek.com/")

    def test_redirect_never_reuses_credential(self):
        self.assertIsNone(api.NoRedirect().redirect_request(
            None, None, 307, "", {}, "https://example.com/"))

    @unittest.skipUnless(os.name == "posix", "Uses POSIX mode bits")
    def test_key_file_requires_private_permissions(self):
        with tempfile.TemporaryDirectory() as directory, patch.dict(
                os.environ, {"XDG_CONFIG_HOME": directory, "DEEPSEEK_API_KEY": ""}):
            path = api.config_path()
            path.parent.mkdir()
            path.write_text('{"api_key":"example-test-value"}')
            path.chmod(0o644)
            with self.assertRaises(api.APIError):
                api.load_key()
            path.chmod(0o600)
            self.assertEqual(api.load_key(), "example-test-value")

    def test_tts_does_not_replace_existing_wav(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "speech.wav"
            args = api.cli_parser().parse_args(["tts", "--text", "sample", "--output", str(path)])
            client = SimpleNamespace(request=lambda *a, **k: b"\x00\x02" * 1200)
            api.tts(client, args)
            with wave.open(str(path)) as audio:
                self.assertEqual((audio.getframerate(), audio.getnframes()), (24000, 1200))
            before = path.read_bytes()
            with self.assertRaises(api.APIError):
                api.tts(client, args)
            self.assertEqual(path.read_bytes(), before)


class ProviderContracts(unittest.TestCase):
    def test_refusal_does_not_return_partial_text(self):
        result = api.summarize_chat({"stop_reason": "refusal", "content": [
            {"type": "text", "text": "partial answer"},
            {"type": "web_fetch_tool_result", "kind": "read_link",
             "content": {"type": "web_fetch_tool_result_error", "error_code": "url_not_accessible"}},
        ]})
        self.assertEqual(result["status"], "refused")
        self.assertEqual(result["answer"], "")
        self.assertEqual(result["tool_results"][0]["entries"][0]["error_code"], "url_not_accessible")

    def test_file_deleted_when_model_request_fails(self):
        calls = []

        def request(path, *args, **kwargs):
            calls.append((path, kwargs.get("method", "POST")))
            if path == "/files":
                body, _ = kwargs["multipart"]
                self.assertLess(body.index(b'name="purpose"'), body.index(b'name="file"'))
                self.assertIn(b'name="expires_after[seconds]"', body)
                return {"id": "file-api-test"}
            if path == "/anthropic/v1/messages":
                self.assertTrue(kwargs["beta"])
                raise api.APIError("provider failure", "provider_error", 503)
            return {"deleted": True}

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.txt"
            path.write_text("test document")
            args = api.cli_parser().parse_args(["ask-file", str(path), "--prompt", "Read."])
            with self.assertRaises(api.APIError) as caught:
                api.ask_file(SimpleNamespace(request=request), args)
        self.assertEqual(calls[-1], ("/files/file-api-test", "DELETE"))
        self.assertTrue(caught.exception.payload["cleanup"]["deleted"])


if __name__ == "__main__":
    unittest.main()
