"""Verification tests for web/tools/build.py and generated web/site/ output."""
import html
import json
import os
import re
import subprocess
import sys
import unittest
import xml.etree.ElementTree as ET

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.dirname(TOOLS_DIR)
REPO_DIR = os.path.dirname(WEB_DIR)
SITE_DIR = os.path.join(WEB_DIR, "site")
FASTLANE_ANDROID_DIR = os.path.join(REPO_DIR, "fastlane", "metadata", "android")

BANNED_PUBLIC_TERMS = (
    "florisboard",
    "patrickgold",
    "byok",
    "bring your own key",
    "own key",
    "personal key",
    "personal api key",
    "api key",
    "translate to telugu",
    "translate into telugu",
    "translate to tamil",
    "translate into tamil",
    "skipping sensitive",
    "skipping items android marks",
    "skipping android sensitive",
    "skips content android marks",
    "auto-cleans unpinned ones",
    "word learning",
    "शब्द सीखना",
    "పద అభ్యాసం",
    "சொல் கற்றல்",
    "password and incognito fields turn off composing",
    "turns off ai, voice dictation, autocorrect",
    "password and incognito fields automatically turn off ai, voice dictation, autocorrect",
)

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
            "compare.html": (build.compare(), 4),
            "languages.html": (build.languages_page(), 4),
            "privacy-architecture.html": (build.privacy_architecture(), 4),
            "polite-whatsapp-rewriter.html": (build.polite_whatsapp_rewriter(), 4),
            "ai-tone-translator.html": (build.ai_tone_translator(), 4),
            "rough-notes-to-neat-list.html": (build.rough_notes_to_neat_list(), 4),
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
                # Google Play is live: no Play button may say "coming soon". Only the iPhone badge (not a link) may.
                without_iphone_badge = re.sub(r'<span class="btn soon".*?</span></span>', "", html_text, flags=re.DOTALL)
                self.assertNotIn("coming soon", without_iphone_badge.lower(), f"Unexpected 'coming soon' in {name}")
                for badge in re.findall(r'<span class="btn soon".*?</span></span>', html_text, flags=re.DOTALL):
                    self.assertIn("App Store for iPhone", badge)
                    self.assertNotIn("href", badge)
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
            "compare.html": build.compare(),
            "languages.html": build.languages_page(),
            "privacy-architecture.html": build.privacy_architecture(),
            "polite-whatsapp-rewriter.html": build.polite_whatsapp_rewriter(),
            "ai-tone-translator.html": build.ai_tone_translator(),
            "rough-notes-to-neat-list.html": build.rough_notes_to_neat_list(),
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
        for js_name in ("site.js", "home.js", "tools.js"):
            with open(os.path.join(SITE_DIR, "assets", "js", js_name), encoding="utf-8") as dst_fh, open(
                os.path.join(TOOLS_DIR, js_name), encoding="utf-8"
            ) as src_fh:
                self.assertEqual(dst_fh.read(), src_fh.read(), f"{js_name} on disk is out of sync")
        with open(os.path.join(SITE_DIR, "vercel.json"), encoding="utf-8") as vercel_fh:
            self.assertEqual(vercel_fh.read(), '{\n  "cleanUrls": true,\n  "trailingSlash": false\n}\n')
        for filename, content in expected_pages.items():
            levels = [int(m) for m in re.findall(r"<h([1-6])\b", content)]
            self.assertTrue(levels and levels[0] == 1, f"{filename} must start headings at <h1>, got {levels}")
            for prev_lvl, next_lvl in zip(levels, levels[1:]):
                self.assertLessEqual(
                    next_lvl - prev_lvl, 1,
                    f"{filename} skips heading level from h{prev_lvl} to h{next_lvl}: {levels}",
                )
            for href in re.findall(r'href="(/[^"]*)"', content):
                if href.startswith("/assets/"):
                    asset_disk = os.path.join(SITE_DIR, href.lstrip("/").split("?", 1)[0])
                    self.assertTrue(os.path.isfile(asset_disk), f"Broken asset {href} in {filename}")
                    continue
                path_part, _, frag = href.partition("#")
                target_name = "index.html" if path_part in ("/", "") else (
                    path_part.lstrip("/") if path_part.endswith(".html") else f"{path_part.lstrip('/')}.html"
                )
                self.assertIn(target_name, expected_pages, f"Broken internal link {href} in {filename}")
                if frag:
                    self.assertIn(
                        f'id="{frag}"', expected_pages[target_name],
                        f"Missing anchor #{frag} in {target_name} (linked from {filename})",
                    )
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

    def test_no_byok_or_personal_key_mentions(self):
        for root, _, files in os.walk(SITE_DIR):
            for fname in files:
                fpath = os.path.join(root, fname)
                with open(fpath, "rb") as bin_fh:
                    raw = bin_fh.read()
                if b"\x00" in raw:
                    continue
                lowered = html.unescape(raw.decode("utf-8", errors="ignore")).lower()
                for banned in BANNED_PUBLIC_TERMS:
                    self.assertNotIn(banned, lowered, f"Banned term {banned!r} found in {fpath}")

    def test_comparison_page_covers_five_dimensions(self):
        html_text = build.compare()
        self.assertIn('<link rel="canonical" href="https://smartype.in/compare">', html_text)
        self.assertIn('<meta property="og:url" content="https://smartype.in/compare">', html_text)
        self.assertIn(
            '<div class="cmp-scroll" tabindex="0" role="region" aria-label="Android keyboard comparison">',
            html_text,
        )
        self.assertIn('<th scope="col"', html_text)
        self.assertIn('<th scope="row">', html_text)
        self.assertIn("SmarType vs Gboard vs SwiftKey vs Grammarly", html_text)
        self.assertIn('<th scope="col">Grammarly Android assistant</th>', html_text)
        self.assertIn("existing keyboard", html_text)
        self.assertNotIn("no indic keyboard layouts", html_text.lower())
        for competitor in ("Gboard", "SwiftKey", "Grammarly"):
            self.assertIn(competitor, html_text)
        for term in (
            "Polite",
            "22",
            "Hindi",
            "Telugu",
            "Tamil",
            "21",
            "60 seconds",
            "Check",
            "Quick Notes",
            "floating",
            "password",
            "incognito",
            "/privacy-architecture.html",
        ):
            self.assertIn(term, html_text)
        for unshipped in ("friendly", "concise", "emoji search", "smartype pro"):
            self.assertNotIn(unshipped, html_text.lower())

    def test_privacy_architecture_page_explains_on_device_boundary(self):
        html_text = build.privacy_architecture()
        privacy_html = build.privacy()
        llms_text = build.llms_txt()
        self.assertIn('<link rel="canonical" href="https://smartype.in/privacy-architecture">', html_text)
        self.assertIn('<meta property="og:url" content="https://smartype.in/privacy-architecture">', html_text)
        self.assertIn("periodically removing unpinned sensitive items older than 20 seconds by default", html_text)
        self.assertIn("periodically removes unpinned sensitive items older than 20 seconds by default", privacy_html)
        self.assertIn("periodically removing unpinned sensitive items older than 20 seconds by default", llms_text)
        repo_root = os.path.dirname(WEB_DIR)
        backup_v23 = ET.parse(os.path.join(repo_root, "app/src/main/res/xml/backup_rules.xml")).getroot()
        backup_v31 = ET.parse(os.path.join(repo_root, "app/src/main/res/xml-v31/backup_rules.xml")).getroot()
        expected_backup_set = {
            ("root", "jetpref_datastore"),
            ("file", "ime"),
            ("database", "floris_user_dictionary"),
        }
        v23_set = {(el.attrib["domain"], el.attrib["path"]) for el in backup_v23.findall("include")}
        self.assertEqual(v23_set, expected_backup_set)
        for section in ("cloud-backup", "device-transfer"):
            sec_el = backup_v31.find(section)
            self.assertIsNotNone(sec_el)
            sec_set = {(el.attrib["domain"], el.attrib["path"]) for el in sec_el.findall("include")}
            self.assertEqual(sec_set, expected_backup_set)
        for doc_text in (html_text, privacy_html, llms_text):
            self.assertNotIn("after 20 seconds", doc_text)
            self.assertIn("Android backup", doc_text)
            for backed_up_item in ("settings", "custom styles", "personal dictionary", "custom themes"):
                self.assertIn(backed_up_item, doc_text)
            self.assertNotIn("learned word suggestions, custom styles and settings also stay local unless", doc_text)
            self.assertNotIn("learned words, custom styles, and settings stay local unless", doc_text)
        self.assertIn("What stays on your phone", html_text)
        for term in (
            "keystrokes",
            "clipboard",
            "Quick Notes",
            "without an account",
            "password",
            "incognito",
            "Rewrite",
            "Translate",
            "Format",
            "60 seconds",
            "Check",
            "App Check",
            "Gemini",
            "do not store",
            "train models",
            "/privacy.html#choices",
        ):
            self.assertIn(term, html_text)
        for unshipped in ("friendly", "concise", "emoji search", "smartype pro"):
            self.assertNotIn(unshipped, html_text.lower())

    def test_citation_files_robots_sitemap_and_llms(self):
        with open(os.path.join(SITE_DIR, "sitemap.xml"), encoding="utf-8") as fh:
            sitemap_disk = fh.read()
        ET.fromstring(sitemap_disk)
        for loc in (
            "https://smartype.in/",
            "https://smartype.in/compare",
            "https://smartype.in/languages",
            "https://smartype.in/privacy-architecture",
            "https://smartype.in/polite-whatsapp-rewriter",
            "https://smartype.in/ai-tone-translator",
            "https://smartype.in/rough-notes-to-neat-list",
            "https://smartype.in/privacy",
            "https://smartype.in/terms",
            "https://smartype.in/help",
            "https://smartype.in/contact",
        ):
            self.assertIn(f"<loc>{loc}</loc>", sitemap_disk)
        self.assertNotIn("404", sitemap_disk)

        robots_expected = build.robots_txt()
        with open(os.path.join(SITE_DIR, "robots.txt"), encoding="utf-8") as fh:
            robots_disk = fh.read()
        self.assertEqual(robots_disk, robots_expected)
        for bot in ("Googlebot", "OAI-SearchBot", "GPTBot", "ClaudeBot", "PerplexityBot"):
            self.assertIn(f"User-agent: {bot}", robots_disk)
        self.assertIn("Allow: /", robots_disk)
        self.assertIn("Sitemap: https://smartype.in/sitemap.xml", robots_disk)

        llms_expected = build.llms_txt()
        with open(os.path.join(SITE_DIR, "llms.txt"), encoding="utf-8") as fh:
            llms_disk = fh.read()
        self.assertEqual(llms_disk, llms_expected)
        self.assertTrue(llms_disk.startswith("# SmarType\n"))
        for required in (
            "https://play.google.com/store/apps/details?id=bha.keys.smartype",
            "https://smartype.in/compare",
            "https://smartype.in/privacy-architecture",
            "https://smartype.in/polite-whatsapp-rewriter",
            "https://smartype.in/ai-tone-translator",
            "https://smartype.in/rough-notes-to-neat-list",
            "https://smartype.in/privacy",
            "22 built-in",
            "31",
            "60 seconds",
            "Quick Notes",
            "password",
        ):
            self.assertIn(required, llms_disk)
        for unshipped in ("friendly", "concise", "emoji search", "smartype pro"):
            self.assertNotIn(unshipped, llms_disk.lower())
        translate_line = next(line for line in llms_disk.splitlines() if "In-keyboard AI Translate" in line)
        translate_outputs = translate_line.split("outputs 31 languages: ", 1)[1]
        for lang in (
            "Arabic", "Chinese (Simplified)", "Dutch", "English", "French", "German", "Greek",
            "Hebrew", "Hindi", "Indonesian", "Italian", "Japanese", "Korean", "Polish",
            "Portuguese", "Russian", "Spanish", "Swedish", "Thai", "Turkish", "Vietnamese",
            # The Indian languages from SmarType issue 706 (owner decision 2026-11-21: the site lists them ahead of the app release).
            "Telugu", "Tamil", "Kannada", "Malayalam", "Marathi", "Bengali", "Gujarati", "Punjabi", "Odia", "Urdu",
        ):
            self.assertIn(lang, translate_outputs)
        for non_target in ("Ukrainian", "Nepali", "Sinhala"):
            self.assertNotIn(non_target, translate_outputs)


