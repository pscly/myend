import io
import os
import tempfile
import unittest
from unittest.mock import patch

from app import app


class Files2PasswordTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.old_up_files_path = os.y.up_files_path
        self.old_config = dict(os.y.config)
        os.y.up_files_path = os.path.join(self.temp_dir.name, "up_files")
        os.y.config["FILES2_PWD"] = "y"
        os.makedirs(f"{os.y.up_files_path}2", exist_ok=True)
        self.save_patch = patch("app01.apis.files.view_files2.data_saves.save_data")
        self.save_patch.start()
        self.addCleanup(self.save_patch.stop)
        self.addCleanup(self._restore_state)

    def _restore_state(self):
        os.y.up_files_path = self.old_up_files_path
        os.y.config.clear()
        os.y.config.update(self.old_config)

    def test_files2_index_without_password_redirects_to_files(self):
        response = self.client.get("/files2/")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/files")

    def test_files2_index_with_default_password_lists_files(self):
        response = self.client.get("/files2/?pwd=y")

        self.assertEqual(response.status_code, 200)
        self.assertIn("下载".encode(), response.data)

    def test_files2_index_keeps_password_on_download_links(self):
        with open(f"{os.y.up_files_path}2/sample.txt", "wb") as f:
            f.write(b"sample")

        response = self.client.get("/files2/?pwd=y")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'href="sample.txt?pwd=y"', response.data)

    def test_files2_upload_page_without_password_shows_password_input(self):
        response = self.client.get("/files2/up")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'name="pwd"', response.data)
        self.assertIn("files2 上传需要输入密码才能成功".encode(), response.data)

    def test_upload_page_uses_custom_clean_card_styles(self):
        response = self.client.get("/files2/up")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'/static/css/app.css', response.data)
        self.assertIn(b'class="upload-panel"', response.data)
        self.assertIn("上传文件".encode(), response.data)

    def test_files2_upload_page_with_password_shows_password_input(self):
        response = self.client.get("/files2/up?pwd=y")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'name="pwd"', response.data)
        self.assertIn(b'value="y"', response.data)

    def test_files2_upload_without_password_stays_on_form_and_does_not_save_file(self):
        response = self.client.post(
            "/files2/up",
            data={"file": (io.BytesIO(b"secret"), "no-password.txt")},
            content_type="multipart/form-data",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("密码错误，文件未上传".encode(), response.data)
        self.assertFalse(os.path.exists(f"{os.y.up_files_path}2/no-password.txt"))

    def test_files2_upload_with_wrong_password_stays_on_form_and_does_not_save_file(self):
        response = self.client.post(
            "/files2/up",
            data={"pwd": "bad", "file": (io.BytesIO(b"secret"), "wrong-password.txt")},
            content_type="multipart/form-data",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("密码错误，文件未上传".encode(), response.data)
        self.assertFalse(os.path.exists(f"{os.y.up_files_path}2/wrong-password.txt"))

    def test_files2_upload_with_password_saves_to_up_files2(self):
        response = self.client.post(
            "/files2/up",
            data={"pwd": "y", "file": (io.BytesIO(b"secret"), "ok.txt")},
            content_type="multipart/form-data",
        )

        self.assertEqual(response.status_code, 200)
        with open(f"{os.y.up_files_path}2/ok.txt", "rb") as f:
            self.assertEqual(f.read(), b"secret")

    def test_files2_uses_configured_password(self):
        os.y.config["FILES2_PWD"] = "secret"

        wrong_response = self.client.get("/files2/?pwd=y")
        right_response = self.client.get("/files2/?pwd=secret")

        self.assertEqual(wrong_response.status_code, 302)
        self.assertEqual(wrong_response.headers["Location"], "/files")
        self.assertEqual(right_response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
