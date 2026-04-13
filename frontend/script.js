const screens = [...document.querySelectorAll('.screen')];
const progressRow = document.getElementById('progressRow');
const questionCard = document.getElementById('questionCard');
const prevQuestionBtn = document.getElementById('prevQuestion');
const nextQuestionBtn = document.getElementById('nextQuestion');
const thumbSlots = [...document.querySelectorAll('.thumb-slot img')];
const video = document.getElementById('video');
const shotCanvas = document.getElementById('shotCanvas');
const cameraStatus = document.getElementById('cameraStatus');
const countdownBadge = document.getElementById('countdownBadge');
const flashLayer = document.getElementById('flashLayer');
const layoutGrid = document.getElementById('layoutGrid');
const backendStatus = document.getElementById('backendStatus');
const top5Grid = document.getElementById('top5Grid');

const BACKEND_URL = 'http://127.0.0.1:5000/process-survey';
const STRIP_EXPORT_WIDTH = 320;
const STRIP_EXPORT_HEIGHT = 980;

const questions = [
  {
    id: 'q1',
    backendKey: 'social_battery',
    theme: 'pink',
    prompt: '1. VIBE CHECK: What is your current “social battery” percentage?',
    type: 'choice',
    options: [{ label: '25%' }, { label: '50%' }, { label: '75%' }, { label: '100%' }]
  },
  {
    id: 'q2',
    backendKey: 'genre',
    theme: 'yellow',
    prompt: '2. What is your top musical genre?',
    type: 'choice',
    gridClass: 'genre-grid',
    options: [
      'Pop',
      'RnB',
      'HipHop',
      'OPM',
      'KPop',
      'Rock',
      'Metal',
      'Indie',
      'Jazz',
      'Acoustic'
    ].map(label => ({ label }))
  },
  {
    id: 'q3',
    backendKey: 'instrument',
    theme: 'blue',
    prompt: '3. If you were to be an instrument, what would you be?',
    type: 'choice',
    options: [{ label: 'Drums' }, { label: 'Guitar' }, { label: 'Piano' }, { label: 'Saxophone' }]
  },
  {
    id: 'q4',
    backendKey: 'stress_response',
    theme: 'pink',
    prompt: '4. You just finished a long, stressful day. What’s your next move?',
    type: 'choice',
    options: [
      { label: 'Blast loud music to release everything' },
      { label: 'Play something groovy and distracting' },
      { label: 'Lie down with soft background music' },
      { label: 'Sit in silence' }
    ]
  },
  {
    id: 'q5',
    backendKey: 'life_scene',
    theme: 'yellow',
    prompt: '5. If your life were a movie right now, what scene is it?',
    type: 'choice',
    options: [
      { label: 'A happy montage (everything is going right)' },
      { label: 'A calm “in-between” scene' },
      { label: 'A sad, reflective moment' },
      { label: 'The emotional climax' }
    ]
  },
  {
    id: 'q6',
    backendKey: 'aux_control',
    theme: 'blue',
    prompt: '6. Someone gives you the aux control at a party. You play?',
    type: 'choice',
    options: [
      { label: 'Something that makes EVERYONE jump' },
      { label: 'A catchy beat people can groove to' },
      { label: 'Chill vibes for background mood' },
      { label: 'Something lowkey… not trying to stand out' }
    ]
  },
  {
    id: 'q7',
    backendKey: 'cant_sleep',
    theme: 'pink',
    prompt: '7. It’s late... you can’t sleep. What do you put on?',
    type: 'choice',
    options: [
      { label: 'Something upbeat to distract yourself' },
      { label: 'Soft chill music' },
      { label: 'Sad songs that match your mood' },
      { label: 'Ambient and instrumental' }
    ]
  },
  {
    id: 'q8',
    backendKey: 'game_pace',
    theme: 'yellow',
    prompt: '8. Choose your game pace:',
    type: 'choice',
    options: [
      { label: 'Fast-paced action, no breaks' },
      { label: 'Balanced gameplay' },
      { label: 'Slow and strategic' },
      { label: 'Something super chill' }
    ]
  },
  {
    id: 'q9',
    backendKey: 'walking_pace',
    theme: 'blue',
    prompt: '9. You’re walking to class and you’re late...',
    type: 'choice',
    options: [
      { label: 'Speed walking / almost running' },
      { label: 'Walking fast but controlled' },
      { label: 'Still walking normally' },
      { label: 'Accepting your fate, slow walk' }
    ]
  },
  {
    id: 'q10',
    backendKey: 'beat_reaction',
    theme: 'pink',
    prompt: '10. A really catchy beat drops... What do you do?',
    type: 'choice',
    options: [
      { label: 'Instantly start dancing' },
      { label: 'Nod your head / groove a little' },
      { label: 'Just listen and vibe' },
      { label: 'Stay completely still' }
    ]
  },
  {
    id: 'q11',
    backendKey: 'music_era',
    theme: 'yellow',
    prompt: '11. If you were to live again in a certain era of music, what year would it be?',
    type: 'choice',
    options: [{ label: '1980s' }, { label: '1990s' }, { label: '2000s' }, { label: '2010s' }]
  },
  {
    id: 'q12',
    backendKey: 'weather',
    theme: 'blue',
    prompt: '12. If you were a weather today, which would you be?',
    type: 'choice',
    options: [{ label: 'Sunny' }, { label: 'Partly Sunny' }, { label: 'Cloudy' }, { label: 'Rainy' }]
  },
  {
    id: 'q13',
    backendKey: 'tiktok_reaction',
    theme: 'pink',
    prompt: '13. A trending TikTok song plays, what would you do?',
    type: 'choice',
    options: [{ label: 'Learn the dance' }, { label: 'Try a little' }, { label: 'Just watching it' }, { label: 'Ignore' }]
  },
  {
    id: 'q14',
    backendKey: 'morning_routine',
    theme: 'yellow',
    prompt: '14. You wake up and have an unexpected extra hour in the morning. How do you start your day?',
    type: 'choice',
    options: [
      { label: 'Sprint through a workout' },
      { label: 'Do a moderate routine' },
      { label: 'Stretch slowly or meditate' },
      { label: 'Stay in bed scrolling' }
    ]
  },
  {
    id: 'q15',
    backendKey: 'roadtrip_vibe',
    theme: 'blue',
    prompt: '15. Music is playing during a fun road trip. What would you do?',
    type: 'choice',
    options: [
      { label: 'Singing and dancing in your seat' },
      { label: 'Vibing and tapping along' },
      { label: 'Relaxed, just enjoying' },
      { label: 'Quiet and not reacting much' }
    ]
  }
];

