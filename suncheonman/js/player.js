/* ============================================================
   순천만 사운드트랙 — Player v2
   컨셉: 람사르 습지 순천만(한국의 갯벌) 자연 소리
   ============================================================ */

'use strict';

// ──────────────────────────────────────────────
// 🎵 트랙 데이터
// ──────────────────────────────────────────────
const TRACKS = [
  {
    id: 1,
    title: '순천만 저녁 만조',
    artist: 'Suncheonman Bay',
    subtitle: '만조 · 밤',
    src: '/suncheonman/audio/track01.mp3',
    cover: '/suncheonman/images/cover01.jpg',
    desc: '칠흑 같은 밤, 만조로 채워진 순천만 갯벌 위로 물결이 스며들며 갈대숲 사이 잔잔한 파도 소리가 속삭입니다. 별빛 흩뿌려진 수면 위로 흐르는 물소리가 마음 깊이 평온함을 전합니다.',
  },
  {
    id: 2,
    title: '짱뚱어밭',
    artist: 'Suncheonman Bay',
    subtitle: '짱뚱어 · 갯벌',
    src: '/suncheonman/audio/track02.mp3',
    cover: '/suncheonman/images/cover02.jpg',
    desc: '썰물 진 갯벌 위로 짱뚱어들이 통통 튀어 다니고, 물 빠지는 보글보글 소리와 갈매기 울음, 갈대 바람 소리가 어우러져 생명력 넘치는 습지의 교향곡을 들려줍니다.',
  },
  {
    id: 3,
    title: '순천만가는길',
    artist: 'Suncheonman Bay',
    subtitle: '여수만 · 밤바다',
    src: '/suncheonman/audio/track03.mp3',
    cover: '/suncheonman/images/cover03.jpg',
    desc: '여수만과 순천만이 만나는 여름밤, 잔잔한 파도가 해안에 부드럽게 부딪히고 풀벌레 합창이 어우러져 별빛 수놓인 고요한 밤바다의 선율을 들려줍니다.',
  },
  {
    id: 4,
    title: '용산전망대 새벽',
    artist: 'Suncheonman Bay',
    subtitle: '용산전망대 · 새벽',
    src: '/suncheonman/audio/track04.mp3',
    cover: '/suncheonman/images/cover04.jpg',
    desc: '여름밤에서 새벽으로 넘어가는 순간, 매미의 마지막 열창과 새들의 지저귐, 갈대를 스치는 바람과 잔잔한 파도 소리가 어우러져 새로운 하루를 여는 자연의 합창을 들려줍니다.',
  },
  {
    id: 5,
    title: '화포항 저녁만조 통통배',
    artist: 'Suncheonman Bay',
    subtitle: '화포항 · 통통배',
    src: '/suncheonman/audio/track05.mp3',
    cover: '/suncheonman/images/cover05.jpg',
    desc: '만조로 가득 찬 화포항의 밤, 어선들이 잔잔한 물결에 살짝 흔들리며 통통통 찰박찰박 경쾌한 소리를 내고, 다리 위 불빛이 수면에 반사되는 평온한 항구의 밤을 들려줍니다.',
  },
];

// ──────────────────────────────────────────────
// DOM 참조
// ──────────────────────────────────────────────
const audio         = document.getElementById('audioPlayer');
const playPauseBtn  = document.getElementById('playPauseBtn');
const playIcon      = document.getElementById('playIcon');
const prevBtn       = document.getElementById('prevBtn');
const nextBtn       = document.getElementById('nextBtn');
const prevTrack     = document.getElementById('prevTrack');
const nextTrack     = document.getElementById('nextTrack');
const shuffleBtn    = document.getElementById('shuffleBtn');
const repeatBtn     = document.getElementById('repeatBtn');
const progressWrap  = document.getElementById('progressWrap');
const progressFill  = document.getElementById('progressFill');
const progressThumb = document.getElementById('progressThumb');
const timeCurrent   = document.getElementById('timeCurrent');
const timeTotal     = document.getElementById('timeTotal');
const totalDuration = document.getElementById('totalDuration');
const trackTitle    = document.getElementById('trackTitle');
const trackArtist   = document.getElementById('trackArtist');
const trackNumber   = document.getElementById('trackNumber');
const albumImg      = document.getElementById('albumImg');
const albumFallback = document.getElementById('albumFallback');
const vinyl         = document.getElementById('vinyl');
const tracklistEl   = document.getElementById('tracklist');
const soundDesc     = document.getElementById('soundDesc');

// ──────────────────────────────────────────────
// 상태
// ──────────────────────────────────────────────
let currentIndex = 0;
let isPlaying    = false;
let isShuffle    = false;
let repeatMode   = 0; // 0=off 1=all 2=one
let isDragging   = false;

// ──────────────────────────────────────────────
// 유틸리티
// ──────────────────────────────────────────────
function formatTime(sec) {
  if (isNaN(sec) || sec < 0) return '0:00';
  const m = Math.floor(sec / 60);
  const s = Math.floor(sec % 60);
  return `${m}:${s.toString().padStart(2, '0')}`;
}

