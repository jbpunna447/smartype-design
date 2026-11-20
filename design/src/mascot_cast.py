"""Modular key mascot wardrobe and parody-safe character presets for story reels and social carousels."""
import hashlib
import re
import unicodedata

from brand_marks import INK
from illustration_concepts import _glow, _key, _shadow, _spark, _svg

MINT, SKY, CORAL, GOLD = "#4BDCA4", "#2AA8E0", "#E5484D", "#F5B82E"
OUTLINE = "var(--ill-ink, #08323B)"

HAIR_STYLES = ("none", "classic-fade", "long-wave", "ponytail", "swept-blonde", "silver-part", "messy-curls", "spiky")
BEARD_STYLES = ("none", "stubble", "trimmed-full", "white-full-beard", "mustache")
GLASSES_STYLES = ("none", "round-wire", "rimless", "thick-frame")
ACCESSORY_STYLES = ("none", "red-tie", "vest-collar", "hoodie-collar", "bow-ribbon", "podium-mic")
EXPRESSIONS = ("watching", "smitten", "panic", "angry", "cool", "relieved")
POSES = ("typing-phone", "facepalm", "cool-shades", "podium-speaks", "angry-texting", "cheer-jump")

BLOCKED_PARODY_NAME_DIGESTS = frozenset((
    "023b4b99fe7c4662", "023cdfbd6d487283", "06375675f6be9ef0", "091db186b8ad81c4",
    "1ba7576a58d4333f", "1e4e7e04d8fe6740", "1e95336302ae4544", "1eb31ae51a031ae4",
    "1ff7c189a1459ba6", "2553478f3bfe4ec7", "26912c2adf28c35f", "29bf37371c00253f",
    "2c17b65538784135", "3a7539f9b871851f", "417a58158044313e", "48e6c22983e0446f",
    "4a2359208cad3204", "4d3b84af7f12a99e", "529713cc946ab793", "5f51caed6b5daa0d",
    "64c49cf68381a6d1", "6572e145f74f60a3", "6a5f7bd039b36563", "6b1f00bb01901236",
    "6ca8d923f852a125", "6ffb2274a08e7e7f", "757339960f4bf033", "75cce1ad1e5bb601",
    "7a15ae4bbdc306ad", "7beef813b2a01a4c", "7ee9cc85af5a4e95", "811075a7e2d1de8c",
    "84eb1209b0e645e5", "87174d48b9d90020", "87a49b8f3a3603bc", "8df5fde4a35a53f5",
    "9120182607b47e8e", "91a2b8dc3112e020", "97cf278a1bec0276", "9c7166cfa757292b",
    "9d715fe30ec1ef0e", "9ecdcfa67672ec75", "a50a780aec9cb016", "b1b3c4ca7e997ed9",
    "b99a49ddf1a1daf7", "ba763d9a637902af", "c399f26dca8f3ef9", "c5e0cc9cda15ddf1",
    "c6418c400acb5831", "c69756c2c4be0ac9", "c946a730a4c23499", "cc42016400dfbadb",
    "d2bca14e6866283f", "d4ffdc72e95cc47f", "d9265643b077ac67", "db4449aa9e495b31",
    "e109668d4ea8b8cd", "e75c156c34c534a0", "ee6582fdbb0d0b37", "f0d6fcf84c321cfd",
    "f3d045c8559cb6e1", "f6bfb1a53e327f4f", "fadd627dec06fd95", "ffc5e83b0ebab726",
))