class FastlaneMetadataTests(unittest.TestCase):
    EXPECTED_LOCALES = ("en-GB", "en-US", "hi-IN", "te-IN", "ta-IN")
    ASO_PHRASES = (
        "english to hindi ai keyboard",
        "polite message rewrite keyboard",
        "voice typing punctuation keyboard",
        "private android ai keyboard",
    )

    def test_locales_and_character_limits(self):
        self.assertEqual(set(os.listdir(FASTLANE_ANDROID_DIR)), set(self.EXPECTED_LOCALES))

        for locale in self.EXPECTED_LOCALES:
            with self.subTest(locale=locale):
                locale_dir = os.path.join(FASTLANE_ANDROID_DIR, locale)
                expected_entries = {"title.txt", "short_description.txt", "full_description.txt"}
                if locale == "en-GB":
                    expected_entries.add("images")
                self.assertEqual(set(os.listdir(locale_dir)), expected_entries)
                with open(os.path.join(locale_dir, "title.txt"), encoding="utf-8") as fh:
                    title = fh.read().rstrip("\r\n")
                with open(os.path.join(locale_dir, "short_description.txt"), encoding="utf-8") as fh:
                    short_desc = fh.read().rstrip("\r\n")
                with open(os.path.join(locale_dir, "full_description.txt"), encoding="utf-8") as fh:
                    full_desc = fh.read().rstrip("\r\n")

                self.assertNotIn("\n", title)
                self.assertTrue(1 <= len(title) <= 30, f"{locale} title length {len(title)} > 30: {title!r}")
                self.assertIn("SmarType", title)

                self.assertNotIn("\n", short_desc)
                self.assertTrue(1 <= len(short_desc) <= 80, f"{locale} short_desc length {len(short_desc)} > 80")

                self.assertTrue(200 <= len(full_desc) <= 4000, f"{locale} full_desc length {len(full_desc)} out of bounds")
                for unshipped in ("friendly", "concise", "emoji search", "smartype pro"):
                    self.assertNotIn(unshipped, full_desc.lower(), f"Unshipped term {unshipped!r} in {locale}")

    def test_listings_target_four_aso_phrases_and_ban_legacy_or_byok_terms(self):
        email_re = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
        for root, _, files in os.walk(FASTLANE_ANDROID_DIR):
            for fname in files:
                if not fname.endswith(".txt"):
                    continue
                fpath = os.path.join(root, fname)
                with open(fpath, encoding="utf-8") as fh:
                    content = fh.read()
                lowered = content.lower()
                for banned in BANNED_PUBLIC_TERMS:
                    self.assertNotIn(banned, lowered, f"Banned term {banned!r} found in {fpath}")
                for match in email_re.findall(content):
                    self.assertTrue(match.endswith("@smartype.in"), f"Disallowed email {match} in {fpath}")

        for locale in self.EXPECTED_LOCALES:
            with self.subTest(locale=locale):
                locale_dir = os.path.join(FASTLANE_ANDROID_DIR, locale)
                combined = ""
                for fname in ("title.txt", "short_description.txt", "full_description.txt"):
                    with open(os.path.join(locale_dir, fname), encoding="utf-8") as fh:
                        combined += "\n" + fh.read().lower()
                for phrase in self.ASO_PHRASES:
                    self.assertIn(phrase, combined, f"{locale} missing ASO phrase {phrase!r}")

    def test_en_gb_default_store_graphics_match_design_assets(self):
        en_images = os.path.join(FASTLANE_ANDROID_DIR, "en-GB", "images")
        design_brand = os.path.join(REPO_DIR, "design", "assets", "brand", "png", "play-store-icon-512.png")
        design_feature = os.path.join(REPO_DIR, "design", "assets", "store", "en", "feature-a.png")
        with open(os.path.join(en_images, "icon.png"), "rb") as actual_fh, open(design_brand, "rb") as expected_fh:
            self.assertEqual(actual_fh.read(), expected_fh.read())
        with open(os.path.join(en_images, "featureGraphic.png"), "rb") as actual_fh, open(design_feature, "rb") as expected_fh:
            self.assertEqual(actual_fh.read(), expected_fh.read())
        screenshots_dir = os.path.join(en_images, "phoneScreenshots")
        expected_shots = [
            "01-ai-open.png",
            "02-tr-open.png",
            "03-vo-listen.png",
            "05-nt-changed.png",
            "06-cb-open.png",
            "07-lg-globe.png",
            "08-themes.png",
            "09-privacy.png",
        ]
        self.assertEqual(sorted(os.listdir(screenshots_dir)), expected_shots)
        for fname in expected_shots:
            src = os.path.join(REPO_DIR, "design", "assets", "store", "en", fname)
            dst = os.path.join(screenshots_dir, fname)
            with open(dst, "rb") as dst_fh, open(src, "rb") as src_fh:
                self.assertEqual(dst_fh.read(), src_fh.read(), f"Mismatch in {fname}")