const layouts = [
  {
    id: 'monami',
    label: 'Monami Strawberry',
    previewSrc: 'assets/monami-frame.png',
    frameSrc: 'assets/monami-frame.png',
    useOverlayFrame: true,
    colors: { border: '#ea567c', panel: '#ffd6e3', accent: '#ee6b95', text: '#bc365f', bg: '#fff6fb' }
  },
  {
    id: 'butterball',
    label: "Peter's Butter Ball",
    previewSrc: 'assets/butterball-frame.png',
    frameSrc: 'assets/butterball-frame.png',
    useOverlayFrame: true,
    colors: { border: '#b79c2b', panel: '#faefba', accent: '#d6bb52', text: '#8a6d00', bg: '#fffdf4' }
  },
  {
    id: 'snoopy',
    label: 'Snoopy Mint',
    previewSrc: 'assets/snoopy-frame.png',
    frameSrc: 'assets/snoopy-frame.png',
    useOverlayFrame: true,
    colors: { border: '#5ab7bb', panel: '#d5f0f1', accent: '#8fd7d5', text: '#2f767a', bg: '#f6ffff' }
  },
  {
    id: 'bubble',
    label: 'Bubble Dough',
    previewSrc: 'assets/bubble-frame.png',
    frameSrc: 'assets/bubble-frame.png',
    useOverlayFrame: true,
    colors: { border: '#e25f76', panel: '#ffd9df', accent: '#ff7f96', text: '#c53c56', bg: '#fff8fa' }
  }
];