CAST_PRESETS = (
    ("guy", "Everyday Guy Key", "Casual Fade & Hoodie",
     {"body": "key", "hair": "classic-fade", "beard": "stubble", "glasses": "none", "accessory": "hoodie-collar", "expression": "smitten", "pose": "typing-phone"}, 0.9),
    ("girl", "Everyday Girl Key", "Long Wave & Ribbon",
     {"body": "key", "hair": "long-wave", "beard": "none", "glasses": "none", "accessory": "bow-ribbon", "expression": "watching", "pose": "typing-phone"}, 1.1),
    ("vip-podium", "VIP Podium Key", "Swept Blonde & Red Tie",
     {"body": "key", "hair": "swept-blonde", "beard": "none", "glasses": "none", "accessory": "red-tie", "expression": "panic", "pose": "podium-speaks"}, 0.7),
    ("statesman", "Statesman Key", "Silver Part & Full Beard",
     {"body": "key", "hair": "silver-part", "beard": "white-full-beard", "glasses": "rimless", "accessory": "vest-collar", "expression": "relieved", "pose": "cool-shades"}, 1.0),
    ("tech-founder", "Tech Founder Key", "Tousled Curls & Thick Frames",
     {"body": "key", "hair": "messy-curls", "beard": "trimmed-full", "glasses": "thick-frame", "accessory": "hoodie-collar", "expression": "cool", "pose": "cool-shades"}, 0.8),
    ("spark-buddy", "Spark Sidekick", "AI Helper Companion",
     {"body": "spark", "hair": "none", "beard": "none", "glasses": "none", "accessory": "none", "expression": "relieved", "pose": "cheer-jump"}, 0.6),
)
_PRESET_MAP = {slug: (title, spec, still_at) for slug, title, _sub, spec, still_at in CAST_PRESETS}


def _digest_phrase(phrase: str) -> str:
    return hashlib.sha256(f"smartype-parody-guard-v1:{phrase}".encode("utf-8")).hexdigest()[:16]


def assert_parody_safe_text(text: str) -> str:
    folded = unicodedata.normalize("NFKD", str(text))
    ascii_text = "".join(
        ch for ch in folded if not unicodedata.combining(ch) and unicodedata.category(ch) != "Cf"
    )
    raw_words = [w for w in re.sub(r"[^a-zA-Z0-9]+", " ", ascii_text).lower().split() if w]
    spaced = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1 \2", ascii_text)
    spaced = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", spaced)
    camel_words = [w for w in re.sub(r"[^a-zA-Z0-9]+", " ", spaced).lower().split() if w]
    for words in (raw_words, camel_words):
        for i, word in enumerate(words):
            if _digest_phrase(word) in BLOCKED_PARODY_NAME_DIGESTS:
                raise ValueError("PARODY_REAL_NAME_FORBIDDEN")
            if i + 1 < len(words) and (
                _digest_phrase(f"{word} {words[i + 1]}") in BLOCKED_PARODY_NAME_DIGESTS
                or _digest_phrase(f"{word}{words[i + 1]}") in BLOCKED_PARODY_NAME_DIGESTS
            ):
                raise ValueError("PARODY_REAL_NAME_FORBIDDEN")
    return text


def _face(expr: str) -> str:
    ex1, ex2, ey = 88.5, 111.5, 90.0
    parts = []
    if expr in ("smitten", "relieved"):
        parts.append("".join(f'<path d="M{ex - 5.5:.1f} {ey + 1.5:.1f} q5.5 -8.5 11 0" fill="none" stroke="{INK}" stroke-width="3.2" stroke-linecap="round"/>' for ex in (ex1, ex2)))
    else:
        ry = 4.2 if expr in ("angry", "cool") else (8.4 if expr == "panic" else 7.0)
        rx = 6.2 if expr == "panic" else 5.2
        parts.append('<g class="blink">' + "".join(
            f'<ellipse cx="{ex:.1f}" cy="{ey:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{INK}"/>'
            f'<circle cx="{ex + 1.8:.1f}" cy="{ey - 2.0:.1f}" r="1.9" fill="#FFFFFF"/>' for ex in (ex1, ex2)) + "</g>")
    if expr == "angry":
        parts.append(f'<path d="M82 79 l13 4 M118 79 l-13 4" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>')
    elif expr == "panic":
        parts.append(f'<path d="M82 77 q6 -5 13 0 M105 77 q6 -5 13 0" fill="none" stroke="{INK}" stroke-width="2.8" stroke-linecap="round"/>'
                     f'<path d="M129 77 c3 5 4 9 0 11 c-4 -2 -3 -6 0 -11Z" fill="{SKY}"/>')
    if expr == "panic":
        parts.append(f'<ellipse cx="100" cy="109" rx="4.8" ry="6.2" fill="{INK}"/>')
    elif expr == "angry":
        parts.append(f'<path d="M92 111 q8 -6 16 0" fill="none" stroke="{INK}" stroke-width="3.4" stroke-linecap="round"/>')
    else:
        w = 19 if expr in ("smitten", "relieved") else 14
        parts.append(f'<path d="M{100 - w / 2:.1f} 106 q{w / 2:.1f} 10 {w:.1f} 0" fill="none" stroke="{INK}" stroke-width="3.4" stroke-linecap="round"/>')
    cheeks = CORAL if expr in ("smitten", "angry") else MINT
    parts.append("".join(f'<ellipse cx="{cx}" cy="103" rx="5.2" ry="3" fill="{cheeks}" opacity=".42"/>' for cx in (77, 123)))
    return "".join(parts)


