import base64, os

with open('/home/user/webapp/seonamsa/images/cd_cover.jpg','rb') as f:
    cover_b64 = base64.b64encode(f.read()).decode()
with open('/home/user/webapp/seonamsa/images/cd_disc.png','rb') as f:
    disc_b64 = base64.b64encode(f.read()).decode()

# SVG 일러스트 4종 (흰색 stroke)
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

# svg4 — 귀 이미지 (듣기/감상)
svg4 = '''<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- 귀 외형 -->
  <path d="M24 8c-7.2 0-13 5.8-13 13 0 4.5 2.3 8.5 5.8 10.8v3.7c0 2.5 2 4.5 4.5 4.5 1.2 0 2.3-.5 3.1-1.3l3.2-3.2c4.9-1.2 8.4-5.6 8.4-10.5C36 13.8 30.6 8 24 8z" stroke="white" stroke-width="2.2" stroke-linejoin="round"/>
  <!-- 귀 내부 선 -->
  <path d="M20 21c0-2.2 1.8-4 4-4s4 1.8 4 4c0 1.5-.8 2.8-2 3.5v4.5" stroke="white" stroke-width="1.8" stroke-linecap="round"/>
  <!-- 음파 -->
  <path d="M38 17c1.5 2 2.5 4.5 2.5 7" stroke="white" stroke-width="1.8" stroke-linecap="round" opacity="0.7"/>
  <path d="M41 14c2.5 3.2 4 7.2 4 11.5" stroke="white" stroke-width="1.5" stroke-linecap="round" opacity="0.4"/>
</svg>'''

# NFC SVG 아이콘 — 원래 WiFi/NFC 웨이브 아이콘 (골드)
nfc_svg = '''<svg viewBox="0 0 24 24" fill="#C8A96A" xmlns="http://www.w3.org/2000/svg" style="width:10pt;height:10pt;">
  <path d="M1 9l2 2c4.97-4.97 13.03-4.97 18 0l2-2C16.93 2.93 7.08 2.93 1 9zm8 8l3 3 3-3c-1.65-1.66-4.34-1.66-6 0zm-4-4l2 2c2.76-2.76 7.24-2.76 10 0l2-2C15.14 9.14 8.87 9.14 5 13z"/>
</svg>'''

NOTE4 = '선암사에서 직접 녹음한 음원입니다.<br/>산사의 소리풍경에 귀를 기울여 보세요.'
steps = [
    ("스마트폰 NFC 기능을 켜주세요", "Enable NFC on your smartphone", svg1, ""),
    ("키링 뒷면에 폰을 가까이 대세요", "Hold your phone near the back of the keyring", svg2, ""),
    ("화면에 나타나는 링크를 탭하세요", "Tap the link that appears on your screen", svg3, ""),
    ("선암사의 자연 소리를 감상하세요", "Enjoy the natural soundscape of Seonamsa", svg4, NOTE4),
]

step_labels = [
    ("열기", "UNLOCK"),
    ("연결", "CONNECT"),
    ("감상", "LISTEN"),
    ("공유", "SHARE"),
]

def make_card(card_id):
    rows = []
    for i,(ko,en,svg,note) in enumerate(steps):
        lko, len_ = step_labels[i]
        note_html = f'<div class="step-note">{note}</div>' if note else ''
        rows.append(f'''
        <div class="step">
          <div class="snum">{i+1}</div>
          <div class="illust">{svg}</div>
          <div class="stxt">
            <div class="sko">{ko}</div>
            <div class="sen">{en}</div>
            {note_html}
          </div>
        </div>''')
    steps_html = '\n'.join(rows)

    return f'''
<div class="card {card_id}">
  <div class="dbar t"></div>
  <div class="dbar b"></div>
  <div class="bgc a"></div>
  <div class="bgc b"></div>
  <div class="ci">

    <div class="top-row">
      <div class="cd-stack">
        <img class="cd-cover-img" src="data:image/jpeg;base64,{cover_b64}" alt="CD Cover"/>
        <img class="cd-disc-img" src="data:image/png;base64,{disc_b64}" alt="CD Disc"/>
      </div>
      <div class="title-nfc">
        <div class="title-block">
          <div class="bt-main">SEONAMSA</div>
          <div class="bt-sub">TEMPLE&nbsp;&nbsp;SOUNDSCAPE</div>
          <div class="bt-ko">선암사 사운드스케이프</div>
        </div>
        <div class="nfc-mark">
          <div class="nfc-outer">{nfc_svg}</div>
          <div class="nfc-txt">NFC</div>
        </div>
      </div>
    </div>

    <div class="ss">
      <div class="slabel">
        <span class="slabel-ko">사용법</span>
        <span class="slabel-en">How to Use</span>
        <div class="slabel-line"></div>
      </div>
      {steps_html}
    </div>

    <div class="cf">
      <div class="ubadge-row">
        <span class="ubadge">★&nbsp;&nbsp;UNESCO WORLD HERITAGE&nbsp;&nbsp;★</span>
      </div>
      <div class="orgs-row">
        <span class="obadge">국가유산청</span>
        <span class="obadge">순천시</span>
        <span class="obadge">세계유산활용프로그램</span>
      </div>
      <div class="copy">© 2026 SIMDA. All rights reserved. | Audio and multimedia content rights are reserved by SIMDA.</div>
    </div>

  </div>
</div>'''