const layoutRenderMap = {
  monami: {
    slots: [
      { x: 52, y: 177, w: 216, h: 118, r: 12 },
      { x: 52, y: 375, w: 216, h: 118, r: 12 },
      { x: 52, y: 573, w: 216, h: 118, r: 12 },
      { x: 52, y: 771, w: 216, h: 118, r: 12 }
    ],
    title: { x: 160, y: 915, maxWidth: 120, lineHeight: 10, font: 'bold 8px "Space Mono", monospace' },
    artist: { x: 160, y: 932, maxWidth: 120, lineHeight: 9, font: 'bold 7px "DM Sans", sans-serif' }
  },
  butterball: {
    slots: [
      { x: 56, y: 206, w: 208, h: 110, r: 10 },
      { x: 56, y: 404, w: 208, h: 110, r: 10 },
      { x: 56, y: 602, w: 208, h: 110, r: 10 },
      { x: 56, y: 800, w: 208, h: 110, r: 10 }
    ],
    title: { x: 160, y: 920, maxWidth: 100, lineHeight: 9, font: 'bold 7px "Space Mono", monospace' },
    artist: { x: 160, y: 938, maxWidth: 100, lineHeight: 8, font: 'bold 6px "DM Sans", sans-serif' }
  },
  snoopy: {
    slots: [
      { x: 48, y: 182, w: 224, h: 116, r: 10 },
      { x: 48, y: 380, w: 224, h: 116, r: 10 },
      { x: 48, y: 578, w: 224, h: 116, r: 10 },
      { x: 48, y: 776, w: 224, h: 116, r: 10 }
    ],
    title: { x: 160, y: 920, maxWidth: 120, lineHeight: 10, font: 'bold 8px "Space Mono", monospace' },
    artist: { x: 160, y: 937, maxWidth: 120, lineHeight: 9, font: 'bold 7px "DM Sans", sans-serif' }
  },
  bubble: {
    slots: [
      { x: 46, y: 183, w: 228, h: 116, r: 10 },
      { x: 46, y: 381, w: 228, h: 116, r: 10 },
      { x: 46, y: 579, w: 228, h: 116, r: 10 },
      { x: 46, y: 777, w: 228, h: 116, r: 10 }
    ],
    title: { x: 160, y: 920, maxWidth: 120, lineHeight: 10, font: 'bold 8px "Space Mono", monospace' },
    artist: { x: 160, y: 937, maxWidth: 120, lineHeight: 9, font: 'bold 7px "DM Sans", sans-serif' }
  }
};

let currentQuestionIndex = 0;
const answers = {};
let stream = null;
let capturedShots = [];
let selectedLayout = layouts[3];
let finalSong = null;
let finalStripDataUrl = '';
let isCapturing = false;
let topMatches = [];

function showScreen(id) {
  screens.forEach(screen => screen.classList.toggle('active', screen.id === id));
}

document.querySelectorAll('[data-next]').forEach(btn => {
  btn.addEventListener('click', () => showScreen(btn.dataset.next));
});

document.getElementById('startQuizBtn')?.addEventListener('click', () => {
  showScreen('screen-quiz');
  renderQuiz();
});

document.getElementById('backToLayoutsBtn')?.addEventListener('click', () => {
  showScreen('screen-layout');
});

function renderProgress() {
  progressRow.innerHTML = '';
  questions.forEach((_, idx) => {
    const chip = document.createElement('div');
    chip.className = 'progress-chip';
    if (idx === currentQuestionIndex) chip.classList.add('active');
    if (answers[questions[idx].id] !== undefined) chip.classList.add('done');
    progressRow.appendChild(chip);
  });
}

function renderQuiz() {
  renderProgress();

  const q = questions[currentQuestionIndex];
  questionCard.className = `question-card ${q.theme}`;
  const title = `<h3 class="question-title">${q.prompt}</h3>`;
  const gridClass = q.gridClass || 'options-grid';
  const selected = answers[q.id];

  const optionsHtml = q.options.map((opt, idx) => `
    <button class="option-btn ${selected === idx ? 'selected' : ''}" data-option="${idx}">
      ${opt.label}
    </button>
  `).join('');

  questionCard.innerHTML = `${title}<div class="${gridClass}">${optionsHtml}</div>`;

  questionCard.querySelectorAll('.option-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      answers[q.id] = Number(btn.dataset.option);
      if (currentQuestionIndex < questions.length - 1) {
        currentQuestionIndex += 1;
      }
      renderQuiz();
    });
  });

  prevQuestionBtn.disabled = currentQuestionIndex === 0;
  nextQuestionBtn.disabled = currentQuestionIndex === questions.length - 1 && answers[q.id] === undefined;
}