def _hair_back(hair: str) -> str:
    if hair == "long-wave":
        return (f'<path d="M58 68 C47 84 48 112 58 124 C63 118 64 96 64 74 Z" fill="#3B233A" stroke="{OUTLINE}" stroke-width="2.4"/>'
                f'<path d="M142 68 C153 84 152 112 142 124 C137 118 136 96 136 74 Z" fill="#3B233A" stroke="{OUTLINE}" stroke-width="2.4"/>')
    if hair == "ponytail":
        return (f'<path d="M134 62 C154 56 162 76 151 95 C143 92 141 78 134 71 Z" fill="#2A1F33" stroke="{OUTLINE}" stroke-width="2.4"/>'
                f'<circle cx="136" cy="66" r="4.5" fill="{MINT}" stroke="{INK}" stroke-width="1.8"/>')
    return ""


def _hair_front(hair: str) -> str:
    if hair == "classic-fade":
        return f'<g class="hair-front"><path d="M64 68 C64 49 136 49 136 68 C122 59 84 59 64 68 Z" fill="#163844" stroke="{OUTLINE}" stroke-width="2.4"/></g>'
    if hair in ("long-wave", "ponytail"):
        fill = "#3B233A" if hair == "long-wave" else "#2A1F33"
        return f'<g class="hair-front"><path d="M63 70 C65 47 135 47 137 70 C118 57 86 58 63 70 Z" fill="{fill}" stroke="{OUTLINE}" stroke-width="2.4"/></g>'
    if hair == "swept-blonde":
        return (f'<g class="hair-front"><path d="M61 68 C60 44 108 35 144 52 C136 62 122 65 98 63 C82 62 71 65 61 68 Z" fill="{GOLD}" stroke="{INK}" stroke-width="2.6"/>'
                f'<path d="M74 55 C94 46 118 47 133 53" fill="none" stroke="#D18F15" stroke-width="2.4" stroke-linecap="round"/></g>')
    if hair == "silver-part":
        return (f'<g class="hair-front"><path d="M63 68 C64 47 136 47 137 68 C119 58 84 58 63 68 Z" fill="#E6EEF2" stroke="{INK}" stroke-width="2.4"/>'
                f'<path d="M82 54 L88 62" stroke="#9BB0BA" stroke-width="2.2" stroke-linecap="round"/></g>')
    if hair == "messy-curls":
        puffs = "".join(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#1E2F3C" stroke="{OUTLINE}" stroke-width="2.2"/>'
                        for cx, cy, r in ((74, 59, 9), (87, 54, 10), (101, 53, 10.5), (115, 55, 10), (127, 60, 8.5)))
        return f'<g class="hair-front">{puffs}</g>'
    if hair == "spiky":
        return f'<g class="hair-front"><path d="M65 67 L76 46 L89 58 L101 42 L113 58 L126 47 L135 67 Q100 59 65 67 Z" fill="#123944" stroke="{OUTLINE}" stroke-width="2.4"/></g>'
    return ""


def _beard(beard: str) -> str:
    if beard == "stubble":
        return f'<path d="M70 112 C72 131 128 131 130 112 C122 124 78 124 70 112 Z" fill="{INK}" opacity=".16"/>'
    if beard == "trimmed-full":
        return f'<path d="M67 107 C67 134 133 134 133 107 L125 107 C121 121 79 121 75 107 Z" fill="#1E2F3C" stroke="{INK}" stroke-width="2"/>'
    if beard == "white-full-beard":
        return (f'<path d="M66 105 C64 139 136 139 134 105 L123 105 C118 119 82 119 77 105 Z" fill="#F2F6F8" stroke="{INK}" stroke-width="2.3"/>'
                f'<path d="M86 103 Q100 97 114 103" fill="none" stroke="{INK}" stroke-width="2.4" stroke-linecap="round"/>')
    if beard == "mustache":
        return f'<path d="M84 102 C91 96 98 99 100 102 C102 99 109 96 116 102" fill="none" stroke="{INK}" stroke-width="3.6" stroke-linecap="round"/>'
    return ""


