import base64, os

with open('/home/user/webapp/suncheonman/images/cd_cover.jpg','rb') as f:
    cover_b64 = base64.b64encode(f.read()).decode()
with open('/home/user/webapp/suncheonman/images/cd_disc.png','rb') as f:
    disc_b64 = base64.b64encode(f.read()).decode()

svg1 = '''<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="8" y="10" width="32" height="28" rx="3" stroke="white" stroke-width="2.2"/>
  <path d="M8 18h32" stroke="white" stroke-width="2"/>
  <circle cx="24" cy="30" r="5" stroke="white" stroke-width="2"/>
  <path d="M21 30l2 2 4-4" stroke="white" stroke-width="2" stroke-linecap="round"/>
</svg>'''

svg2 = '''<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="14" y="6" width="20" height="36" rx="3" stroke="white" stroke-width="2.2"/>
  <circle cx="24" cy="37" r="2" stroke="white" stroke-width="1.8"/>
  <path d="M20 10h8" stroke="white" stroke-width="2" stroke-linecap="round"/>
  <path d="M17 22c2-3 5-4 7-4s5 1 7 4" stroke="white" stroke-width="2" stroke-linecap="round"/>
  <path d="M20 27c1-2 2.5-3 4-3s3 1 4 3" stroke="white" stroke-width="2" stroke-linecap="round"/>
</svg>'''

svg3 = '''<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="24" cy="24" r="14" stroke="white" stroke-width="2.2"/>
  <circle cx="24" cy="24" r="4" stroke="white" stroke-width="2"/>
  <path d="M24 10v4M24 34v4M10 24h4M34 24h4" stroke="white" stroke-width="2" stroke-linecap="round"/>
  <path d="M17 17l3 3M28 28l3 3M17 31l3-3M28 20l3-3" stroke="white" stroke-width="1.8" stroke-linecap="round"/>
</svg>'''

svg4 = '''<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M24 8c-7.2 0-13 5.8-13 13 0 4.5 2.3 8.5 5.8 10.8v3.7c0 2.5 2 4.5 4.5 4.5 1.2 0 2.3-.5 3.1-1.3l3.2-3.2c4.9-1.2 8.4-5.6 8.4-10.5C36 13.8 30.6 8 24 8z" stroke="white" stroke-width="2.2" stroke-linejoin="round"/>
  <path d="M20 21c0-2.2 1.8-4 4-4s4 1.8 4 4c0 1.5-.8 2.8-2 3.5v4.5" stroke="white" stroke-width="1.8" stroke-linecap="round"/>
  <path d="M38 17c1.5 2 2.5 4.5 2.5 7" stroke="white" stroke-width="1.8" stroke-linecap="round" opacity="0.7"/>
  <path d="M41 14c2.5 3.2 4 7.2 4 11.5" stroke="white" stroke-width="1.5" stroke-linecap="round" opacity="0.4"/>
</svg>'''

nfc_svg = '''<svg viewBox="0 0 24 24" fill="#D4A24A" xmlns="http://www.w3.org/2000/svg" style="width:32px;height:32px;">
  <path d="M1 9l2 2c4.97-4.97 13.03-4.97 18 0l2-2C16.93 2.93 7.08 2.93 1 9zm8 8l3 3 3-3c-1.65-1.66-4.34-1.66-6 0zm-4-4l2 2c2.76-2.76 7.24-2.76 10 0l2-2C15.14 9.14 8.87 9.14 5 13z"/>
</svg>'''

steps = [
    ("스마트폰 NFC 기능을 켜주세요",   "Enable NFC on your smartphone",                   svg1, ""),
    ("키링 뒷면에 폰을 가까이 대세요",  "Hold your phone near the back of the keyring",    svg2, ""),
    ("화면에 나타나는 링크를 탭하세요",  "Tap the link that appears on your screen",        svg3, ""),
    ("순천만의 자연 소리를 감상하세요",  "Enjoy the natural soundscape of Suncheonman Bay",        svg4,
     "순천만에서 직접 녹음한 음원입니다.<br>갯벌의 소리풍경에 귀를 기울여 보세요."),
]

steps_html = ""
for i, (ko, en, svg, note) in enumerate(steps):
    note_html = f'<div class="snote">{note}</div>' if note else ''
    steps_html += f'''
    <div class="step">
      <div class="snum">{i+1}</div>
      <div class="illust">{svg}</div>
      <div class="stxt">
        <div class="sko">{ko}</div>
        <div class="sen">{en}</div>
        {note_html}
      </div>
    </div>'''

html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<style>
@import url('https://fonts.googleapis.com/css2?family=Nanum+Myeongjo:wght@400;700&family=Bebas+Neue&family=Montserrat:wght@400;500;600;700&family=Noto+Sans+KR:wght@300;400;500;700&display=swap');