prevQuestionBtn?.addEventListener('click', () => {
  if (currentQuestionIndex > 0) {
    currentQuestionIndex -= 1;
    renderQuiz();
  }
});

nextQuestionBtn?.addEventListener('click', () => {
  const q = questions[currentQuestionIndex];
  if (answers[q.id] === undefined) return;

  if (currentQuestionIndex < questions.length - 1) {
    currentQuestionIndex += 1;
    renderQuiz();
  } else {
    showScreen('screen-ready');
  }
});

document.getElementById('readyCaptureBtn')?.addEventListener('click', async () => {
  showScreen('screen-camera');
  await openCamera();
});

document.getElementById('openCameraBtn')?.addEventListener('click', openCamera);

document.getElementById('captureSequenceBtn')?.addEventListener('click', async () => {
  if (isCapturing) return;
  isCapturing = true;

  try {
    if (!stream) await openCamera();

    capturedShots = [];
    thumbSlots.forEach(img => img.removeAttribute('src'));
    cameraStatus.textContent = 'Get ready...';

    await runCaptureSequence();
    stopCamera();
    renderLayouts();
    backendStatus.textContent = 'Pick a layout. Then the frontend will get your top matches.';
    showScreen('screen-layout');
  } catch (error) {
    console.error('Capture error:', error);
    alert('Camera capture failed. Try again.');
  }

  isCapturing = false;
});

async function openCamera() {
  try {
    stopCamera();

    stream = await navigator.mediaDevices.getUserMedia({
      video: {
        facingMode: 'user',
        width: { ideal: 1280 },
        height: { ideal: 960 }
      },
      audio: false
    });

    video.srcObject = stream;
    await video.play();
    cameraStatus.textContent = 'Camera ready.';
  } catch (error) {
    cameraStatus.textContent = 'Camera access blocked. Allow camera access, then try again.';
    console.error(error);
    throw error;
  }
}

function stopCamera() {
  if (stream) {
    stream.getTracks().forEach(track => track.stop());
    stream = null;
  }
  if (video) video.srcObject = null;
}