function pad2(n) { return String(n).padStart(2, '0'); }

// ──────────────────────────────────────────────
// 트랙 로드 & 렌더
// ──────────────────────────────────────────────
function loadTrack(index, autoPlay = false) {
  const track = TRACKS[index];
  currentIndex = index;

  audio.src = track.src;
  audio.load();

  // UI 업데이트
  trackTitle.textContent  = track.title;
  trackArtist.textContent = track.artist;
  trackNumber.textContent = `${pad2(index + 1)} / ${pad2(TRACKS.length)}`;

  // 사운드 설명 업데이트
  if (soundDesc) {
    soundDesc.style.opacity = '0';
    soundDesc.style.transition = 'opacity 0.4s ease';
    setTimeout(() => {
      soundDesc.textContent = track.desc;
      soundDesc.style.opacity = '1';
    }, 300);
  }

  // 앨범 커버 — 항상 CD 커버 이미지 고정 (트랙마다 바뀌지 않음)
  albumImg.src = '/suncheonman/images/cd_cover.jpg';
  albumImg.style.display = 'block';
  albumFallback.style.display = 'none';
  albumImg.onerror = () => { albumImg.style.display = 'none'; albumFallback.style.display = 'flex'; };

  // 진행바 리셋
  updateProgress(0, 0);
  timeCurrent.textContent   = '0:00';
  timeTotal.textContent     = '0:00';
  totalDuration.textContent = '0:00';

  renderTracklist();

  if (autoPlay) playAudio();
  else pauseAudio();
}

// ──────────────────────────────────────────────
// 재생 / 일시정지
// ──────────────────────────────────────────────
function playAudio() {
  const promise = audio.play();
  if (promise !== undefined) {
    promise.then(() => {
      isPlaying = true;
      playIcon.className = 'fas fa-pause';
      vinyl.classList.add('spinning');
    }).catch(() => {
      // autoplay blocked
    });
  }
}

function pauseAudio() {
  audio.pause();
  isPlaying = false;
  playIcon.className = 'fas fa-play';
  vinyl.classList.remove('spinning');
}

function togglePlay() {
  if (audio.src && audio.src !== window.location.href) {
    if (isPlaying) pauseAudio(); else playAudio();
  }
}

// ──────────────────────────────────────────────
// 트랙 이동
// ──────────────────────────────────────────────
function goNext() {
  let idx;
  if (isShuffle) {
    do { idx = Math.floor(Math.random() * TRACKS.length); }
    while (idx === currentIndex && TRACKS.length > 1);
  } else {
    idx = (currentIndex + 1) % TRACKS.length;
  }
  loadTrack(idx, isPlaying);
}

function goPrev() {
  if (audio.currentTime > 3) {
    audio.currentTime = 0;
    return;
  }
  const idx = (currentIndex - 1 + TRACKS.length) % TRACKS.length;
  loadTrack(idx, isPlaying);
}

// ──────────────────────────────────────────────
// 진행바
// ──────────────────────────────────────────────
function updateProgress(current, duration) {
  const pct = duration > 0 ? (current / duration) * 100 : 0;
  progressFill.style.width = `${pct}%`;
  progressThumb.style.left = `${pct}%`;
  if (progressWrap) progressWrap.setAttribute('aria-valuenow', Math.round(pct));
}

function seekFromEvent(e) {
  const rect = progressWrap.getBoundingClientRect();
  const clientX = e.touches ? e.touches[0].clientX : e.clientX;
  const ratio = Math.min(Math.max((clientX - rect.left) / rect.width, 0), 1);
  if (!isNaN(audio.duration) && audio.duration > 0) {
    audio.currentTime = ratio * audio.duration;
  }
  updateProgress(ratio * (audio.duration || 0), audio.duration || 0);
}

progressWrap.addEventListener('mousedown', (e) => { isDragging = true; seekFromEvent(e); });
progressWrap.addEventListener('touchstart', (e) => { isDragging = true; seekFromEvent(e); }, { passive: true });
document.addEventListener('mousemove', (e) => { if (isDragging) seekFromEvent(e); });
document.addEventListener('touchmove', (e) => { if (isDragging) seekFromEvent(e); }, { passive: true });
document.addEventListener('mouseup',  () => { isDragging = false; });
document.addEventListener('touchend', () => { isDragging = false; });

// ──────────────────────────────────────────────
// Audio 이벤트
// ──────────────────────────────────────────────
audio.addEventListener('timeupdate', () => {
  if (!isDragging) {
    updateProgress(audio.currentTime, audio.duration);
    timeCurrent.textContent = formatTime(audio.currentTime);
  }
});

audio.addEventListener('loadedmetadata', () => {
  timeTotal.textContent    = formatTime(audio.duration);
  totalDuration.textContent = formatTime(audio.duration);
});

audio.addEventListener('ended', () => {
  if (repeatMode === 2) {
    audio.currentTime = 0;
    playAudio();
  } else {
    goNext();
  }
});

audio.addEventListener('error', () => { pauseAudio(); });