class MicroToolRuntimeTests(unittest.TestCase):
    def test_format_rough_notes_modes_and_edge_cases(self):
        tools_js = os.path.join(TOOLS_DIR, "tools.js")
        self.assertTrue(os.path.isfile(tools_js), "Missing web/tools/tools.js")
        probe = r"""
const { formatRoughNotes } = require(process.argv[1]);
const out = {
  bullets: formatRoughNotes("book flight, 2 nights hotel, 5kg basmati rice", "bullets"),
  numbered: formatRoughNotes("1. tickets\n- passport\n[x] charger", "numbered"),
  commaMarkers: formatRoughNotes("1. tickets, 2. passport; [ ] visa", "bullets"),
  indented: formatRoughNotes("  - apples\n  - bananas,", "bullets"),
  thousands: formatRoughNotes("budget 1,000 INR, taxi 250 INR", "bullets"),
  checklist: formatRoughNotes("milk; eggs; bread", "checklist"),
  inlineDash: formatRoughNotes("basmati rice 5kg - paneer 200g - ginger & coriander", "bullets"),
  table: formatRoughNotes("Flight: AI-102 9am\nHotel - 2 nights near metro\nMeet Priya at 7:30 PM\nhttps://smartype.in", "table"),
  empty: formatRoughNotes("   \n , ;  ", "bullets"),
  bareMarkers: formatRoughNotes(" - \n 1. \n [ ] , ", "bullets"),
  xss: formatRoughNotes("<script>alert(1)</script>, a & b", "bullets"),
};
process.stdout.write(JSON.stringify(out));
"""
        proc = subprocess.run(
            ["node", "-e", probe, tools_js],
            check=True,
            capture_output=True,
            text=True,
        )
        res = json.loads(proc.stdout)
        self.assertEqual(
            res["bullets"],
            {"text": "• Book flight\n• 2 nights hotel\n• 5kg basmati rice", "empty": False},
        )
        self.assertEqual(
            res["numbered"],
            {"text": "1. Tickets\n2. Passport\n3. Charger", "empty": False},
        )
        self.assertEqual(
            res["commaMarkers"],
            {"text": "• Tickets\n• Passport\n• Visa", "empty": False},
        )
        self.assertEqual(
            res["indented"],
            {"text": "• Apples\n• Bananas", "empty": False},
        )
        self.assertEqual(
            res["thousands"],
            {"text": "• Budget 1,000 INR\n• Taxi 250 INR", "empty": False},
        )
        self.assertEqual(
            res["checklist"],
            {"text": "☐ Milk\n☐ Eggs\n☐ Bread", "empty": False},
        )
        self.assertEqual(
            res["inlineDash"],
            {"text": "• Basmati rice 5kg\n• Paneer 200g\n• Ginger & coriander", "empty": False},
        )
        self.assertEqual(
            res["table"],
            {
                "text": "Item | Details\n--- | ---\nFlight | AI-102 9am\nHotel | 2 nights near metro\nMeet Priya at 7:30 PM | —\nhttps://smartype.in | —",
                "empty": False,
            },
        )
        self.assertEqual(
            res["empty"],
            {"text": "Paste or type comma-separated or line-separated notes above.", "empty": True},
        )
        self.assertEqual(
            res["bareMarkers"],
            {"text": "Paste or type comma-separated or line-separated notes above.", "empty": True},
        )
        self.assertEqual(
            res["xss"],
            {"text": "• <script>alert(1)</script>\n• A & b", "empty": False},
        )

    def test_dom_runtime_rtl_lang_focus_and_copy_cleanup(self):
        tools_js = os.path.join(TOOLS_DIR, "tools.js")
        probe = r"""
const path = process.argv[1];
function makeEl(tag, attrs = {}) {
  const listeners = {};
  const el = {
    tagName: tag.toUpperCase(),
    dataset: Object.assign({}, attrs.dataset || {}),
    attributes: {},
    children: [],
    style: {},
    className: "",
    textContent: attrs.textContent || "",
    value: attrs.value || "",
    disabled: false,
    hidden: false,
    dir: "ltr",
    lang: "en",
    onclick: null,
    parentNode: null,
    classList: {
      toggle(c, on) {
        const parts = new Set(el.className.split(/\s+/).filter(Boolean));
        if (on) parts.add(c); else parts.delete(c);
        el.className = [...parts].join(" ");
      }
    },
    setAttribute(k, v) { el.attributes[k] = String(v); },
    getAttribute(k) { return el.attributes[k]; },
    addEventListener(ev, fn) { (listeners[ev] = listeners[ev] || []).push(fn); },
    trigger(ev) {
      if (ev === "click" && typeof el.onclick === "function") el.onclick();
      (listeners[ev] || []).forEach((fn) => fn());
    },
    appendChild(ch) { ch.parentNode = el; el.children.push(ch); return ch; },
    removeChild(ch) { el.children = el.children.filter((x) => x !== ch); ch.parentNode = null; },
    remove() { if (el.parentNode) el.parentNode.removeChild(el); },
    replaceChildren(...kids) {
      el.children.forEach((c) => { if (global.document.activeElement === c) global.document.activeElement = global.document.body; c.parentNode = null; });
      el.children = [];
      kids.forEach((k) => el.appendChild(k));
    },
    contains(target) { return target === el || el.children.includes(target); },
    focus() { global.document.activeElement = el; },
    select() { global.document.activeElement = el; },
  };
  return el;
}

function ssrRow(items) {
  const row = makeEl("div");
  items.forEach((lbl) => row.appendChild(makeEl("button", { textContent: lbl })));
  return row;
}

function runScenario(mode, cfg, initialValue = "") {
  const body = makeEl("body");
  const root = makeEl("div", { dataset: { tool: mode } });
  const g0 = (cfg.groups || [{ presets: cfg.presets || [] }])[0];
  const p0 = (g0.presets || [{ tones: [] }])[0];
  const map = {
    "[data-group-row]": ssrRow((cfg.groups || []).map((g) => g.label)),
    "[data-preset-row]": ssrRow((g0.presets || []).map((p) => p.label)),
    "[data-tone-row]": ssrRow((p0.tones || []).map((t) => t.name)),
    "[data-mode-row]": ssrRow((cfg.modes || []).map((m) => m.name)),
    "[data-source]": makeEl("div"),
    "[data-badge]": makeEl("span"),
    "[data-output]": makeEl("p"),
    "[data-sub]": makeEl("p"),
    "[data-copy]": makeEl("button"),
    "[data-copy-label]": makeEl("span", { textContent: "Copy" }),
    "[data-notes-input]": makeEl("textarea", { value: initialValue }),
  };
  root.querySelector = (sel) => map[sel] || null;
  const dataEl = makeEl("script", { textContent: JSON.stringify(cfg) });
  global.document = {
    readyState: "complete",
    body,
    activeElement: body,
    createElement: (t) => makeEl(t),
    querySelector: (sel) => (sel === "[data-tool]" ? root : null),
    getElementById: (id) => (id === "tool-data" ? dataEl : null),
    execCommand: () => { throw new Error("CopyBlocked"); },
  };
  global.navigator = {};
  delete require.cache[require.resolve(path)];
  require(path);
  return { body, map };
}

const pScene = runScenario("presets", {
  groups: [
    { label: "EN-HI", dir: "ltr", lang: "en", outLang: "hi", presets: [
      { label: "P1", raw: "Hello", tones: [{ name: "Respectful", out: "नमस्ते", sub: "Namaste" }, { name: "Warm", out: "हाय", sub: "Hi" }] },
      { label: "P1b", raw: "Thanks", tones: [{ name: "Respectful", out: "धन्यवाद", sub: "Dhanyavaad" }] },
    ] },
    { label: "AR-EN", dir: "rtl", lang: "ar", outLang: "en", presets: [{ label: "P2", raw: "مرحبا", tones: [{ name: "Polite", out: "Hello", sub: "" }] }] },
  ],
});
pScene.map["[data-tone-row]"].children[1].trigger("click");
const afterTone = pScene.map["[data-output]"].textContent;
pScene.map["[data-preset-row]"].children[1].focus();
pScene.map["[data-preset-row]"].children[1].trigger("click");
const afterPreset = pScene.map["[data-output]"].textContent;
const gBtns = pScene.map["[data-group-row]"].children;
gBtns[1].focus();
gBtns[1].trigger("click");
const afterAr = {
  srcDir: pScene.map["[data-source]"].dir,
  srcLang: pScene.map["[data-source]"].lang,
  outLang: pScene.map["[data-output]"].lang,
  focusKept: global.document.activeElement === pScene.map["[data-group-row]"].children[1],
};
pScene.map["[data-group-row]"].children[0].trigger("click");
const afterHi = {
  srcDir: pScene.map["[data-source]"].dir,
  outLang: pScene.map["[data-output]"].lang,
};

const nScene = runScenario("notes", {
  presets: [{ label: "Trip", raw: "tickets, hotel" }],
  modes: [{ id: "bullets", name: "Bullets" }, { id: "table", name: "Table" }],
}, "custom note");
const initialPresetPressed = nScene.map["[data-preset-row]"].children[0].getAttribute("aria-pressed");
const copyBtn = nScene.map["[data-copy]"];
copyBtn.focus();
copyBtn.trigger("click");
const leakedChildren = nScene.body.children.length;
const copyFocusRestored = global.document.activeElement === copyBtn;
global.document.execCommand = () => true;
copyBtn.trigger("click");
const copiedShown = nScene.map["[data-copy-label]"].textContent === "Copied";
nScene.map["[data-notes-input]"].value = "   ";
nScene.map["[data-notes-input]"].trigger("input");
const copiedReset = nScene.map["[data-copy-label]"].textContent === "Copy";
const emptyDisabled = copyBtn.disabled && nScene.map["[data-output]"].dataset.empty === "true";
nScene.map["[data-preset-row]"].children[0].trigger("click");
nScene.map["[data-mode-row]"].children[1].trigger("click");
const presetRestored = nScene.map["[data-notes-input]"].value === "tickets, hotel" && !copyBtn.disabled && nScene.map["[data-output]"].textContent.includes("Item | Details");

process.stdout.write(JSON.stringify({ afterTone, afterPreset, afterAr, afterHi, initialPresetPressed, leakedChildren, copyFocusRestored, copiedShown, copiedReset, emptyDisabled, presetRestored }));
"""
        proc = subprocess.run(["node", "-e", probe, tools_js], check=True, capture_output=True, text=True)
        res = json.loads(proc.stdout)
        self.assertEqual(res["afterTone"], "हाय")
        self.assertEqual(res["afterPreset"], "धन्यवाद")
        self.assertEqual(res["afterAr"], {"srcDir": "rtl", "srcLang": "ar", "outLang": "en", "focusKept": True})
        self.assertEqual(res["afterHi"], {"srcDir": "ltr", "outLang": "hi"})
        self.assertEqual(res["initialPresetPressed"], "false")
        self.assertEqual(res["leakedChildren"], 0)
        self.assertTrue(res["copyFocusRestored"])
        self.assertTrue(res["copiedShown"])
        self.assertTrue(res["copiedReset"])
        self.assertTrue(res["emptyDisabled"])
        self.assertTrue(res["presetRestored"])

    def test_tools_js_and_css_are_purely_local_and_safe(self):
        tools_js = os.path.join(TOOLS_DIR, "tools.js")
        self.assertTrue(os.path.isfile(tools_js), "Missing web/tools/tools.js")
        with open(tools_js, encoding="utf-8") as fh:
            js_text = fh.read()
        for forbidden in ("innerHTML", "outerHTML", "insertAdjacentHTML", "fetch(", "XMLHttpRequest", "sendBeacon", "localStorage", "sessionStorage"):
            self.assertNotIn(forbidden, js_text)
        with open(os.path.join(TOOLS_DIR, "site.css"), encoding="utf-8") as css_fh:
            css_text = css_fh.read()
        for selector in (".tool-card", ".tool-dock", ".tool-chip", ".tool-res"):
            self.assertIn(selector, css_text)
        self.assertIn("overflow-wrap: anywhere", css_text)