function wait(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function runCaptureSequence() {
  for (let i = 0; i < 4; i++) {
    const countdownTime = i === 0 ? 10 : 6;

    countdownBadge.classList.remove('hidden');

    for (let c = countdownTime; c >= 1; c--) {
      countdownBadge.textContent = c;
      cameraStatus.textContent =
        i === 0
          ? `First shot in ${c}s`
          : `Shot ${i + 1} of 4 in ${c}s`;

      await wait(1000);
    }

    triggerFlash();
    captureShot(i);
    cameraStatus.textContent = `Captured shot ${i + 1} of 4`;
    await wait(700);
  }

  countdownBadge.classList.add('hidden');
}

function triggerFlash() {
  flashLayer.classList.remove('hidden');
  setTimeout(() => flashLayer.classList.add('hidden'), 120);
}

function captureShot(index) {
  shotCanvas.width = video.videoWidth || 720;
  shotCanvas.height = video.videoHeight || 960;

  const ctx = shotCanvas.getContext('2d');
  ctx.drawImage(video, 0, 0, shotCanvas.width, shotCanvas.height);

  const dataUrl = shotCanvas.toDataURL('image/png');
  capturedShots.push(dataUrl);

  if (thumbSlots[index]) {
    thumbSlots[index].src = dataUrl;
  }
}

function renderLayouts() {
  layoutGrid.innerHTML = layouts.map(layout => `
    <div class="layout-card ${selectedLayout.id === layout.id ? 'active' : ''}" data-layout="${layout.id}">
      <img src="${layout.previewSrc}" alt="${layout.label} layout preview">
      <strong>${layout.label}</strong>
    </div>
  `).join('');

  layoutGrid.querySelectorAll('.layout-card').forEach(card => {
  card.addEventListener('click', async () => {
    selectedLayout = layouts.find(layout => layout.id === card.dataset.layout);

    layoutGrid.querySelectorAll('.layout-card').forEach(c => c.classList.remove('active'));
    card.classList.add('active');

    backendStatus.textContent = 'Calling backend...';
    card.insertAdjacentHTML('beforeend', '<div class="mini-loading">Getting your top matches...</div>');

    try {
      const res = await processSurveyWithBackend();

      // 🔥 FORCE ARRAY SAFETY (THIS FIXES YOUR ERROR)
      const safeMatches = Array.isArray(res?.results) ? res.results : [];

      if (!safeMatches.length) {
        throw new Error('No matches returned from backend.');
      }

      topMatches = safeMatches;

      renderTop5(topMatches);
      showScreen('screen-top5');

    } catch (error) {
      console.error(error);
      backendStatus.textContent = 'Backend or matching failed. Check console.';
      alert(error.message || 'Failed to get top matches.');
    } finally {
      renderLayouts();
    }
  });
});
}

function renderTop5(matches = []) {
  if (!Array.isArray(matches)) matches = [];
  top5Grid.innerHTML = matches.map(song => `
    <div class="top5-card" data-rank="${song.rank}">
      <div class="top5-rank">${song.rank}</div>
      <img
        class="top5-cover"
        src="${song.albumArt || 'https://via.placeholder.com/84?text=Song'}"
        alt="${song.title} cover"
      />
      <div class="top5-meta">
        <div class="top5-title">${song.title}</div>
        <div class="top5-artist">${song.artist}</div>
        <div class="top5-percent">${Math.round(song.match)}% match</div>
      </div>
      <button class="top5-pick" type="button">CHOOSE</button>
    </div>
  `).join('');

  top5Grid.querySelectorAll('.top5-card').forEach(card => {
    card.addEventListener('click', async () => {
      const chosenRank = Number(card.dataset.rank);
      const chosenSong = matches.find(song => song.rank === chosenRank);
      if (!chosenSong) return;

      finalSong = {
        title: chosenSong.title,
        artist: chosenSong.artist
      };

      finalStripDataUrl = await generateStrip(capturedShots, selectedLayout, finalSong);

      await populateResult();
      showScreen('screen-result');
    });
  });
}

function buildPayload() {
  return {
    answers: {
      social_battery: getAnswerLabel('q1'),
      instrument: getAnswerLabel('q3'),
      stress_response: getAnswerLabel('q4'),
      life_scene: getAnswerLabel('q5'),
      aux_control: getAnswerLabel('q6'),
      cant_sleep: getAnswerLabel('q7'),
      game_pace: getAnswerLabel('q8'),
      walking_pace: getAnswerLabel('q9'),
      beat_reaction: getAnswerLabel('q10'),
      music_era: getAnswerLabel('q11'),
      weather: getAnswerLabel('q12'),
      tiktok_reaction: getAnswerLabel('q13'),
      morning_routine: getAnswerLabel('q14'),
      roadtrip_vibe: getAnswerLabel('q15')
    },
    genre: normalizeGenre(getAnswerLabel('q2'))
  };
}

function getAnswerLabel(questionId) {
  const question = questions.find(q => q.id === questionId);
  const selectedIndex = answers[questionId];
  if (!question || selectedIndex === undefined) return '';
  return question.options[selectedIndex].label;
}

function normalizeGenre(label) {
  if (!label) return '';

  const genreMap = {
    Pop: 'pop',
    RnB: 'rnb',
    HipHop: 'hiphop',
    OPM: 'opm',
    KPop: 'kpop',
    Rock: 'rock',
    Metal: 'metal',
    Indie: 'indie',
    Jazz: 'jazz',
    Acoustic: 'acoustic'
  };

  return genreMap[label] || label.toLowerCase();
}

function processSurveyWithBackend() {
  const payload = buildPayload();

  payload.strip = finalStripDataUrl || null;

  return fetch(BACKEND_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
  .then(async (response) => {
    let data;

    try {
      data = await response.json();
    } catch {
      throw new Error('Backend did not return valid JSON.');
    }

    console.log('Backend response:', data);

    if (!response.ok) {
      throw new Error(data.message || 'Backend request failed.');
    }

    let results = [];

    if (Array.isArray(data.results) && data.results.length > 0) {
      results = data.results;
    } else {
      const title = data.title || data.song_title || data.songTitle;
      const artist = data.artist || data.song_artist || data.songArtist;

      if (title && artist) {
        results = [{ title, artist, match: 100 }];
      } else {
        throw new Error('Backend JSON is missing usable song data.');
      }
    }
processSurveyWithBackend.lastDownloadUrl = data.download_url || null;
    return {
      results: results.slice(0, 5).map((song, index) => ({
        rank: index + 1,
        title: song.title || 'Unknown Title',
        artist: song.artist || 'Unknown Artist',
        match: Number(song.match ?? song.score ?? song.percentage ?? (100 - index * 5)),
        albumArt: song.albumArt || song.album_art || song.image || song.cover || ''
      })),

      // ✅ THIS IS WHAT FIXES YOUR QR FLOW
      download_url: data.download_url || null
    };
  });
}

function loadImage(src) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve(img);
    img.onerror = () => reject(new Error(`Failed to load image: ${src}`));
    img.src = src;
  });
}