html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8"/>
<style>
@import url('https://fonts.googleapis.com/css2?family=Nanum+Myeongjo:wght@400;700&family=Bebas+Neue&family=Montserrat:wght@400;500;600;700&family=Noto+Sans+KR:wght@300;400;500;700&display=swap');

:root {{
  --green-deep: #1A4D3E;
  --green-mid:  #2D6B58;
  --beige:      #D9C5B2;
  --beige-lt:   #EDE3D8;
  --gold:       #C8A96A;
  --gold-lt:    #E2C98A;
}}
*{{box-sizing:border-box;margin:0;padding:0;}}
@page{{size:210mm 297mm;margin:0;}}
html{{width:210mm;height:297mm;}}
body{{width:210mm;height:297mm;position:relative;overflow:hidden;
  background:#d4d4d4;font-family:'Noto Sans KR',sans-serif;}}

/* 칼선 */
.cut-h{{position:absolute;left:0;right:0;top:148.5mm;
  border-top:0.4pt dashed #999;z-index:20;}}
.cut-v{{position:absolute;top:0;bottom:0;left:105mm;
  border-left:0.4pt dashed #999;z-index:20;}}

/* 카드 */
.card{{position:absolute;width:105mm;height:148.5mm;
  background:#1A4D3E;overflow:hidden;}}
.c1{{top:0;left:0;}} .c2{{top:0;left:105mm;}}
.c3{{top:148.5mm;left:0;}} .c4{{top:148.5mm;left:105mm;}}

/* 단청 바 */
.dbar{{position:absolute;left:0;right:0;height:4pt;
  background:repeating-linear-gradient(90deg,
    #C8A96A 0,#C8A96A 5pt,
    #2D6B58 5pt,#2D6B58 10pt,
    #D9C5B2 10pt,#D9C5B2 15pt,
    #2D6B58 15pt,#2D6B58 20pt);
  opacity:.85;z-index:2;}}
.dbar.t{{top:0;}} .dbar.b{{bottom:0;}}

/* 배경 원형 */
.bgc{{position:absolute;border-radius:50%;background:#C8A96A;opacity:.05;}}
.bgc.a{{width:72mm;height:72mm;right:-14mm;top:-14mm;}}
.bgc.b{{width:42mm;height:42mm;left:-10mm;bottom:-10mm;}}

/* 카드 내부 */
.ci{{position:absolute;top:4pt;bottom:4pt;left:0;right:0;
  padding:8pt 8pt 6pt;
  display:flex;flex-direction:column;gap:5pt;}}

/* 상단 CD + 타이틀 */
.top-row{{display:flex;gap:7pt;align-items:flex-start;flex-shrink:0;}}
.cd-stack{{position:relative;width:20mm;height:20mm;flex-shrink:0;}}
.cd-cover-img{{position:absolute;top:0;left:0;width:18mm;height:18mm;
  border-radius:2pt;object-fit:cover;
  box-shadow:0 1pt 5pt rgba(0,0,0,.4);z-index:1;}}
.cd-disc-img{{position:absolute;bottom:0;right:0;width:12mm;height:12mm;
  border-radius:50%;object-fit:cover;
  box-shadow:0 1pt 4pt rgba(0,0,0,.5);z-index:2;}}

.title-nfc{{flex:1;display:flex;align-items:flex-start;
  justify-content:space-between;}}
.title-block{{display:flex;flex-direction:column;gap:2pt;}}
.bt-main{{font-family:'Bebas Neue',sans-serif;font-size:20pt;
  color:#EDE3D8;letter-spacing:.18em;line-height:1;}}
.bt-sub{{font-family:'Montserrat',sans-serif;font-size:4.5pt;font-weight:600;
  color:#E2C98A;letter-spacing:.26em;text-transform:uppercase;opacity:.9;}}
.bt-ko{{font-family:'Nanum Myeongjo',serif;font-size:5pt;
  color:#D9C5B2;letter-spacing:.18em;opacity:.72;}}

/* NFC 마크 — 골드 단일 원 */
.nfc-mark{{display:flex;flex-direction:column;align-items:center;gap:2.5pt;}}
.nfc-outer{{
  width:22pt;height:22pt;
  border-radius:50%;
  border:1.5pt solid #C8A96A;
  display:flex;align-items:center;justify-content:center;
  background:rgba(200,169,106,.08);
}}
.nfc-txt{{font-family:'Montserrat',sans-serif;font-size:4.5pt;font-weight:700;
  letter-spacing:.18em;color:#E2C98A;text-transform:uppercase;}}

/* 스텝 영역 */
.ss{{flex:1;display:flex;flex-direction:column;justify-content:center;}}
.slabel{{display:flex;align-items:center;gap:4pt;margin-bottom:4pt;}}
.slabel-ko{{font-family:'Noto Sans KR',sans-serif;font-size:7pt;font-weight:700;
  color:#E2C98A;letter-spacing:.08em;white-space:nowrap;}}
.slabel-en{{font-family:'Montserrat',sans-serif;font-size:5pt;font-weight:600;
  color:#E2C98A;letter-spacing:.14em;text-transform:uppercase;
  opacity:.6;white-space:nowrap;}}
.slabel-line{{flex:1;height:.4pt;
  background:rgba(200,169,106,.45);}}

.step{{display:flex;align-items:center;gap:5pt;padding:3pt 0;
  border-bottom:.35pt solid rgba(200,169,106,.13);}}
.step:last-child{{border-bottom:none;}}

/* 번호 원 — 배경색 직접 지정 (gradient NO) */
.snum{{
  width:14pt;height:14pt;flex-shrink:0;
  background-color:#C8A96A;
  border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  font-family:'Montserrat',sans-serif;font-size:7pt;font-weight:700;
  color:#1A4D3E;
}}

/* 일러스트 박스 */
.illust{{
  width:20pt;height:20pt;flex-shrink:0;
  background:rgba(255,255,255,.07);
  border:.6pt solid rgba(255,255,255,.18);
  border-radius:3pt;
  display:flex;align-items:center;justify-content:center;
  padding:1.5pt;
}}
.illust svg{{width:100%;height:100%;}}

/* 텍스트 */
.stxt{{flex:1;}}
.sko{{font-family:'Noto Sans KR',sans-serif;font-size:9.5pt;font-weight:500;
  color:#EDE3D8;line-height:1.35;}}
.sen{{font-family:'Montserrat',sans-serif;font-size:6.5pt;
  color:#D9C5B2;opacity:.6;line-height:1.3;margin-top:1pt;}}
.step-note{{font-family:'Nanum Myeongjo',serif;font-size:5pt;
  color:#E2C98A;opacity:.8;line-height:1.5;margin-top:1.5pt;}}

/* 푸터 */
.cf{{flex-shrink:0;margin-top:4pt;padding-top:4pt;
  border-top:.4pt solid rgba(200,169,106,.28);
  display:flex;flex-direction:column;gap:3pt;}}

/* UNESCO pill — border 단일, outline/box-shadow 없음 */
.ubadge-row{{display:flex;}}
.ubadge{{
  display:inline-block;
  padding:3pt 10pt;
  border-width:1pt;
  border-style:solid;
  border-color:#C8A96A;
  border-radius:100pt;
  outline:none;
  font-family:'Montserrat',sans-serif;font-size:4.5pt;font-weight:700;
  letter-spacing:.18em;color:#E2C98A;text-transform:uppercase;
  white-space:nowrap;
  -webkit-appearance:none;
}}

/* 기관 pill — 각각 독립 */
.orgs-row{{display:flex;gap:3pt;align-items:center;flex-wrap:wrap;}}
.obadge{{
  display:inline-block;
  padding:2pt 6pt;
  border-width:.7pt;
  border-style:solid;
  border-color:rgba(200,169,106,.45);
  border-radius:100pt;
  outline:none;
  font-family:'Noto Sans KR',sans-serif;font-size:4.5pt;font-weight:500;
  color:#D9C5B2;letter-spacing:.04em;opacity:.85;
  white-space:nowrap;
  -webkit-appearance:none;
}}

.copy{{font-family:'Montserrat',sans-serif;font-size:3pt;
  color:#D9C5B2;opacity:.32;letter-spacing:.04em;}}
</style>
</head>
<body>

<div class="cut-h"></div>
<div class="cut-v"></div>

{make_card("c1")}
{make_card("c2")}
{make_card("c3")}
{make_card("c4")}

</body>
</html>'''

out = '/home/user/webapp/seonamsa/nfc-guide-print.html'
with open(out,'w',encoding='utf-8') as f:
    f.write(html)
print(f'HTML 생성 완료: {os.path.getsize(out)//1024}KB')
