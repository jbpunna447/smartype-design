"""Verification tests for web/tools/build.py and generated web/site/ output."""
import os
import re
import sys
import unittest

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.dirname(TOOLS_DIR)
SITE_DIR = os.path.join(WEB_DIR, "site")

if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)

import build  # noqa: E402


class WebBuildPrivacyTests(unittest.TestCase):
    def test_privacy_page_has_no_draft_banner_and_discloses_ephemeral_voice_dictation(self):
        html_text = build.privacy()
        self.assertNotIn('class="draft"', html_text)
        self.assertIn("Last updated: 18 November 2026", html_text)
        self.assertNotIn("speech is turned into text on your phone", html_text.lower())
        self.assertIn("60 seconds", html_text)
        self.assertIn("Check", html_text)
        self.assertIn("Google Firebase", html_text)
        self.assertIn("Gemini", html_text)
        self.assertIn("deleted immediately", html_text)
        self.assertIn("don't store them after the request", html_text)
        self.assertIn("don't use them to train models", html_text)
        self.assertIn("system voice input when available", html_text)
        self.assertIn("own privacy terms", html_text)

    def test_privacy_choices_anchor_satisfies_play_account_deletion_disclosure(self):
        html_text = build.privacy()
        m = re.search(r'<section id="choices">.*?</section>', html_text, flags=re.DOTALL)
        self.assertIsNotNone(m, "Missing #choices section required by Play Delete account URL")
        choices = m.group(0)
        self.assertIn("SmarType", choices)
        self.assertIn("mailto:contact@smartype.in", choices)
        self.assertIn("30 days", choices)
        for required_term in (
            "account ID",
            "name",
            "email address",
            "profile photo",
            "sign-in dates",
            "AI usage",
            "subscription status",
            "Google Play",
            "phone",
        ):
            self.assertIn(required_term, choices)
        self.assertNotIn("typing, suggestions and voice still work", choices.lower())

    def test_help_home_and_terms_align_with_cloud_voice_and_signin(self):
        help_html = build.help_page()
        home_html = build.home()
        terms_html = build.terms()

        self.assertNotIn("speech is turned into text on your phone", help_html.lower())
        self.assertIn("SmarType sends audio only when you use SmarType AI voice typing and tap Check", help_html)
        self.assertIn("60 seconds", help_html)
        self.assertIn("system voice input when available", help_html)
        self.assertIn("own privacy terms", help_html)
        self.assertNotIn("typing, suggestions and voice work without one", help_html.lower())
        self.assertNotIn("speech becomes text on your phone", home_html.lower())
        self.assertNotIn("speech to text on your phone", home_html.lower())
        self.assertNotIn("typing, suggestions and voice work without an account", home_html.lower())
        self.assertIn("Typing and suggestions work without an account.", home_html)
        self.assertIn("system voice", home_html.lower())
        self.assertIn("home.js", home_html)
        self.assertIn("site.js", home_html)
        self.assertNotIn('class="draft"', terms_html)
        self.assertIn("Last updated: 18 November 2026", terms_html)
        self.assertIn("text or voice audio", terms_html.lower())

    def test_play_buttons_link_to_play_store_without_coming_soon(self):
        expected_url = "https://play.google.com/store/apps/details?id=bha.keys.smartype"
        pages = {
            "index.html": (build.home(), 4),
            "privacy.html": (build.privacy(), 2),
            "terms.html": (build.terms(), 2),
            "help.html": (build.help_page(), 2),
            "contact.html": (build.contact(), 2),
            "404.html": (build.notfound(), 2),
        }
        anchor_re = re.compile(
            r'<a\s+class="(?P<cls>btn key[^"]*)"\s+href="(?P<href>[^"]+)"[^>]*>(?P<body>.*?)</a>',
            flags=re.DOTALL,
        )
        for name, (html_text, expected_count) in pages.items():
            with self.subTest(page=name):
                self.assertNotIn("coming soon", html_text.lower(), f"Unexpected 'coming soon' in {name}")
                self.assertNotIn("aria-disabled", html_text.lower(), f"Unexpected 'aria-disabled' in {name}")
                matches = [m for m in anchor_re.finditer(html_text) if "play-chip" in m.group("body")]
                self.assertEqual(len(matches), expected_count)
                for m in matches:
                    self.assertEqual(m.group("href"), expected_url)
                labels = [re.sub(r"<[^>]+>", "", m.group("body")).strip() for m in matches]
                self.assertEqual(labels[0], "Google Play")
                for full_label in labels[1:]:
                    self.assertEqual(full_label, "Get it on Google Play")

    def test_mobile_menu_nav_link_selector_excludes_play_button(self):
        with open(os.path.join(TOOLS_DIR, "site.css"), encoding="utf-8") as css_fh:
            css_text = css_fh.read()
        self.assertIn(".menu a:not(.btn)", css_text)
        self.assertNotRegex(css_text, r"\.menu\s+a\s*\{")

    def test_generated_site_matches_builder_and_contains_only_smartype_emails(self):
        expected_pages = {
            "index.html": build.home(),
            "privacy.html": build.privacy(),
            "terms.html": build.terms(),
            "help.html": build.help_page(),
            "contact.html": build.contact(),
            "404.html": build.notfound(),
        }
        email_re = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
        for filename, expected in expected_pages.items():
            disk_path = os.path.join(SITE_DIR, filename)
            with open(disk_path, encoding="utf-8") as fh:
                actual = fh.read()
            self.assertEqual(actual, expected, f"{filename} on disk is out of sync with build.py")
            for match in email_re.findall(actual):
                self.assertTrue(match.endswith("@smartype.in"), f"Disallowed email {match} in {filename}")
        with open(os.path.join(SITE_DIR, "assets", "site.css"), encoding="utf-8") as css_fh:
            css_text = css_fh.read()
        with open(os.path.join(TOOLS_DIR, "site.css"), encoding="utf-8") as src_css_fh:
            src_css_text = src_css_fh.read()
        self.assertEqual(css_text, src_css_text)
        self.assertIn("scroll-margin-top:", css_text)
        for root, _, files in os.walk(WEB_DIR):
            for fname in files:
                fpath = os.path.join(root, fname)
                with open(fpath, "rb") as bin_fh:
                    raw = bin_fh.read()
                if b"\x00" in raw:
                    continue
                text = raw.decode("utf-8", errors="ignore")
                for match in email_re.findall(text):
                    if re.search(r"@[0-9]+x\.(png|webp|jpg)$", match, flags=re.IGNORECASE):
                        continue
                    self.assertTrue(match.endswith("@smartype.in"), f"Disallowed email {match} in {fpath}")


if __name__ == "__main__":
    unittest.main()