def _glasses(glasses: str, cool: bool) -> str:
    if glasses == "round-wire":
        return (f'<circle cx="88.5" cy="90" r="10" fill="none" stroke="{INK}" stroke-width="2.2"/>'
                f'<circle cx="111.5" cy="90" r="10" fill="none" stroke="{INK}" stroke-width="2.2"/>'
                f'<path d="M98.5 90 h3" stroke="{INK}" stroke-width="2.2"/>')
    if glasses == "rimless":
        return (f'<rect x="77.5" y="83" width="21" height="13" rx="4" fill="{SKY}" fill-opacity=".14" stroke="{INK}" stroke-width="1.5"/>'
                f'<rect x="101.5" y="83" width="21" height="13" rx="4" fill="{SKY}" fill-opacity=".14" stroke="{INK}" stroke-width="1.5"/>'
                f'<path d="M98.5 89 h3 M72 88 h5.5 M122.5 88 h5.5" stroke="{INK}" stroke-width="1.8" stroke-linecap="round"/>')
    if glasses == "thick-frame":
        lens = INK if cool else "#FFFFFF"
        op = ".88" if cool else ".18"
        return (f'<rect x="76.5" y="81.5" width="22" height="16" rx="4.5" fill="{lens}" fill-opacity="{op}" stroke="{INK}" stroke-width="3.2"/>'
                f'<rect x="101.5" y="81.5" width="22" height="16" rx="4.5" fill="{lens}" fill-opacity="{op}" stroke="{INK}" stroke-width="3.2"/>'
                f'<path d="M98.5 88.5 h3" stroke="{INK}" stroke-width="3.2"/>')
    return ""


def _accessory(acc: str) -> str:
    if acc == "red-tie":
        return (f'<path d="M86 135 L100 142 L114 135" fill="#FFFFFF" stroke="{INK}" stroke-width="2"/>'
                f'<path d="M97 137 L103 137 L105 154 L100 160 L95 154 Z" fill="{CORAL}" stroke="{INK}" stroke-width="1.8"/>')
    if acc == "vest-collar":
        return (f'<rect x="76" y="128" width="48" height="12" rx="5" fill="#D9822B" stroke="{INK}" stroke-width="2"/>'
                f'<circle cx="100" cy="134" r="1.8" fill="#FFFFFF"/>')
    if acc == "hoodie-collar":
        return (f'<path d="M74 133 Q100 145 126 133" fill="none" stroke="{ SKY }" stroke-width="6" stroke-linecap="round"/>'
                f'<path d="M92 138 v12 M108 138 v12" stroke="{OUTLINE}" stroke-width="2.4" stroke-linecap="round"/>')
    if acc == "bow-ribbon":
        return (f'<path d="M68 58 L57 51 L59 64 Z M68 58 L79 51 L77 64 Z" fill="{MINT}" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
                f'<circle cx="68" cy="58" r="3.4" fill="{SKY}" stroke="{INK}" stroke-width="1.8"/>')
    if acc == "podium-mic":
        return (f'<path d="M148 164 C148 138 140 124 128 118" fill="none" stroke="{OUTLINE}" stroke-width="3.2" stroke-linecap="round"/>'
                f'<ellipse cx="125" cy="116" rx="5.5" ry="4" fill="{INK}" stroke="{OUTLINE}" stroke-width="1.8"/>')
    return ""


def _phone(x: float, y: float, rot: float, alert: bool = False) -> str:
    bar = CORAL if alert else MINT
    return (f'<g transform="rotate({rot} {x} {y})">'
            f'<rect x="{x - 12}" y="{y - 19}" width="24" height="38" rx="5.5" fill="#0D1114" stroke="{OUTLINE}" stroke-width="2.2"/>'
            f'<rect x="{x - 9}" y="{y - 14}" width="18" height="28" rx="3" fill="#F7F9FA"/>'
            f'<rect x="{x - 6.5}" y="{y - 9}" width="13" height="4" rx="2" fill="{SKY}"/>'
            f'<rect x="{x - 6.5}" y="{y - 2}" width="10" height="4" rx="2" fill="{bar}"/></g>')


