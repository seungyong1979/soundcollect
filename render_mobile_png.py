from PIL import Image, ImageDraw, ImageFont
import math, os

# ── 색상 ──────────────────────────────────────────────
GREEN_DEEP  = (26,  77, 62)
GREEN_MID   = (45, 107, 88)
GREEN_LIGHT = (58, 130, 106)
GOLD        = (200, 169, 106)
GOLD_LT     = (226, 201, 138)
BEIGE       = (237, 227, 216)
BEIGE_DIM   = (200, 185, 168)
WHITE       = (255, 255, 255)

W, H = 1080, 1920

# ── 폰트 경로 ────────────────────────────────────────
FONT_KO_R  = "/usr/share/fonts/truetype/nanum/NanumSquareR.ttf"
FONT_KO_B  = "/usr/share/fonts/truetype/nanum/NanumSquareB.ttf"
FONT_KO_EB = "/usr/share/fonts/truetype/nanum/NanumSquareEB.ttf"
FONT_KO_L  = "/usr/share/fonts/truetype/nanum/NanumSquareL.ttf"
FONT_MJ    = "/usr/share/fonts/truetype/nanum/NanumMyeongjo.ttf"
FONT_MJ_B  = "/usr/share/fonts/truetype/nanum/NanumMyeongjoBold.ttf"

def fnt(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def load_img(path, size):
    img = Image.open(path).convert("RGBA")
    img = img.resize(size, Image.LANCZOS)
    return img

def circle_mask(size):
    mask = Image.new("L", size, 0)
    d = ImageDraw.Draw(mask)
    d.ellipse([0, 0, size[0]-1, size[1]-1], fill=255)
    return mask

def round_rect_mask(size, r):
    mask = Image.new("L", size, 0)
    d = ImageDraw.Draw(mask)
    d.rounded_rectangle([0, 0, size[0]-1, size[1]-1], radius=r, fill=255)
    return mask

# ── 캔버스 ────────────────────────────────────────────
img = Image.new("RGB", (W, H), GREEN_DEEP)
draw = ImageDraw.Draw(img, "RGBA")

# ── 배경 그라디언트 효과 (세로 미묘한 변화) ──────────
for y in range(H):
    ratio = y / H
    r = int(GREEN_DEEP[0] + (38 - GREEN_DEEP[0]) * ratio * 0.4)
    g = int(GREEN_DEEP[1] + (95 - GREEN_DEEP[1]) * ratio * 0.3)
    b = int(GREEN_DEEP[2] + (80 - GREEN_DEEP[2]) * ratio * 0.3)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

draw = ImageDraw.Draw(img, "RGBA")

# ── 배경 원형 장식 (반투명 골드) ──────────────────────
def draw_circle_overlay(cx, cy, r, alpha=13):
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(*GOLD, alpha))
    base = img.convert("RGBA")
    merged = Image.alpha_composite(base, overlay)
    img.paste(merged.convert("RGB"))