// ──────────────────────────────────────────────
// 트랙리스트 렌더
// ──────────────────────────────────────────────
function renderTracklist() {
  tracklistEl.innerHTML = '';

  TRACKS.forEach((track, i) => {
    const li = document.createElement('li');
    li.className = 'track-item' + (i === currentIndex ? ' playing' : '');
    li.setAttribute('role', 'listitem');
    li.setAttribute('tabindex', '0');
    li.setAttribute('aria-label', `${track.title} — ${track.artist}`);

    li.innerHTML = `
      <div class="track-num">
        <span class="num-label">${pad2(i + 1)}</span>
        <div class="playing-indicator" aria-hidden="true">
          <span></span><span></span><span></span>
        </div>
      </div>
      <div class="track-cover-thumb">
        <img src="${track.cover}" alt="${track.title} 커버" class="thumb-img" />
      </div>
      <div class="track-details">
        <p class="track-name">${track.title}</p>
        <p class="track-meta">${track.subtitle || track.artist}</p>
      </div>
      <span class="track-duration" data-idx="${i}">--:--</span>
    `;

    li.addEventListener('click', () => loadTrack(i, true));
    li.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') loadTrack(i, true);
    });

    tracklistEl.appendChild(li);
  });

  // 현재 트랙 이퀄라이저 표시
  const items = tracklistEl.querySelectorAll('.track-item');
  items.forEach((item, i) => {
    const numLabel  = item.querySelector('.num-label');
    const indicator = item.querySelector('.playing-indicator');
    if (i === currentIndex) {
      numLabel.style.display  = 'none';
      indicator.style.display = 'flex';
    } else {
      numLabel.style.display  = 'block';
      indicator.style.display = 'none';
    }
  });

  // 썸네일 에러 처리
  tracklistEl.querySelectorAll('.thumb-img').forEach(img => {
    img.addEventListener('error', function () {
      const wrapper = this.closest('.track-cover-thumb');
      if (wrapper) wrapper.innerHTML = '<i class="fas fa-feather" style="color:var(--gold);font-size:1rem"></i>';
    });
  });

  loadTrackDurations();
}

// ──────────────────────────────────────────────
// 트랙 길이 미리 로드
// ──────────────────────────────────────────────
function loadTrackDurations() {
  TRACKS.forEach((track, i) => {
    const tempAudio = new Audio();
    tempAudio.src = track.src;
    tempAudio.preload = 'metadata';
    tempAudio.addEventListener('loadedmetadata', () => {
      const el = tracklistEl.querySelector(`[data-idx="${i}"]`);
      if (el) el.textContent = formatTime(tempAudio.duration);
    });
  });
}

// ──────────────────────────────────────────────
// 셔플 / 반복 토글
// ──────────────────────────────────────────────
function toggleShuffle() {
  isShuffle = !isShuffle;
  shuffleBtn.classList.toggle('active', isShuffle);
  shuffleBtn.title = isShuffle ? '셔플 켜짐' : '셔플';
}

function toggleRepeat() {
  repeatMode = (repeatMode + 1) % 3;
  repeatBtn.classList.toggle('active', repeatMode > 0);
  if (repeatMode === 0) {
    repeatBtn.innerHTML = '<i class="fas fa-redo-alt"></i>';
    repeatBtn.title = '반복 없음';
  } else if (repeatMode === 1) {
    repeatBtn.innerHTML = '<i class="fas fa-redo-alt"></i>';
    repeatBtn.title = '전체 반복';
  } else {
    repeatBtn.innerHTML = '<i class="fas fa-redo-alt"></i><sup style="font-size:0.5rem;position:relative;top:-5px;left:-2px;color:var(--gold)">1</sup>';
    repeatBtn.title = '한 곡 반복';
  }
}

// ──────────────────────────────────────────────
// 이벤트 바인딩
// ──────────────────────────────────────────────
playPauseBtn.addEventListener('click', togglePlay);
prevBtn.addEventListener('click', goPrev);
nextBtn.addEventListener('click', goNext);
prevTrack.addEventListener('click', goPrev);
nextTrack.addEventListener('click', goNext);
shuffleBtn.addEventListener('click', toggleShuffle);
repeatBtn.addEventListener('click', toggleRepeat);

// 키보드 단축키
document.addEventListener('keydown', (e) => {
  const tag = document.activeElement.tagName;
  if (tag === 'INPUT' || tag === 'TEXTAREA') return;
  switch (e.code) {
    case 'Space':
      e.preventDefault();
      togglePlay();
      break;
    case 'ArrowRight':
      if (e.shiftKey) goNext();
      else if (!isNaN(audio.duration)) audio.currentTime = Math.min(audio.currentTime + 5, audio.duration);
      break;
    case 'ArrowLeft':
      if (e.shiftKey) goPrev();
      else audio.currentTime = Math.max(audio.currentTime - 5, 0);
      break;
  }
});

// ──────────────────────────────────────────────
// 초기화
// ──────────────────────────────────────────────
function init() {
  renderTracklist();
  loadTrack(0, false);
}

init();