def _limbs_and_props(pose: str) -> tuple[str, str]:
    legs = (f'<path d="M86 139 Q83 154 85 166 M114 139 Q117 154 115 166" fill="none" stroke="{OUTLINE}" stroke-width="5" stroke-linecap="round"/>'
            f'<ellipse cx="81" cy="168" rx="8.5" ry="4.5" fill="{OUTLINE}"/><ellipse cx="119" cy="168" rx="8.5" ry="4.5" fill="{OUTLINE}"/>')
    if pose == "cheer-jump":
        legs = (f'<path d="M86 138 Q77 150 72 158 M114 138 Q123 150 128 158" fill="none" stroke="{OUTLINE}" stroke-width="5" stroke-linecap="round"/>'
                f'<ellipse cx="69" cy="160" rx="8" ry="4.2" fill="{OUTLINE}"/><ellipse cx="131" cy="160" rx="8" ry="4.2" fill="{OUTLINE}"/>')
        front = (f'<path d="M63 96 Q44 74 50 54 M137 96 Q156 74 150 54" fill="none" stroke="{OUTLINE}" stroke-width="5" stroke-linecap="round"/>'
                 f'<circle cx="50" cy="52" r="5.8" fill="{OUTLINE}"/><circle cx="150" cy="52" r="5.8" fill="{OUTLINE}"/>')
        return legs, front
    if pose == "facepalm":
        front = (f'<path d="M63 102 Q46 118 58 132" fill="none" stroke="{OUTLINE}" stroke-width="5" stroke-linecap="round"/>'
                 + _phone(62, 134, -14, alert=True)
                 + f'<path d="M137 100 Q156 82 106 83" fill="none" stroke="{OUTLINE}" stroke-width="5" stroke-linecap="round"/>'
                 f'<ellipse cx="102" cy="84" rx="8" ry="6" fill="{OUTLINE}"/>')
        return legs, front
    if pose == "podium-speaks":
        front = (f'<path d="M63 104 Q48 118 66 128 M137 98 Q158 84 154 66" fill="none" stroke="{OUTLINE}" stroke-width="5" stroke-linecap="round"/>'
                 f'<circle cx="67" cy="128" r="5.6" fill="{OUTLINE}"/><circle cx="154" cy="64" r="5.8" fill="{OUTLINE}"/>')
        return legs, front
    if pose == "cool-shades":
        front = (f'<path d="M63 102 Q45 116 62 126 M137 100 Q156 92 156 78" fill="none" stroke="{OUTLINE}" stroke-width="5" stroke-linecap="round"/>'
                 f'<circle cx="156" cy="76" r="5.8" fill="{OUTLINE}"/>' + _phone(66, 126, -10))
        return legs, front
    alert = pose == "angry-texting"
    sparks = f'<path d="M88 38 l5 8 l-7 3 l6 7 M114 38 l-5 8 l7 3 l-6 7" fill="none" stroke="{CORAL}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>' if alert else ""
    front = (f'<path d="M63 102 Q48 122 84 126 M137 102 Q152 122 116 126" fill="none" stroke="{OUTLINE}" stroke-width="5" stroke-linecap="round"/>'
             + _phone(100, 127, -6 if not alert else 5, alert=alert)
             + f'<circle cx="84" cy="127" r="5.4" fill="{OUTLINE}"/><circle cx="116" cy="127" r="5.4" fill="{OUTLINE}"/>' + sparks)
    return legs, front