draw_circle_overlay(W + 100, -100, 380, 15)
draw_circle_overlay(-60, H + 80, 260, 10)
draw_circle_overlay(W - 60, H - 300, 160, 8)
draw_circle_overlay(W // 2, H // 2, 500, 4)

draw = ImageDraw.Draw(img, "RGBA")

# ── 단청 장식 바 ──────────────────────────────────────
def draw_dbar(y_top, bar_h=16):
    colors = [GOLD, GREEN_MID, BEIGE, GREEN_MID, GOLD_LT, GREEN_LIGHT]
    seg = 18
    x = 0
    ci = 0
    while x < W:
        c = colors[ci % len(colors)]
        draw.rectangle([x, y_top, x + seg - 1, y_top + bar_h - 1], fill=(*c, 220))
        x += seg
        ci += 1

draw_dbar(0)
draw_dbar(H - 16)

# ── CD 커버 이미지 ────────────────────────────────────
COVER_X, COVER_Y = 80, 48
COVER_S = 196
cover = load_img("seonamsa/images/cd_cover.jpg", (COVER_S, COVER_S))
cover_mask = round_rect_mask((COVER_S, COVER_S), 14)
cover.putalpha(cover_mask)
img.paste(cover, (COVER_X, COVER_Y), cover)

# CD 디스크 오버랩
DISC_S = 118
DISC_X = COVER_X + COVER_S - DISC_S + 14
DISC_Y = COVER_Y + COVER_S - DISC_S + 14
disc = load_img("seonamsa/images/cd_disc.png", (DISC_S, DISC_S))
disc_mask = circle_mask((DISC_S, DISC_S))
disc.putalpha(disc_mask)
img.paste(disc, (DISC_X, DISC_Y), disc)

# ── 타이틀 ────────────────────────────────────────────
TX = COVER_X + COVER_S + 36
f_main = fnt(FONT_MJ_B, 80)
draw.text((TX, 54), "SEONAMSA", font=f_main, fill=BEIGE)
f_sub = fnt(FONT_KO_L, 22)
draw.text((TX, 148), "TEMPLE  SOUNDSCAPE", font=f_sub, fill=GOLD_LT)
f_ko_sm = fnt(FONT_MJ, 23)
draw.text((TX, 180), "선암사 사운드스케이프", font=f_ko_sm, fill=(*BEIGE_DIM, 190))

# ── NFC 마크 (우상단) ─────────────────────────────────
NFC_CX, NFC_CY = W - 88, 100
NFC_R = 44
draw.ellipse([NFC_CX - NFC_R, NFC_CY - NFC_R, NFC_CX + NFC_R, NFC_CY + NFC_R],
             outline=GOLD, width=3)

def draw_nfc_waves_v2(cx, cy, col, aw=3):
    # 아래 점
    draw.ellipse([cx - 4, cy + 8, cx + 4, cy + 16], fill=col)
    # 3단 웨이브 (위쪽으로 퍼지는 아치)
    for i, (rr, lw) in enumerate([(12, aw), (20, aw - 1), (28, aw - 1)]):
        y0 = cy - rr + 4
        draw.arc([cx - rr, y0, cx + rr, y0 + rr * 2 - 8],
                 start=220, end=320, fill=col, width=lw)

draw_nfc_waves_v2(NFC_CX, NFC_CY - 8, GOLD)
f_nfc = fnt(FONT_KO_B, 18)
draw.text((NFC_CX, NFC_CY + NFC_R + 10), "NFC",
          font=f_nfc, fill=GOLD_LT, anchor="mm")

# ── 구분선 "사용법 / How to Use" ──────────────────────
SEC_Y = 296
f_sec_ko = fnt(FONT_KO_EB, 32)
f_sec_en = fnt(FONT_KO_L, 22)
draw.text((80, SEC_Y), "사용법", font=f_sec_ko, fill=GOLD_LT)
sec_ko_w = int(draw.textlength("사용법", font=f_sec_ko))
draw.text((80 + sec_ko_w + 24, SEC_Y + 4), "How to Use",
          font=f_sec_en, fill=(*GOLD_LT, 160))
sec_en_w = int(draw.textlength("How to Use", font=f_sec_en))
LINE_SX = 80 + sec_ko_w + 24 + sec_en_w + 24
draw.line([(LINE_SX, SEC_Y + 19), (W - 80, SEC_Y + 19)],
          fill=(*GOLD, 90), width=1)

# ════════════════════════════════════════════════════
# ── 아이콘 그리기 함수들 ──────────────────────────────
# ════════════════════════════════════════════════════

def draw_icon_nfc(cx, cy, size, col):
    """STEP1: 스마트폰 NFC 켜기 — 폰 + NFC 파장"""
    s = size
    # 스마트폰 외곽
    pw, ph = int(s * 0.36), int(s * 0.58)
    px, py = cx - pw // 2, cy - ph // 2
    draw.rounded_rectangle([px, py, px + pw, py + ph],
                            radius=6, outline=col, width=3)
    # 화면 영역
    draw.rounded_rectangle([px + 5, py + 10, px + pw - 5, py + ph - 18],
                            radius=3, outline=(*col, 160), width=1)
    # 홈버튼
    draw.ellipse([cx - 5, py + ph - 14, cx + 5, py + ph - 4],
                 outline=col, width=2)
    # NFC 웨이브 (폰 오른쪽 옆)
    wx = px + pw + 12
    for ri, rr in enumerate([10, 18, 26]):
        alpha_val = 255 - ri * 50
        draw.arc([wx, cy - rr, wx + rr * 2, cy + rr],
                 start=150, end=210, fill=(*col, alpha_val), width=3)


def draw_icon_tap(cx, cy, size, col):
    """STEP2: 폰을 키링 뒤에 가까이 — 폰↓ + 키링태그"""
    s = size
    # 키링 (아래 타원)
    tag_rx, tag_ry = int(s * 0.26), int(s * 0.13)
    tag_cy = cy + int(s * 0.20)
    draw.ellipse([cx - tag_rx, tag_cy - tag_ry, cx + tag_rx, tag_cy + tag_ry],
                 outline=col, width=3)
    draw.ellipse([cx - tag_rx + 6, tag_cy - tag_ry + 4,
                  cx + tag_rx - 6, tag_cy + tag_ry - 4],
                 outline=(*col, 120), width=1)
    # 고리
    draw.arc([cx - 10, tag_cy - tag_ry - 18, cx + 10, tag_cy - tag_ry + 2],
             start=0, end=180, fill=col, width=3)
    # 폰 (위)
    pw, ph = int(s * 0.28), int(s * 0.42)
    px, py = cx - pw // 2, cy - int(s * 0.34)
    draw.rounded_rectangle([px, py, px + pw, py + ph],
                            radius=5, outline=col, width=3)
    # 화면 내 NFC 심볼
    for rr in [6, 11]:
        draw.arc([cx - rr, py + 12 - rr, cx + rr, py + 12 + rr],
                 start=200, end=340, fill=(*col, 180), width=2)
    # 화살표 (폰→태그 방향)
    arr_y = py + ph + 4
    draw.line([(cx, arr_y), (cx, tag_cy - tag_ry - 22)],
              fill=(*col, 200), width=2)
    draw.polygon([(cx, tag_cy - tag_ry - 18),
                  (cx - 5, arr_y + 10),
                  (cx + 5, arr_y + 10)], fill=(*col, 200))


def draw_icon_link(cx, cy, size, col):
    """STEP3: 링크 탭 — 손가락 탭 + 링크 아이콘"""
    s = size
    # 체인 링크 (좌상단)
    lx, ly = cx - int(s * 0.18), cy - int(s * 0.20)
    lr, lh = int(s * 0.16), int(s * 0.09)
    # 왼쪽 링크 고리
    draw.rounded_rectangle([lx - lr, ly - lh, lx + lr, ly + lh],
                            radius=lh, outline=col, width=3)
    # 오른쪽 링크 고리
    draw.rounded_rectangle([lx + int(s * 0.06) - lr, ly - lh + int(s * 0.14),
                             lx + int(s * 0.06) + lr, ly + lh + int(s * 0.14)],
                            radius=lh, outline=col, width=3)
    # 손가락 (아래 오른쪽)
    fx, fy = cx + int(s * 0.04), cy + int(s * 0.06)
    # 손가락 원 (터치 포인트)
    draw.ellipse([fx - 16, fy - 16, fx + 16, fy + 16],
                 outline=col, width=3)
    draw.ellipse([fx - 8, fy - 8, fx + 8, fy + 8],
                 fill=(*col, 180))
    # 파장 (탭 효과)
    for rr in [22, 32]:
        draw.arc([fx - rr, fy - rr, fx + rr, fy + rr],
                 start=0, end=360, fill=(*col, 60), width=1)


def draw_icon_ear(cx, cy, size, col):
    """STEP4: 귀 + 음파"""
    s = size
    # 귀 외곽 (타원형 귀 실루엣)
    ew, eh = int(s * 0.32), int(s * 0.46)
    ex, ey = cx - int(s * 0.08) - ew // 2, cy - eh // 2

    # 귀 외형 (아치 형태)
    draw.arc([ex, ey, ex + ew, ey + eh],
             start=270, end=180, fill=col, width=4)
    # 귀 안쪽 곡선
    iw, ih = int(ew * 0.55), int(eh * 0.6)
    ix = ex + ew - iw - 4
    iy = ey + (eh - ih) // 2 + 4
    draw.arc([ix, iy, ix + iw, iy + ih],
             start=280, end=160, fill=(*col, 200), width=3)
    # 귓볼 (아래 돌출부)
    lobe_cx = ex + ew // 2 + 4
    lobe_cy = ey + eh - 2
    draw.arc([lobe_cx - 10, lobe_cy - 10, lobe_cx + 14, lobe_cy + 12],
             start=180, end=360, fill=col, width=3)
    # 귀 아랫부분 연결선
    draw.line([(ex + 6, ey + eh - 10), (lobe_cx - 10, lobe_cy + 2)],
              fill=col, width=3)

    # 음파 (귀 왼쪽)
    wave_x = ex - 10
    for i, rr in enumerate([14, 22, 30]):
        alpha_val = 255 - i * 55
        draw.arc([wave_x - rr, cy - rr, wave_x + rr, cy + rr],
                 start=150, end=210, fill=(*col, alpha_val), width=3)


ICON_FUNCS = [draw_icon_nfc, draw_icon_tap, draw_icon_link, draw_icon_ear]

# ════════════════════════════════════════════════════
# ── 스텝 배치 ─────────────────────────────────────
# ════════════════════════════════════════════════════

steps = [
    ("스마트폰 NFC 기능을 켜주세요",    "Enable NFC on your smartphone",                None),
    ("키링 뒷면에 폰을 가까이 대세요",   "Hold your phone near the back of the keyring", None),
    ("화면에 나타나는 링크를 탭하세요",  "Tap the link that appears on your screen",     None),
    ("선암사의 자연 소리를 감상하세요",   "Enjoy the natural soundscape of Seonamsa",
     "선암사에서 직접 녹음한 음원입니다.\n산사의 소리풍경에 귀를 기울여 보세요."),
]

STEP_START_Y = 356
step_heights  = [288, 288, 288, 356]   # 4번은 노트 포함으로 더 높음
SNUM_R  = 30
ILLUST_S = 96
PAD_L   = 72

f_sko  = fnt(FONT_KO_EB, 42)
f_sen  = fnt(FONT_KO_L,  28)
f_note = fnt(FONT_MJ,    24)
f_snum = fnt(FONT_MJ_B,  28)

sy = STEP_START_Y + 16

for i, (ko, en, note) in enumerate(steps):
    sh  = step_heights[i]
    mid_y = sy + sh // 2

    # ── 번호 원 (골드) ──
    draw.ellipse([PAD_L, mid_y - SNUM_R,
                  PAD_L + SNUM_R * 2, mid_y + SNUM_R],
                 fill=GOLD)
    draw.text((PAD_L + SNUM_R, mid_y), str(i + 1),
              font=f_snum, fill=GREEN_DEEP, anchor="mm")

    # ── 일러스트 박스 (반투명 녹색 패널) ──
    IL_X = PAD_L + SNUM_R * 2 + 26
    IL_Y = mid_y - ILLUST_S // 2
    # 박스 배경
    overlay2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od2 = ImageDraw.Draw(overlay2)
    od2.rounded_rectangle([IL_X, IL_Y, IL_X + ILLUST_S, IL_Y + ILLUST_S],
                           radius=14,
                           fill=(*GREEN_LIGHT, 55),
                           outline=(*GOLD, 80), width=2)
    img.paste(Image.alpha_composite(img.convert("RGBA"), overlay2).convert("RGB"))
    draw = ImageDraw.Draw(img, "RGBA")

    # ── 아이콘 그리기 ──
    icon_cx = IL_X + ILLUST_S // 2
    icon_cy = mid_y
    ICON_FUNCS[i](icon_cx, icon_cy, ILLUST_S, GOLD_LT)

    # ── 텍스트 ──
    TX2 = IL_X + ILLUST_S + 30
    if note:
        text_mid = mid_y - 20
    else:
        text_mid = mid_y - 10

    draw.text((TX2, text_mid - 26), ko,  font=f_sko,  fill=BEIGE)
    draw.text((TX2, text_mid + 28), en,  font=f_sen,  fill=BEIGE_DIM)
    if note:
        f_note_use = fnt(FONT_MJ, 24)
        draw.text((TX2, text_mid + 70), note,
                  font=f_note_use, fill=(*GOLD_LT, 220))

    # ── 구분선 ──
    if i < 3:
        line_y = sy + sh - 2
        draw.line([(PAD_L, line_y), (W - PAD_L, line_y)],
                  fill=(*GOLD, 40), width=1)

    sy += sh

# ════════════════════════════════════════════════════
# ── 푸터 ────────────────────────────────────────────
# ════════════════════════════════════════════════════
FOOTER_TOP = sy + 28
draw.line([(72, FOOTER_TOP), (W - 72, FOOTER_TOP)], fill=(*GOLD, 80), width=1)

# UNESCO pill
UB_Y = FOOTER_TOP + 28
f_ubadge = fnt(FONT_KO_L, 22)
ub_text  = "★  UNESCO WORLD HERITAGE  ★"
ub_w     = int(draw.textlength(ub_text, font=f_ubadge)) + 64
ub_h     = 52
draw.rounded_rectangle([72, UB_Y, 72 + ub_w, UB_Y + ub_h],
                        radius=ub_h // 2,
                        outline=GOLD, width=2)
draw.text((72 + ub_w // 2, UB_Y + ub_h // 2), ub_text,
          font=f_ubadge, fill=GOLD_LT, anchor="mm")

# 기관명 pill 3개
f_org = fnt(FONT_KO_R, 21)
orgs  = ["국가유산청", "순천시", "세계유산활용프로그램"]
ox = 72
oy = UB_Y + ub_h + 20
for org in orgs:
    ow = int(draw.textlength(org, font=f_org)) + 48
    oh = 46
    draw.rounded_rectangle([ox, oy, ox + ow, oy + oh],
                            radius=oh // 2,
                            outline=(*GOLD, 110), width=1)
    draw.text((ox + ow // 2, oy + oh // 2), org,
              font=f_org, fill=BEIGE_DIM, anchor="mm")
    ox += ow + 16

# 카피라이트
f_copy = fnt(FONT_KO_L, 17)
copy_y = oy + 62
draw.text((72, copy_y),
          "© 2026 SIMDA. All rights reserved.",
          font=f_copy, fill=(*BEIGE_DIM, 100))

# ── 저장 ─────────────────────────────────────────────
out = "seonamsa/nfc-guide-mobile.png"
img.save(out, "PNG", optimize=True)
size_kb = os.path.getsize(out) // 1024
print(f"PNG 저장 완료: {W}x{H}px  {size_kb}KB  →  {out}")

# 레이아웃 디버그
total_used = STEP_START_Y + 16 + sum(step_heights) + 28 + ub_h + 20 + 46 + 62 + 24
print(f"세로 사용 영역: {total_used}px / {H}px (단청바 제외)")
