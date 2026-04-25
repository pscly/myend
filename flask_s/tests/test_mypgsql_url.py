import unittest

from entities.mypgsql import normalize_db_url


class NormalizeDbUrlTest(unittest.TestCase):
    def test_converts_plain_postgresql_url_to_psycopg_driver(self):
        self.assertEqual(
            normalize_db_url("postgresql://user:pwd@example.com:5432/db"),
            "postgresql+psycopg://user:pwd@example.com:5432/db",
        )

    def test_keeps_existing_driver_and_non_postgresql_urls(self):
        self.assertEqual(
            normalize_db_url("postgresql+psycopg://user:pwd@example.com/db"),
            "postgresql+psycopg://user:pwd@example.com/db",
        )
        self.assertEqual(normalize_db_url("sqlite:///local.db"), "sqlite:///local.db")
        self.assertIsNone(normalize_db_url(None))


if __name__ == "__main__":
    unittest.main()