def render_mascot_svg(
    dp: int = 200,
    *,
    preset: str | None = None,
    body: str | None = None,
    hair: str | None = None,
    beard: str | None = None,
    glasses: str | None = None,
    accessory: str | None = None,
    expression: str | None = None,
    pose: str | None = None,
    uid: str = "mc0",
) -> str:
    still_at = 0.9
    label = "SmarType mascot character"
    spec = {}
    if preset is not None:
        if preset not in _PRESET_MAP:
            raise ValueError(f"Unknown mascot preset: {preset}")
        label, spec, still_at = _PRESET_MAP[preset]

    body = body or spec.get("body", "key")
    hair = hair or spec.get("hair", "none")
    beard = beard or spec.get("beard", "none")
    glasses = glasses or spec.get("glasses", "none")
    accessory = accessory or spec.get("accessory", "none")
    expression = expression or spec.get("expression", "watching")
    pose = pose or spec.get("pose", "typing-phone")

    if body not in ("key", "spark"):
        raise ValueError(f"Unknown body: {body}")
    if hair not in HAIR_STYLES:
        raise ValueError(f"Unknown hair: {hair}")
    if beard not in BEARD_STYLES:
        raise ValueError(f"Unknown beard: {beard}")
    if glasses not in GLASSES_STYLES:
        raise ValueError(f"Unknown glasses: {glasses}")
    if accessory not in ACCESSORY_STYLES:
        raise ValueError(f"Unknown accessory: {accessory}")
    if expression not in EXPRESSIONS:
        raise ValueError(f"Unknown expression: {expression}")
    if pose not in POSES:
        raise ValueError(f"Unknown pose: {pose}")

    assert_parody_safe_text(label)
    anim_id = re.sub(r"[^a-zA-Z0-9_]", "_", uid)
    amp = 10 if pose == "cheer-jump" else (2 if pose == "angry-texting" else 4)
    dur = "0.45s" if pose == "angry-texting" else ("1.8s" if pose == "cheer-jump" else "2.8s")
    css = (
        f"@keyframes {anim_id}_blink {{ 0%,92%,100% {{ transform: scaleY(1); }} 95% {{ transform: scaleY(.1); }} }}"
        f" .{uid} .blink {{ animation: {anim_id}_blink 4s infinite; }}"
        f" @keyframes {anim_id}_rig {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-{amp}px); }} }}"
        f" .{uid} .rig {{ animation: {anim_id}_rig {dur} ease-in-out infinite; }}"
    )

    if body == "spark":
        content = (
            _shadow(100, 172, 34, 6.5, f"{anim_id}sh")
            + '<g class="rig">'
            + f'<path d="M92 118 Q85 142 80 154 M108 118 Q115 142 120 154" fill="none" stroke="{OUTLINE}" stroke-width="4.4" stroke-linecap="round"/>'
            + f'<ellipse cx="77" cy="156" rx="7.2" ry="3.8" fill="{OUTLINE}"/><ellipse cx="123" cy="156" rx="7.2" ry="3.8" fill="{OUTLINE}"/>'
            + f'<path d="M82 102 Q58 88 62 68 M118 102 Q142 88 138 68" fill="none" stroke="{OUTLINE}" stroke-width="4.4" stroke-linecap="round"/>'
            + f'<circle cx="62" cy="66" r="5" fill="{OUTLINE}"/><circle cx="138" cy="66" r="5" fill="{OUTLINE}"/>'
            + f'<g transform="translate(107.75 100)">{_spark(anim_id + "sp", 124)}</g>'
            + '<circle cx="95.2" cy="98" r="3.4" fill="#FFFFFF"/><circle cx="104.8" cy="98" r="3.4" fill="#FFFFFF"/>'
            + f'<g class="blink"><circle cx="95.2" cy="98" r="2.2" fill="{INK}"/><circle cx="104.8" cy="98" r="2.2" fill="{INK}"/></g>'
            + f'<path d="M96.8 104 q3.2 3.4 6.4 0" fill="none" stroke="#FFFFFF" stroke-width="2.4" stroke-linecap="round"/>'
            + "</g>"
        )
        return _svg(uid, css, _glow(100, 100, 84, f"{anim_id}gl", .30) + content, dp, label, still_at)

    legs, front_arms = _limbs_and_props(pose)
    rig = (
        _hair_back(hair)
        + legs
        + _key(62, 60, 76, f"{anim_id}k")
        + _face(expression)
        + _beard(beard)
        + _glasses(glasses, expression == "cool" or pose == "cool-shades")
        + _hair_front(hair)
        + _accessory(accessory)
        + front_arms
    )
    body_svg = _glow(100, 102, 86, f"{anim_id}gl", .28) + _shadow(100, 174, 42, 7.5, f"{anim_id}sh") + f'<g class="rig">{rig}</g>'
    return _svg(uid, css, body_svg, dp, label, still_at)
