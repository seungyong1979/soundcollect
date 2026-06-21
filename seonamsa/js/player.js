/* ============================================================
   선삼사 사운드트랙 - Music Player
   ============================================================ */

'use strict';

// ──────────────────────────────────────────────
// 🎵 트랙 데이터 (mp3 파일 업로드 후 여기를 수정하세요)
// ──────────────────────────────────────────────
const TRACKS = [
  {
    id: 1,
    title: 'Track 01',
    artist: 'Seonamsa Temple',
    src: 'audio/track01.mp3',
    cover: 'images/cover01.jpg',
  },
  {
    id: 2,
    title: 'Track 02',
    artist: 'Seonamsa Temple',
    src: 'audio/track02.mp3',
    cover: 'images/cover02.jpg',
  },
  {
    id: 3,
    title: 'Track 03',
    artist: 'Seonamsa Temple',
    src: 'audio/track03.mp3',
    cover: 'images/cover03.jpg',
  },
  {
    id: 4,
    title: 'Track 04',
    artist: 'Seonamsa Temple',
    src: 'audio/track04.mp3',
    cover: 'images/cover04.jpg',
  },
  {
    id: 5,
    title: 'Track 05',
    artist: 'Seonamsa Temple',
    src: 'audio/track05.mp3',
    cover: 'images/cover05.jpg',
  },
];

// ──────────────────────────────────────────────
// DOM 참조
// ──────────────────────────────────────────────
const audio          = document.getElementById('audioPlayer');
const playPauseBtn   = document.getElementById('playPauseBtn');
const playIcon       = document.getElementById('playIcon');
const prevBtn        = document.getElementById('prevBtn');
const nextBtn        = document.getElementById('nextBtn');
const prevTrack      = document.getElementById('prevTrack');
const nextTrack      = document.getElementById('nextTrack');
const shuffleBtn     = document.getElementById('shuffleBtn');
const repeatBtn      = document.getElementById('repeatBtn');
const progressWrap   = document.getElementById('progressWrap');
const progressFill   = document.getElementById('progressFill');
const progressThumb  = document.getElementById('progressThumb');
const timeCurrent    = document.getElementById('timeCurrent');
const timeTotal      = document.getElementById('timeTotal');
const totalDuration  = document.getElementById('totalDuration');
const trackTitle     = document.getElementById('trackTitle');
const trackArtist    = document.getElementById('trackArtist');
const trackNumber    = document.getElementById('trackNumber');
const albumImg       = document.getElementById('albumImg');
const albumFallback  = document.getElementById('albumFallback');
const vinyl          = document.getElementById('vinyl');
const tracklistEl    = document.getElementById('tracklist');

// ──────────────────────────────────────────────
// 상태
// ──────────────────────────────────────────────
let currentIndex  = 0;
let isPlaying     = false;
let isShuffle     = false;
let repeatMode    = 0; // 0=off 1=all 2=one
let isDragging    = false;
let vinylAngle    = 0;
let vinylRAF      = null;
let lastTimestamp  = null;

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

  // 오디오 소스
  audio.src = track.src;
  audio.load();

  // 메타 UI 업데이트
  trackTitle.textContent  = track.title;
  trackArtist.textContent = track.artist;
  trackNumber.textContent = `${pad2(index + 1)} / ${pad2(TRACKS.length)}`;

  // 앨범 커버
  albumImg.src = track.cover;
  albumImg.style.display = 'block';
  albumFallback.style.display = 'flex';
  albumImg.onload = () => { albumFallback.style.display = 'none'; };
  albumImg.onerror = () => { albumImg.style.display = 'none'; albumFallback.style.display = 'flex'; };

  // 진행바 리셋
  updateProgress(0, 0);
  timeCurrent.textContent = '0:00';
  timeTotal.textContent   = '0:00';
  totalDuration.textContent = '0:00';

  // 트랙리스트 하이라이트
  renderTracklist();

  if (autoPlay) {
    playAudio();
  } else {
    pauseAudio();
  }
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
      startVinylSpin();
    }).catch(() => {
      // autoplay blocked
    });
  }
}

function pauseAudio() {
  audio.pause();
  isPlaying = false;
  playIcon.className = 'fas fa-play';
  stopVinylSpin();
}

function togglePlay() {
  if (audio.src && audio.src !== window.location.href) {
    if (isPlaying) pauseAudio(); else playAudio();
  }
}