async function getAutoLayoutConfig(layout) {
  if (!layout.frameSrc) throw new Error("Missing frame source");

  const { holes, frameWidth, frameHeight } =
    await detectPhotoSlotsFromFrame(layout.frameSrc);

  const scaleX = STRIP_EXPORT_WIDTH / frameWidth;
  const scaleY = STRIP_EXPORT_HEIGHT / frameHeight;

  const slots = holes.slice(0, 4).map(h => ({
    x: h.x * scaleX,
    y: h.y * scaleY,
    w: h.w * scaleX,
    h: h.h * scaleY,
    r: 12
  }));

  return {
    slots,
    title: {
      x: STRIP_EXPORT_WIDTH / 2,
      y: STRIP_EXPORT_HEIGHT - 70,
      maxWidth: 140,
      lineHeight: 10,
      font: 'bold 8px "Space Mono", monospace'
    },
    artist: {
      x: STRIP_EXPORT_WIDTH / 2,
      y: STRIP_EXPORT_HEIGHT - 50,
      maxWidth: 140,
      lineHeight: 9,
      font: 'bold 7px "DM Sans", sans-serif'
    }
  };
}

async function generateStrip(shots, layout, song) {
  if (!shots.length) throw new Error('No captured shots found.');

  const canvas = document.createElement('canvas');
  canvas.width = STRIP_EXPORT_WIDTH;
  canvas.height = STRIP_EXPORT_HEIGHT;

  const ctx = canvas.getContext('2d');

  ctx.imageSmoothingEnabled = true;
  ctx.imageSmoothingQuality = "high";

  let overlayImage = null;

  if (layout.useOverlayFrame && layout.frameSrc) {
    try {
      overlayImage = await loadImage(layout.frameSrc);
    } catch (e) {
      console.warn("Frame load failed", e);
    }
  }

  // 🔥 USE NEW CONFIG WITH SCALING
  const config = await getAutoLayoutConfig(layout);

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // draw photos
  for (let i = 0; i < Math.min(4, shots.length, config.slots.length); i++) {
    const img = await loadImage(shots[i]);
    drawCoverImage(ctx, img, config.slots[i]);
  }

  // draw frame ON TOP
  if (overlayImage) {
    ctx.drawImage(overlayImage, 0, 0, canvas.width, canvas.height);
  }

  // draw text
  ctx.save();
  ctx.fillStyle = '#7d2b2d';
  ctx.textAlign = 'center';

  ctx.font = config.title.font;
  wrapText(ctx, song.title, config.title.x, config.title.y, config.title.maxWidth, config.title.lineHeight, 2);

  ctx.font = config.artist.font;
  wrapText(ctx, song.artist, config.artist.x, config.artist.y, config.artist.maxWidth, config.artist.lineHeight, 1);

  ctx.restore();

  return canvas.toDataURL('image/png');
}

function drawStripBase(ctx, canvas, layout) {
  const config = getLayoutRenderConfig(layout.id);

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // ❌ REMOVE white slot background completely
  // (this was blocking your frame holes)

  // optional debug bg (safe to remove)
  ctx.fillStyle = 'transparent';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
}

const DEBUG_SLOTS = false;