/* ── 1080 × 1920 px 고정 캔버스 ── */
* {{ box-sizing:border-box; margin:0; padding:0; }}
html, body {{
  width:1080px; height:1920px;
  overflow:hidden;
  background:#111;
  font-family:'Noto Sans KR',sans-serif;
}}

.card {{
  width:1080px; height:1920px;
  background:#3D2408;
  position:relative;
  overflow:hidden;
  display:flex;
  flex-direction:column;
}}

/* ── 단청 장식 바 ── */
.dbar {{
  width:100%; height:14px; flex-shrink:0;
  background:repeating-linear-gradient(90deg,
    #D4A24A 0,#D4A24A 18px,
    #6B4520 18px,#6B4520 36px,
    #E3C9A0 36px,#E3C9A0 54px,
    #6B4520 54px,#6B4520 72px);
  opacity:.85;
}}

/* ── 배경 원 장식 ── */
.bgc {{
  position:absolute; border-radius:50%;
  background:#D4A24A; opacity:.05; pointer-events:none;
}}
.bgc.a {{ width:700px; height:700px; right:-120px; top:-120px; }}
.bgc.b {{ width:480px; height:480px; left:-100px; bottom:-80px; }}
.bgc.c {{ width:300px; height:300px; right:80px;  bottom:200px; }}

/* ── 본문 영역 ── */
.body {{
  flex:1;
  display:flex;
  flex-direction:column;
  padding:72px 80px 56px;
  gap:0;
  position:relative;
  z-index:1;
}}

/* ── 헤더: CD 이미지 + 타이틀 + NFC ── */
.header {{
  display:flex;
  align-items:flex-start;
  gap:48px;
  flex-shrink:0;
  margin-bottom:64px;
}}

.cd-stack {{
  position:relative;
  width:220px; height:220px;
  flex-shrink:0;
}}
.cd-cover {{
  position:absolute; top:0; left:0;
  width:190px; height:190px;
  border-radius:10px;
  object-fit:cover;
  box-shadow:0 6px 28px rgba(0,0,0,.55);
  z-index:1;
}}
.cd-disc {{
  position:absolute; bottom:0; right:0;
  width:120px; height:120px;
  border-radius:50%;
  object-fit:cover;
  box-shadow:0 4px 18px rgba(0,0,0,.6);
  z-index:2;
  border:2px solid rgba(212,162,74,.35);
}}

.title-nfc {{
  flex:1;
  display:flex;
  align-items:flex-start;
  justify-content:space-between;
}}
.title-block {{ display:flex; flex-direction:column; gap:10px; padding-top:8px; }}
.bt-main {{
  font-family:'Bebas Neue',sans-serif;
  font-size:88px; letter-spacing:.18em; line-height:1;
  color:#F2E4CC;
}}
.bt-sub {{
  font-family:'Montserrat',sans-serif;
  font-size:20px; font-weight:600;
  letter-spacing:.30em; text-transform:uppercase;
  color:#ECC97A; opacity:.9;
}}
.bt-ko {{
  font-family:'Nanum Myeongjo',serif;
  font-size:22px; letter-spacing:.18em;
  color:#E3C9A0; opacity:.72;
}}

.nfc-mark {{
  display:flex; flex-direction:column;
  align-items:center; gap:10px;
  padding-top:12px;
}}
.nfc-outer {{
  width:80px; height:80px;
  border-radius:50%;
  border:4px solid #D4A24A;
  display:flex; align-items:center; justify-content:center;
  background:rgba(212,162,74,.1);
}}
.nfc-txt {{
  font-family:'Montserrat',sans-serif;
  font-size:18px; font-weight:700;
  letter-spacing:.22em; color:#ECC97A;
  text-transform:uppercase;
}}

/* ── 구분선 헤더 ── */
.sec-label {{
  display:flex; align-items:center; gap:20px;
  margin-bottom:48px;
  flex-shrink:0;
}}
.sec-label-ko {{
  font-family:'Noto Sans KR',sans-serif;
  font-size:28px; font-weight:700;
  color:#ECC97A; letter-spacing:.1em; white-space:nowrap;
}}
.sec-label-en {{
  font-family:'Montserrat',sans-serif;
  font-size:20px; font-weight:600;
  color:#ECC97A; letter-spacing:.18em;
  text-transform:uppercase; opacity:.55; white-space:nowrap;
}}
.sec-line {{
  flex:1; height:1px;
  background:rgba(212,162,74,.4);
}}

/* ── 스텝 리스트 ── */
.steps {{ flex:1; display:flex; flex-direction:column; gap:0; justify-content:center; }}

.step {{
  display:flex; align-items:center;
  gap:36px; padding:36px 0;
  border-bottom:1px solid rgba(212,162,74,.12);
}}
.step:last-child {{ border-bottom:none; }}

.snum {{
  width:56px; height:56px; flex-shrink:0;
  background-color:#D4A24A;
  border-radius:50%;
  display:flex; align-items:center; justify-content:center;
  font-family:'Montserrat',sans-serif;
  font-size:26px; font-weight:700;
  color:#3D2408;
}}

.illust {{
  width:88px; height:88px; flex-shrink:0;
  background:rgba(255,255,255,.07);
  border:1.5px solid rgba(255,255,255,.18);
  border-radius:14px;
  display:flex; align-items:center; justify-content:center;
  padding:10px;
}}
.illust svg {{ width:100%; height:100%; }}

.stxt {{ flex:1; }}
.sko {{
  font-family:'Noto Sans KR',sans-serif;
  font-size:38px; font-weight:500;
  color:#F2E4CC; line-height:1.3;
}}
.sen {{
  font-family:'Montserrat',sans-serif;
  font-size:24px; color:#E3C9A0;
  opacity:.55; line-height:1.3; margin-top:6px;
}}
.snote {{
  font-family:'Nanum Myeongjo',serif;
  font-size:22px; color:#ECC97A;
  opacity:.82; line-height:1.6; margin-top:10px;
}}

/* ── 푸터 ── */
.footer {{
  flex-shrink:0;
  border-top:1px solid rgba(212,162,74,.28);
  padding-top:36px;
  display:flex; flex-direction:column; gap:18px;
  position:relative; z-index:1;
}}

.ubadge-row {{ display:flex; }}
.ubadge {{
  display:inline-block;
  padding:14px 48px;
  border-width:2px; border-style:solid; border-color:#D4A24A;
  border-radius:999px;
  font-family:'Montserrat',sans-serif;
  font-size:20px; font-weight:700;
  letter-spacing:.22em; color:#ECC97A;
  text-transform:uppercase; white-space:nowrap;
}}

.orgs-row {{ display:flex; gap:16px; align-items:center; flex-wrap:wrap; }}
.obadge {{
  display:inline-block;
  padding:10px 28px;
  border-width:1.5px; border-style:solid; border-color:rgba(212,162,74,.4);
  border-radius:999px;
  font-family:'Noto Sans KR',sans-serif;
  font-size:20px; font-weight:400;
  color:#E3C9A0; letter-spacing:.04em; opacity:.85;
  white-space:nowrap;
}}

.copy {{
  font-family:'Montserrat',sans-serif;
  font-size:16px; color:#E3C9A0; opacity:.3;
  letter-spacing:.04em;
}}
</style>
</head>
<body>
<div class="card">
  <!-- 배경 장식 -->
  <div class="bgc a"></div>
  <div class="bgc b"></div>
  <div class="bgc c"></div>

  <!-- 상단 단청 바 -->
  <div class="dbar"></div>

  <!-- 본문 -->
  <div class="body">

    <!-- 헤더 -->
    <div class="header">
      <div class="cd-stack">
        <img class="cd-cover" src="data:image/jpeg;base64,{cover_b64}" alt="CD"/>
        <img class="cd-disc"  src="data:image/png;base64,{disc_b64}"  alt="Disc"/>
      </div>
      <div class="title-nfc">
        <div class="title-block">
          <div class="bt-main">SUNCHEONMAN</div>
          <div class="bt-sub">WETLAND&nbsp;&nbsp;SOUNDSCAPE</div>
          <div class="bt-ko">순천만 사운드스케이프</div>
        </div>
        <div class="nfc-mark">
          <div class="nfc-outer">{nfc_svg}</div>
          <div class="nfc-txt">NFC</div>
        </div>
      </div>
    </div>

    <!-- 사용법 섹션 헤더 -->
    <div class="sec-label">
      <span class="sec-label-ko">사용법</span>
      <span class="sec-label-en">How to Use</span>
      <div class="sec-line"></div>
    </div>

    <!-- 스텝 4개 -->
    <div class="steps">
      {steps_html}
    </div>

  </div>

  <!-- 하단 단청 바 -->
  <div class="dbar"></div>

  <!-- 푸터 (단청 바 위) -->
  <div style="padding:0 80px 56px; position:relative; z-index:1;">
    <div class="footer">
      <div class="ubadge-row">
        <span class="ubadge">★&nbsp;&nbsp;KOREAN TIDAL FLATS · 2021&nbsp;&nbsp;★</span>
      </div>
      <div class="orgs-row">
        <span class="obadge">국가유산청</span>
        <span class="obadge">순천시</span>
        <span class="obadge">순천만국가정원</span>
      </div>
      <div class="copy">© 2026 SIMDA. All rights reserved. | Audio and multimedia content rights are reserved by SIMDA.</div>
    </div>
  </div>

</div>
</body>
</html>'''

out = '/home/user/webapp/suncheonman/nfc-guide-mobile.html'
with open(out,'w',encoding='utf-8') as f:
    f.write(html)
print(f'HTML 생성 완료: {os.path.getsize(out)//1024}KB')