// ──────────────────────────────────────────────
// 바이닐 회전 애니메이션
// ──────────────────────────────────────────────
function startVinylSpin() {
  vinyl.classList.add('spinning');
}

function stopVinylSpin() {
  vinyl.classList.remove('spinning');
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
// 진행바 업데이트
// ──────────────────────────────────────────────
function updateProgress(current, duration) {
  const pct = duration > 0 ? (current / duration) * 100 : 0;
  progressFill.style.width = `${pct}%`;
  progressThumb.style.left = `${pct}%`;
}

// ──────────────────────────────────────────────
// 진행바 클릭 / 드래그
// ──────────────────────────────────────────────
function seekFromEvent(e) {
  const rect = progressWrap.getBoundingClientRect();
  const clientX = e.touches ? e.touches[0].clientX : e.clientX;
  const ratio = Math.min(Math.max((clientX - rect.left) / rect.width, 0), 1);
  if (!isNaN(audio.duration) && audio.duration > 0) {
    audio.currentTime = ratio * audio.duration;
  }
  updateProgress(ratio * (audio.duration || 0), audio.duration || 0);
}

progressWrap.addEventListener('mousedown', (e) => {
  isDragging = true;
  seekFromEvent(e);
});

progressWrap.addEventListener('touchstart', (e) => {
  isDragging = true;
  seekFromEvent(e);
}, { passive: true });

document.addEventListener('mousemove', (e) => {
  if (isDragging) seekFromEvent(e);
});

document.addEventListener('touchmove', (e) => {
  if (isDragging) seekFromEvent(e);
}, { passive: true });

document.addEventListener('mouseup', () => { isDragging = false; });
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
    // 한 곡 반복
    audio.currentTime = 0;
    playAudio();
  } else {
    goNext();
  }
});

audio.addEventListener('error', () => {
  pauseAudio();
  // 파일 없을 때 UI만 리셋
});

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
    li.setAttribute('aria-label', `${track.title} - ${track.artist}`);

    li.innerHTML = `
      <div class="track-num">
        <span class="num-label">${pad2(i + 1)}</span>
        <div class="playing-indicator">
          <span></span><span></span><span></span>
        </div>
      </div>
      <div class="track-cover-thumb" data-thumb="${i}">
        <img src="${track.cover}" alt="${track.title} 커버" class="thumb-img" data-thumb-img="${i}" />
      </div>
      <div class="track-details">
        <p class="track-name">${track.title}</p>
        <p class="track-meta">${track.artist}</p>
      </div>
      <span class="track-duration" data-idx="${i}">--:--</span>
    `;

    li.addEventListener('click', () => loadTrack(i, true));
    li.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') loadTrack(i, true);
    });

    tracklistEl.appendChild(li);
  });

  // 재생 중 표시 - num-label 숨기고 equalizer 보이기
  const items = tracklistEl.querySelectorAll('.track-item');
  items.forEach((item, i) => {
    const numLabel = item.querySelector('.num-label');
    const indicator = item.querySelector('.playing-indicator');
    if (i === currentIndex) {
      numLabel.style.display = 'none';
      indicator.style.display = 'flex';
    } else {
      numLabel.style.display = 'block';
      indicator.style.display = 'none';
    }
  });

  // 썸네일 이미지 에러 처리
  tracklistEl.querySelectorAll('.thumb-img').forEach(img => {
    img.addEventListener('error', function() {
      const wrapper = this.closest('[data-thumb]');
      if (wrapper) wrapper.innerHTML = '<span style="font-size:1.1rem;color:rgba(255,255,255,0.5)">♪</span>';
    });
  });

  // 오프스크린 트랙 길이 읽기
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
      const durationEl = tracklistEl.querySelector(`[data-idx="${i}"]`);
      if (durationEl) {
        durationEl.textContent = formatTime(tempAudio.duration);
      }
    });
  });
}

// ──────────────────────────────────────────────
// 셔플 / 반복 토글
// ──────────────────────────────────────────────
function toggleShuffle() {
  isShuffle = !isShuffle;
  shuffleBtn.classList.toggle('active', isShuffle);
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
    repeatBtn.innerHTML = '<i class="fas fa-redo-alt"></i><sup style="font-size:0.55rem;position:relative;top:-4px;left:-2px;color:#90d4ff">1</sup>';
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
  // 첫 트랙 로드 (자동재생 안 함)
  loadTrack(0, false);
}

init();