function drawCoverImage(ctx, img, slot) {
  ctx.save();

  ctx.imageSmoothingEnabled = true;
  ctx.imageSmoothingQuality = "high";

  // clip to hole
  roundedRect(ctx, slot.x, slot.y, slot.w, slot.h, slot.r || 12);
  ctx.clip();

  const imgRatio = img.width / img.height;
  const slotRatio = slot.w / slot.h;

  let drawW, drawH;

  // 🔥 balanced cover fit (no ugly zoom)
  if (imgRatio > slotRatio) {
    drawH = slot.h;
    drawW = drawH * imgRatio;
  } else {
    drawW = slot.w;
    drawH = drawW / imgRatio;
  }

  const dx = slot.x + (slot.w - drawW) / 2;
  const dy = slot.y + (slot.h - drawH) / 2;

  ctx.drawImage(img, dx, dy, drawW, drawH);

  // 🔥 DEBUG MODE (toggle true)
  if (DEBUG_SLOTS) {
    ctx.strokeStyle = 'red';
    ctx.lineWidth = 2;
    ctx.strokeRect(slot.x, slot.y, slot.w, slot.h);
  }

  ctx.restore();
}

function roundedRect(ctx, x, y, width, height, radius) {
  ctx.beginPath();
  ctx.moveTo(x + radius, y);
  ctx.arcTo(x + width, y, x + width, y + height, radius);
  ctx.arcTo(x + width, y + height, x, y + height, radius);
  ctx.arcTo(x, y + height, x, y, radius);
  ctx.arcTo(x, y, x + width, y, radius);
  ctx.closePath();
}

function wrapText(ctx, text, x, y, maxWidth, lineHeight, maxLines = 2) {
  const words = String(text).trim().split(/\s+/);
  const lines = [];
  let current = '';

  for (const word of words) {
    const test = current ? `${current} ${word}` : word;
    if (ctx.measureText(test).width <= maxWidth) {
      current = test;
    } else {
      if (current) lines.push(current);
      current = word;
    }
  }

  if (current) lines.push(current);

  let finalLines = lines.slice(0, maxLines);

  if (lines.length > maxLines && finalLines.length > 0) {
    let last = finalLines[finalLines.length - 1];
    while (last.length > 0 && ctx.measureText(`${last}...`).width > maxWidth) {
      last = last.slice(0, -1).trim();
    }
    finalLines[finalLines.length - 1] = `${last}...`;
  }

  finalLines.forEach((line, index) => {
    ctx.fillText(line, x, y + index * lineHeight);
  });
}

function dataURLtoBlob(dataUrl) {
  const arr = dataUrl.split(',');
  const mime = arr[0].match(/:(.*?);/)[1];
  const bstr = atob(arr[1]);
  let n = bstr.length;
  const u8arr = new Uint8Array(n);

  while (n--) {
    u8arr[n] = bstr.charCodeAt(n);
  }

  return new Blob([u8arr], { type: mime });
}

async function detectPhotoSlotsFromFrame(frameSrc) {
  const img = await loadImage(frameSrc);

  const tempCanvas = document.createElement('canvas');
  tempCanvas.width = img.width;
  tempCanvas.height = img.height;

  const ctx = tempCanvas.getContext('2d');
  ctx.drawImage(img, 0, 0);

  const imageData = ctx.getImageData(0, 0, img.width, img.height);
  const data = imageData.data;

  const visited = new Uint8Array(img.width * img.height);
  const holes = [];

  const isTransparent = (i) => data[i + 3] < 20;

  function floodFill(startX, startY) {
    const stack = [[startX, startY]];
    let minX = startX, maxX = startX;
    let minY = startY, maxY = startY;

    while (stack.length) {
      const [x, y] = stack.pop();
      const idx = y * img.width + x;

      if (visited[idx]) continue;
      visited[idx] = 1;

      const pixelIndex = idx * 4;
      if (!isTransparent(pixelIndex)) continue;

      minX = Math.min(minX, x);
      maxX = Math.max(maxX, x);
      minY = Math.min(minY, y);
      maxY = Math.max(maxY, y);

      if (x > 0) stack.push([x - 1, y]);
      if (x < img.width - 1) stack.push([x + 1, y]);
      if (y > 0) stack.push([x, y - 1]);
      if (y < img.height - 1) stack.push([x, y + 1]);
    }

    return {
      x: minX,
      y: minY,
      w: maxX - minX,
      h: maxY - minY
    };
  }

  for (let y = 0; y < img.height; y++) {
    for (let x = 0; x < img.width; x++) {
      const idx = y * img.width + x;

      if (visited[idx]) continue;

      const pixelIndex = idx * 4;

      if (isTransparent(pixelIndex)) {
        const hole = floodFill(x, y);

        // ignore tiny noise
        if (hole.w > 50 && hole.h > 50) {
          holes.push(hole);
        }
      }
    }
  }

  // sort top → bottom
  holes.sort((a, b) => (b.w * b.h) - (a.w * a.h));
holes.shift(); // remove largest

// ✅ now sort real slots top → bottom
holes.sort((a, b) => a.y - b.y);

  return {
    holes,
    frameWidth: img.width,
    frameHeight: img.height
  };
}

