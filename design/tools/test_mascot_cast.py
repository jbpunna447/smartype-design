import os
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "tools"))

from mascot_cast import (  # noqa: E402
    ACCESSORY_STYLES,
    BEARD_STYLES,
    CAST_PRESETS,
    EXPRESSIONS,
    GLASSES_STYLES,
    HAIR_STYLES,
    POSES,
    assert_parody_safe_text,
    render_mascot_svg,
)


def _parse_svg(svg_text: str) -> ET.Element:
    if 'xmlns="http://www.w3.org/2000/svg"' not in svg_text:
        svg_text = svg_text.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1)
    return ET.fromstring(svg_text)


class MascotCastTests(unittest.TestCase):
    def test_all_presets_and_slots_parse_as_valid_xml_without_emoji(self):
        self.assertEqual(len(CAST_PRESETS), 6)
        self.assertEqual(len(HAIR_STYLES), 8)
        self.assertEqual(len(BEARD_STYLES), 5)
        self.assertEqual(len(GLASSES_STYLES), 4)
        self.assertEqual(len(ACCESSORY_STYLES), 6)
        self.assertEqual(len(EXPRESSIONS), 6)
        self.assertEqual(len(POSES), 6)

        slugs = [entry[0] for entry in CAST_PRESETS]
        self.assertEqual(
            slugs,
            ["guy", "girl", "vip-podium", "statesman", "tech-founder", "spark-buddy"],
        )

        for slug, title, subtitle, spec, still_at in CAST_PRESETS:
            assert_parody_safe_text(title)
            assert_parody_safe_text(subtitle)
            svg = render_mascot_svg(200, preset=slug, uid=slug)
            _parse_svg(svg)
            self.assertIn("var(--ill-ink", svg)
            self.assertTrue(all(ord(ch) < 0x1F300 for ch in svg + title + subtitle))
            self.assertGreater(still_at, 0.0)
            self.assertIsInstance(spec, dict)

        for hair in HAIR_STYLES:
            hair_svg = render_mascot_svg(180, hair=hair, uid=f"h-{hair}")
            root = _parse_svg(hair_svg)
            if hair in ("classic-fade", "long-wave", "ponytail", "messy-curls", "spiky"):
                front_groups = [el for el in root.iter() if el.attrib.get("class") == "hair-front"]
                self.assertEqual(len(front_groups), 1, f"Missing hair-front group for {hair}")
                strokes = [el.attrib.get("stroke", "") for el in front_groups[0].iter() if "stroke" in el.attrib]
                self.assertTrue(strokes and all("var(--ill-ink" in st for st in strokes), f"Dark hair {hair} lacks var(--ill-ink) stroke: {strokes}")
        for beard in BEARD_STYLES:
            _parse_svg(render_mascot_svg(180, beard=beard, uid=f"b-{beard}"))
        for glasses in GLASSES_STYLES:
            _parse_svg(render_mascot_svg(180, glasses=glasses, uid=f"g-{glasses}"))
        for acc in ACCESSORY_STYLES:
            _parse_svg(render_mascot_svg(180, accessory=acc, uid=f"a-{acc}"))
        for expr in EXPRESSIONS:
            _parse_svg(render_mascot_svg(180, expression=expr, uid=f"e-{expr}"))
        for pose in POSES:
            _parse_svg(render_mascot_svg(180, pose=pose, uid=f"p-{pose}"))

    def test_unknown_slot_or_preset_raises_value_error(self):
        with self.assertRaises(ValueError):
            render_mascot_svg(180, preset="nonexistent")
        with self.assertRaises(ValueError):
            render_mascot_svg(180, hair="mohawk-invalid")

    def test_preset_allows_explicit_expression_or_pose_override(self):
        panic_svg = render_mascot_svg(180, preset="statesman", expression="panic", pose="facepalm", uid="st-panic")
        default_svg = render_mascot_svg(180, preset="statesman", uid="st-default")
        _parse_svg(panic_svg)
        self.assertNotEqual(panic_svg, default_svg)
        self.assertIn("#F2F6F8", panic_svg)  # preserves white-full-beard from statesman preset
        self.assertIn("ry=\"8.4\"", panic_svg)  # applies panic eye height override

    def test_parody_guard_rejects_blocked_name_digests_and_handles(self):
        for bad in (
            "Real Person",
            "@real_person",
            "Real   Person!",
            "#RealPerson",
            "R\u00e9al-Person",
            "@realperson",
            "#realperson",
            "#REALPerson",
            "rEaL pErSoN",
            "@rEaL_pErSoN",
            "#rEaLpErSoN",
            "Re\u200bal Person",
        ):
            with self.assertRaisesRegex(ValueError, "PARODY_REAL_NAME_FORBIDDEN"):
                assert_parody_safe_text(bad)
        self.assertEqual(assert_parody_safe_text("Statesman Key"), "Statesman Key")
        self.assertEqual(assert_parody_safe_text("VIP Podium Key"), "VIP Podium Key")
        self.assertEqual(assert_parody_safe_text("Tech Founder Key"), "Tech Founder Key")

    def test_cast_export_site_showcase_and_bundle_isolation(self):
        from build_illustrations import build_cast_illustrations  # noqa: WPS433

        cast_dir = build_cast_illustrations()
        self.assertEqual(cast_dir, os.path.join(ROOT, "assets", "illustrations-cast"))
        for slug, *_ in CAST_PRESETS:
            light_svg = os.path.join(cast_dir, "svg", f"{slug}.svg")
            dark_svg = os.path.join(cast_dir, "svg", f"{slug}-dark.svg")
            still_light = os.path.join(cast_dir, "still", f"{slug}.svg")
            still_dark = os.path.join(cast_dir, "still", f"{slug}-dark.svg")
            for path in (light_svg, dark_svg, still_light, still_dark):
                self.assertTrue(os.path.isfile(path), path)
                with open(path) as fh:
                    text = fh.read()
                ET.fromstring(text)
            with open(dark_svg) as fh:
                self.assertIn("--ill-ink:#E3EEF0", fh.read())
            with open(still_light) as fh:
                self.assertIn("animation-play-state: paused !important", fh.read())

        from build_site import zip_dir  # noqa: WPS433

        with tempfile.TemporaryDirectory() as tmp:
            fresh_zip = os.path.join(tmp, "smartype-illustrations.zip")
            zip_dir(os.path.join(ROOT, "assets", "illustrations"), fresh_zip, "smartype-illustrations", skip=("source",))
            for candidate_zip in (fresh_zip, os.path.join(ROOT, "site", "downloads", "smartype-illustrations.zip")):
                self.assertTrue(os.path.isfile(candidate_zip))
                with zipfile.ZipFile(candidate_zip) as zf:
                    names = zf.namelist()
                self.assertTrue(names)
                for slug, *_ in CAST_PRESETS:
                    self.assertFalse(any(slug in entry for entry in names), f"Unexpected cast slug {slug} in app zip")
                self.assertFalse(any("illustrations-cast" in entry for entry in names))

        for rel in ("illustrations.html", os.path.join("design-system", "illustrations.html")):
            page_path = os.path.join(ROOT, "site", rel)
            self.assertTrue(os.path.isfile(page_path), page_path)
            with open(page_path) as fh:
                html_text = fh.read()
            self.assertIn("Modular story wardrobe", html_text)
            self.assertNotIn("/Users/", html_text)
            self.assertNotIn("/Volumes/", html_text)
            self.assertTrue(all(ord(ch) < 0x1F300 for ch in html_text))
        for slug, *_ in CAST_PRESETS:
            self.assertTrue(os.path.isfile(os.path.join(ROOT, "site", "assets", "illustrations-cast", "svg", f"{slug}.svg")))
            self.assertTrue(os.path.isfile(os.path.join(ROOT, "site", "assets", "illustrations-cast", "still", f"{slug}-dark.svg")))


if __name__ == "__main__":
    unittest.main()
