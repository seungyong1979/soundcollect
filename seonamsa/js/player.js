/* ============================================================
   선암사 사운드트랙 — Player v2
   컨셉: 유네스코 세계유산 선암사 자연 소리
   ============================================================ */

'use strict';

// ──────────────────────────────────────────────
// 🎵 트랙 데이터
// ──────────────────────────────────────────────
const TRACKS = [
  {
    id: 1,
    title: '새벽 종소리',
    artist: 'Seonamsa Temple',
    subtitle: '새벽의 고요함',
    src: '/seonamsa/audio/track01.mp3',
    cover: '/seonamsa/images/cover01.jpg',
    desc: '이른 새벽, 선암사 종루에서 울려 퍼지는 은은한 종소리가 고요한 산사의 공기를 가득 채웁니다.',
  },
  {
    id: 2,
    title: '계곡 물소리',
    artist: 'Seonamsa Temple',
    subtitle: '승선교 아래',
    src: '/seonamsa/audio/track02.mp3',
    cover: '/seonamsa/images/cover02.jpg',
    desc: '승선교 아래로 흐르는 계곡물 소리. 바위를 타고 흐르는 맑은 물소리가 마음을 씻어줍니다.',
  },
  {
    id: 3,
    title: '숲속 새소리',
    artist: 'Seonamsa Temple',
    subtitle: '산사의 여름',
    src: '/seonamsa/audio/track03.mp3',
    cover: '/seonamsa/images/cover03.jpg',
    desc: '울창한 삼나무 숲 사이로 들려오는 새소리. 선암사의 여름 숲이 노래합니다.',
  },
  {
    id: 4,
    title: '빗소리와 처마',
    artist: 'Seonamsa Temple',
    subtitle: '여름 소나기',
    src: '/seonamsa/audio/track04.mp3',
    cover: '/seonamsa/images/cover04.jpg',
    desc: '처마 끝에서 떨어지는 빗방울 소리. 선암사 고목 사이를 적시는 여름 소나기의 정취.',
  },
  {
    id: 5,
    title: '풀벌레 소리',
    artist: 'Seonamsa Temple',
    subtitle: '여름밤 선암사',
    src: '/seonamsa/audio/track05.mp3',
    cover: '/seonamsa/images/cover05.jpg',
    desc: '해가 지고 나면 선암사 마당에 풀벌레 소리가 가득합니다. 여름밤의 고요하고 풍성한 자연 소리.',
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

  // 앨범 커버
  albumImg.src = track.cover;
  albumImg.style.display = 'block';
  albumFallback.style.display = 'flex';
  albumImg.onload  = () => { albumFallback.style.display = 'none'; };
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
      if (wrapper) wrapper.innerHTML = '<i class="fas fa-leaf" style="color:var(--gold);font-size:1rem"></i>';
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