class WebMicroToolsTests(unittest.TestCase):
    def _assert_common_tool_contract(self, slug, html_text):
        self.assertIn(f'<link rel="canonical" href="https://smartype.in/{slug}">', html_text)
        self.assertIn(f'<meta property="og:url" content="https://smartype.in/{slug}">', html_text)
        self.assertIn("tools.js", html_text)
        self.assertRegex(
            html_text,
            re.compile(r'<div class="tool-res"[^>]*>.*?</div>\s*<div class="tool-dock">.*?play-chip.*?Get it on Google Play', re.DOTALL),
        )
        m = re.search(r'<script id="tool-data" type="application/json">(.*?)</script>', html_text, flags=re.DOTALL)
        self.assertIsNotNone(m, f"Missing #tool-data JSON on {slug}")
        payload = json.loads(m.group(1))
        for unshipped in ("friendly", "concise", "emoji search", "smartype pro"):
            self.assertNotIn(unshipped, html_text.lower())
        return payload

    def test_polite_whatsapp_rewriter_page(self):
        html_text = build.polite_whatsapp_rewriter()
        payload = self._assert_common_tool_contract("polite-whatsapp-rewriter", html_text)
        self.assertIn("Polite WhatsApp message rewriter", html_text)
        self.assertGreaterEqual(len(payload["presets"]), 4)
        for style_name in ("Polite", "Professional", "Empathetic", "Firm"):
            self.assertIn(style_name, html_text)

    def test_ai_tone_translator_multilanguage_page(self):
        html_text = build.ai_tone_translator()
        payload = self._assert_common_tool_contract("ai-tone-translator", html_text)
        self.assertIn("English-to-Hindi", html_text)
        group_labels = [g["label"] for g in payload["groups"]]
        for expected_pair in ("English → Hindi", "English → Spanish", "Arabic → English", "French → English"):
            self.assertTrue(
                any(expected_pair in label for label in group_labels),
                f"Missing {expected_pair} in {group_labels}",
            )
        arabic_group = next(g for g in payload["groups"] if "Arabic → English" in g["label"])
        self.assertEqual(arabic_group.get("dir"), "rtl")
        self.assertEqual(arabic_group.get("lang"), "ar")
        self.assertEqual(arabic_group.get("outLang"), "en")
        hindi_group = next(g for g in payload["groups"] if "English → Hindi" in g["label"])
        self.assertEqual(hindi_group.get("outLang"), "hi")
        self.assertIn('data-output lang="hi"', html_text)
        self.assertIn('role="group" aria-label="1. Choose a language pair"', html_text)
        self.assertIn("21", html_text)

    def test_rough_notes_to_neat_list_page(self):
        html_text = build.rough_notes_to_neat_list()
        payload = self._assert_common_tool_contract("rough-notes-to-neat-list", html_text)
        self.assertIn("Rough-notes-to-neat-list formatter", html_text)
        self.assertIn("<textarea", html_text)
        self.assertIn('maxlength="2000"', html_text)
        self.assertIn('role="group" aria-label="Output format"', html_text)
        mode_ids = [m["id"] for m in payload["modes"]]
        self.assertEqual(mode_ids, ["bullets", "numbered", "checklist", "table"])
        escaped = build.micro_tool_page("t.html", "T", "D", "K", "H", "L", "<div></div>", "S", "P", {"x": "</script>"})
        self.assertIn(r"<\/script>", escaped)


if __name__ == "__main__":
    unittest.main()