async function uploadToCloudinary(dataUrl) {
  const cloudName = "deugdxahz";
  const uploadPreset = "photobooth_upload";

  const formData = new FormData();

  const blob = dataURLtoBlob(dataUrl);
  formData.append("file", blob);
  formData.append("upload_preset", uploadPreset);

  const res = await fetch(
    `https://api.cloudinary.com/v1_1/${cloudName}/image/upload`,
    {
      method: "POST",
      body: formData
    }
  );

  const data = await res.json();

  if (!data.secure_url) {
    throw new Error("Upload failed");
  }

  return data.secure_url;
}

async function populateResult() {
  document.getElementById('songTitle').textContent = finalSong.title;
  document.getElementById('songArtist').textContent = `by ${finalSong.artist}`;
  document.getElementById('finalStrip').src = finalStripDataUrl;

  const downloadLink = document.getElementById('downloadLink');
  downloadLink.href = finalStripDataUrl;

  const qrImage = document.getElementById('qrImage');

  try {
    qrImage.alt = "Uploading image...";

    const imageUrl = await uploadToCloudinary(finalStripDataUrl);

    // store for debugging / future use
    processSurveyWithBackend.lastDownloadUrl = imageUrl;

    qrImage.src =
      `https://api.qrserver.com/v1/create-qr-code/?size=240x240&data=${encodeURIComponent(imageUrl)}`;

  } catch (err) {
    console.error(err);

    // fallback QR (still works, but not cross-device)
    const blob = dataURLtoBlob(finalStripDataUrl);
    const blobUrl = URL.createObjectURL(blob);

    qrImage.src =
      `https://api.qrserver.com/v1/create-qr-code/?size=240x240&data=${encodeURIComponent(blobUrl)}`;

    alert("Cloud upload failed. Using temporary QR only.");
  }
}

document.getElementById('printBtn')?.addEventListener('click', () => {
  const stripSrc = document.getElementById('finalStrip').src;

  if (!stripSrc) {
    alert('No photostrip available to print yet.');
    return;
  }

  const printWindow = window.open('', '_blank', 'width=500,height=1200');
  if (!printWindow) return;

  printWindow.document.write(`
    <!DOCTYPE html>
    <html>
    <head>
      <title>Print Photostrip</title>
      <style>
        @page { size: auto; margin: 0; }
        html, body { margin: 0; padding: 0; background: white; text-align: center; }
        .print-wrap {
          width: 100%;
          display: flex;
          justify-content: center;
          align-items: flex-start;
          padding: 12px 0;
        }
        img {
          width: 300px;
          max-width: 100%;
          height: auto;
          display: block;
        }
      </style>
    </head>
    <body>
      <div class="print-wrap"><img src="${stripSrc}" alt="Photostrip" /></div>
      <script>
        window.onload = function () {
          window.focus();
          window.print();
          window.close();
        };
      <\/script>
    </body>
    </html>
  `);
  printWindow.document.close();
});

document.getElementById('restartBtn')?.addEventListener('click', () => {
  stopCamera();
  capturedShots = [];
  finalSong = null;
  finalStripDataUrl = '';
  topMatches = [];
  currentQuestionIndex = 0;

  Object.keys(answers).forEach(key => delete answers[key]);
  thumbSlots.forEach(img => img.removeAttribute('src'));

  backendStatus.textContent = 'Waiting for your layout choice. Final song comes from the backend.';
  showScreen('screen-home');
});

window.addEventListener('beforeunload', stopCamera);
renderQuiz();