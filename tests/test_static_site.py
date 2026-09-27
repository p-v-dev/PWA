import os
from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).parent.parent


class StaticSiteTest(unittest.TestCase):
    def test_build_generates_public_contact_config_without_env_file(self):
        env = os.environ | {
            "CONTACT_WHATSAPP_NUMBER": "5512999999999",
            "CONTACT_WHATSAPP_MESSAGE": "Olá, quero solicitar um orçamento.",
            "CONTACT_INSTAGRAM": "pwaconstrutora",
            "CONTACT_PHONE": "(12) 99999-9999",
            "CONTACT_EMAIL": "contato@example.com",
            "CONTACT_BUSINESS_HOURS": "Segunda a sexta, das 8h às 18h",
            "CONTACT_MAPS_URL": "https://maps.app.goo.gl/example",
        }

        result = subprocess.run(
            ["node", "build.mjs"],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        config = (ROOT / "dist" / "contact-config.js").read_text(encoding="utf-8")
        self.assertIn("5512999999999", config)
        self.assertIn("pwaconstrutora", config)
        self.assertIn("contato@example.com", config)
        llms = (ROOT / "dist" / "llms.txt").read_text(encoding="utf-8")
        self.assertIn("https://wa.me/5512999999999", llms)
        self.assertNotIn("INFORMAÇÃO A PREENCHER", llms)
        self.assertFalse((ROOT / "dist" / ".env").exists())

    def test_build_rejects_invalid_contact_values(self):
        valid_env = os.environ | {
            "CONTACT_WHATSAPP_NUMBER": "5512999999999",
            "CONTACT_EMAIL": "contato@example.com",
            "CONTACT_MAPS_URL": "https://maps.app.goo.gl/example",
        }
        invalid_values = (
            ("CONTACT_WHATSAPP_NUMBER", "12999999999", "CONTACT_WHATSAPP_NUMBER"),
            ("CONTACT_EMAIL", "email-invalido", "CONTACT_EMAIL"),
            ("CONTACT_MAPS_URL", "http://example.com", "CONTACT_MAPS_URL"),
        )

        for name, value, expected_error in invalid_values:
            with self.subTest(name=name):
                result = subprocess.run(
                    ["node", "build.mjs"],
                    cwd=ROOT,
                    env=valid_env | {name: value},
                    capture_output=True,
                    text=True,
                )

                self.assertNotEqual(result.returncode, 0)
                self.assertIn(expected_error, result.stderr)

    def test_site_has_required_files_and_content(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")

        self.assertTrue((ROOT / "styles.css").exists())
        self.assertTrue((ROOT / "script.js").exists())
        self.assertTrue((ROOT / "build.mjs").exists())
        self.assertTrue((ROOT / ".env.example").exists())
        self.assertIn("PWA Construtora Mão de Obra Ltda", html)
        self.assertIn("São José dos Campos", html)
        self.assertNotIn("SEU_NUMERO_AQUI", html)
        self.assertNotIn("IMAGEM EXEMPLO", html)
        self.assertNotIn("INFORMAÇÃO A PREENCHER", html)
        self.assertIn('src="contact-config.js"', html)
        self.assertEqual(html.count('data-contact-link="whatsapp"'), 3)

        for field in ("instagram", "phone", "email", "businessHours", "maps"):
            self.assertIn(f'data-contact-field="{field}"', html)

        for image in ("img1.png", "img4.png", "img5.png", "img6.png", "img7.png"):
            self.assertIn(f'assets/images/{image}', html)

    def test_crawler_files_reference_the_site(self):
        robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
        llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")

        self.assertIn("Sitemap: https://SEU_DOMINIO_AQUI/sitemap.xml", robots)
        self.assertIn("# PWA Construtora Mão de Obra Ltda", llms)
        self.assertIn("https://SEU_DOMINIO_AQUI/", sitemap)


if __name__ == "__main__":
    unittest.main()
