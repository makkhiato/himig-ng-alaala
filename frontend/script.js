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

const BACKEND_URL = 'http://localhost:5000/process-survey';

const questions = [
  {
    id: 'q1', backendKey: 'social_battery', theme: 'pink', prompt: '1. VIBE CHECK: What is your current “social battery” percentage?', type: 'choice',
    options: [{ label: '25%' }, { label: '50%' }, { label: '75%' }, { label: '100%' }]
  },
  {
    id: 'q2', backendKey: 'genre', theme: 'yellow', prompt: '2. What is your top musical genre?', type: 'choice', gridClass: 'genre-grid',
    options: ['Pop', 'Hip-Hop', 'OPM', 'K-Pop', 'Indie', 'Rock', 'R&B'].map(label => ({ label }))
  },
  {
    id: 'q3', backendKey: 'instrument', theme: 'blue', prompt: '3. If you were to be an instrument, what would you be?', type: 'choice',
    options: [{ label: 'Drums' }, { label: 'Guitar' }, { label: 'Piano' }, { label: 'Saxophone' }]
  },
  {
    id: 'q4', backendKey: 'stress_response', theme: 'pink', prompt: '4. You just finished a long, stressful day. What’s your next move?', type: 'choice',
    options: [
      { label: 'Blast loud music to release everything' },
      { label: 'Play something groovy and distracting' },
      { label: 'Lie down with soft background music' },
      { label: 'Sit in silence' }
    ]
  },
  {
    id: 'q5', backendKey: 'life_scene', theme: 'yellow', prompt: '5. If your life were a movie right now, what scene is it?', type: 'choice',
    options: [
      { label: 'A happy montage (everything is going right)' },
      { label: 'A calm “in-between” scene' },
      { label: 'A sad, reflective moment' },
      { label: 'The emotional climax' }
    ]
  },
  {
    id: 'q6', backendKey: 'aux_control', theme: 'blue', prompt: '6. Someone gives you the aux control at a party. You play?', type: 'choice',
    options: [
      { label: 'Something that makes EVERYONE jump' },
      { label: 'A catchy beat people can groove to' },
      { label: 'Chill vibes for background mood' },
      { label: 'Something lowkey… not trying to stand out' }
    ]
  },
  {
    id: 'q7', backendKey: 'cant_sleep', theme: 'pink', prompt: '7. It’s late... you can’t sleep. What do you put on?', type: 'choice',
    options: [
      { label: 'Something upbeat to distract yourself' },
      { label: 'Soft chill music' },
      { label: 'Sad songs that match your mood' },
      { label: 'Ambient and instrumental' }
    ]
  },
  {
    id: 'q8', backendKey: 'game_pace', theme: 'yellow', prompt: '8. Choose your game pace:', type: 'choice',
    options: [
      { label: 'Fast-paced action, no breaks' },
      { label: 'Balanced gameplay' },
      { label: 'Slow and strategic' },
      { label: 'Something super chill' }
    ]
  },
  {
    id: 'q9', backendKey: 'walking_pace', theme: 'blue', prompt: '9. You’re walking to class and you’re late...', type: 'choice',
    options: [
      { label: 'Speed walking / almost running' },
      { label: 'Walking fast but controlled' },
      { label: 'Still walking normally' },
      { label: 'Accepting your fate, slow walk' }
    ]
  },
  {
    id: 'q10', backendKey: 'beat_reaction', theme: 'pink', prompt: '10. A really catchy beat drops... What do you do?', type: 'choice',
    options: [
      { label: 'Instantly start dancing' },
      { label: 'Nod your head / groove a little' },
      { label: 'Just listen and vibe' },
      { label: 'Stay completely still' }
    ]
  },
  {
    id: 'q11', backendKey: 'music_era', theme: 'yellow', prompt: '11. If you were to live again in a certain era of music, what year would it be?', type: 'choice',
    options: [{ label: '1980s' }, { label: '1990s' }, { label: '2000s' }, { label: '2010s' }]
  },
  {
    id: 'q12', backendKey: 'weather', theme: 'blue', prompt: '12. If you were a weather today, which would you be?', type: 'choice',
    options: [{ label: 'Sunny' }, { label: 'Partly Sunny' }, { label: 'Cloudy' }, { label: 'Rainy' }]
  },
  {
    id: 'q13', backendKey: 'tiktok_reaction', theme: 'pink', prompt: '13. A trending TikTok song plays, what would you do?', type: 'choice',
    options: [{ label: 'Learn the dance' }, { label: 'Try a little' }, { label: 'Just watching it' }, { label: 'Ignore' }]
  },
  {
    id: 'q14', backendKey: 'morning_routine', theme: 'yellow', prompt: '14. You wake up and have an unexpected extra hour in the morning. How do you start your day?', type: 'choice',
    options: [
      { label: 'Sprint through a workout' },
      { label: 'Do a moderate routine' },
      { label: 'Stretch slowly or meditate' },
      { label: 'Stay in bed scrolling' }
    ]
  },
  {
    id: 'q15', backendKey: 'roadtrip_vibe', theme: 'blue', prompt: '15. Music is playing during a fun road trip. What would you do?', type: 'choice',
    options: [
      { label: 'Singing and dancing in your seat' },
      { label: 'Vibing and tapping along' },
      { label: 'Relaxed, just enjoying' },
      { label: 'Quiet and not reacting much' }
    ]
  }
];

const layouts = [
  { id: 'monami', label: 'Monami Strawberry', src: 'assets/monami.png', colors: { border: '#ea567c', panel: '#ffd6e3', accent: '#ee6b95', text: '#bc365f', bg: '#fff6fb' } },
  { id: 'butterball', label: "Peter's Butter Ball", src: 'assets/butterball.png', colors: { border: '#b79c2b', panel: '#faefba', accent: '#d6bb52', text: '#8a6d00', bg: '#fffdf4' } },
  { id: 'snoopy', label: 'Snoopy Mint', src: 'assets/snoopy.png', colors: { border: '#5ab7bb', panel: '#d5f0f1', accent: '#8fd7d5', text: '#2f767a', bg: '#f6ffff' } },
  { id: 'bubble', label: 'Bubble Dough', src: 'assets/bubble.png', colors: { border: '#e25f76', panel: '#ffd9df', accent: '#ff7f96', text: '#c53c56', bg: '#fff8fa' } }
];

let currentQuestionIndex = 0;
const answers = {};
let stream = null;
let capturedShots = [];
let selectedLayout = layouts[3];
let finalSong = null;
let finalStripDataUrl = '';
let isCapturing = false;

function showScreen(id) {
  screens.forEach(s => s.classList.toggle('active', s.id === id));
}

document.querySelectorAll('[data-next]').forEach(btn => {
  btn.addEventListener('click', () => showScreen(btn.dataset.next));
});

document.getElementById('startQuizBtn').addEventListener('click', () => {
  showScreen('screen-quiz');
  renderQuiz();
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
    <button class="option-btn ${selected === idx ? 'selected' : ''}" data-option="${idx}">${opt.label}</button>
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

prevQuestionBtn.addEventListener('click', () => {
  if (currentQuestionIndex > 0) {
    currentQuestionIndex -= 1;
    renderQuiz();
  }
});

nextQuestionBtn.addEventListener('click', () => {
  const q = questions[currentQuestionIndex];
  if (answers[q.id] === undefined) return;
  if (currentQuestionIndex < questions.length - 1) {
    currentQuestionIndex += 1;
    renderQuiz();
  } else {
    showScreen('screen-ready');
  }
});

document.getElementById('readyCaptureBtn').addEventListener('click', async () => {
  showScreen('screen-camera');
  await openCamera();
});

document.getElementById('openCameraBtn').addEventListener('click', openCamera);

document.getElementById('captureSequenceBtn').addEventListener('click', async () => {
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
    backendStatus.textContent = 'Pick a layout. Then the frontend will call the backend to get the final song.';
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
      video: { facingMode: 'user', width: { ideal: 1280 }, height: { ideal: 960 } },
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
    countdownBadge.classList.remove('hidden');
    for (let c = 10; c >= 1; c--) {
      countdownBadge.textContent = c;
      cameraStatus.textContent = `Shot ${i + 1} of 4 in ${c}s`;
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
  thumbSlots[index].src = dataUrl;
}

function renderLayouts() {
  layoutGrid.innerHTML = layouts.map(layout => `
    <div class="layout-card ${selectedLayout.id === layout.id ? 'active' : ''}" data-layout="${layout.id}">
      <img src="${layout.src}" alt="${layout.label} layout preview">
      <strong>${layout.label}</strong>
    </div>
  `).join('');

  layoutGrid.querySelectorAll('.layout-card').forEach(card => {
    card.addEventListener('click', async () => {
      selectedLayout = layouts.find(l => l.id === card.dataset.layout);
      layoutGrid.querySelectorAll('.layout-card').forEach(c => c.classList.remove('active'));
      card.classList.add('active');
      backendStatus.textContent = 'Calling backend...';
      card.insertAdjacentHTML('beforeend', '<div class="mini-loading">Processing survey...</div>');

      try {
        finalSong = await processSurveyWithBackend();
        finalStripDataUrl = await generateStrip(capturedShots, selectedLayout, finalSong);
        populateResult();
        showScreen('screen-result');
      } catch (error) {
        console.error(error);
        backendStatus.textContent = 'Backend or strip generation failed. Check console.';
        alert(error.message || 'Failed to process survey or create final strip.');
      } finally {
        renderLayouts();
      }
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
    genre: getAnswerLabel('q2')
  };
}

function getAnswerLabel(questionId) {
  const question = questions.find(q => q.id === questionId);
  const selectedIndex = answers[questionId];
  if (!question || selectedIndex === undefined) return '';
  return question.options[selectedIndex].label;
}

async function processSurveyWithBackend() {
  const payload = buildPayload();
  const response = await fetch(BACKEND_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

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

  const title = data.title || data.song_title || data.songTitle;
  const artist = data.artist || data.song_artist || data.songArtist;

  if (!title || !artist) {
    if (data.message === 'Survey processed successfully') {
      return { title: 'Survey processed successfully', artist: 'Waiting for final backend song data' };
    }
    throw new Error('Backend JSON is missing title/artist fields.');
  }

  return { title, artist };
}

function loadImage(src) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve(img);
    img.onerror = () => reject(new Error(`Failed to load image: ${src}`));
    img.src = src;
  });
}

async function generateStrip(shots, layout, song) {
  if (!shots.length) throw new Error('No captured shots found.');

  let overlayImage = null;
  try {
    overlayImage = await loadImage(layout.src);
  } catch (error) {
    console.warn('Layout image failed to load for export, using canvas fallback theme.', error);
  }

  const canvas = document.createElement('canvas');
  canvas.width = overlayImage?.width || 320;
  canvas.height = overlayImage?.height || 980;
  const ctx = canvas.getContext('2d');

  drawStripBase(ctx, canvas, layout);

  const slots = [
    { x: 46, y: 178, w: 228, h: 150 },
    { x: 46, y: 378, w: 228, h: 150 },
    { x: 46, y: 578, w: 228, h: 150 },
    { x: 46, y: 778, w: 228, h: 150 }
  ];

  for (let i = 0; i < Math.min(4, shots.length); i++) {
    const img = await loadImage(shots[i]);
    drawCoverImage(ctx, img, slots[i]);
  }

  if (overlayImage) {
    try {
      ctx.drawImage(overlayImage, 0, 0, canvas.width, canvas.height);
    } catch (error) {
      console.warn('Overlay draw skipped; fallback strip kept.', error);
    }
  }

  ctx.fillStyle = '#7d2b2d';
  ctx.textAlign = 'center';
  ctx.font = 'bold 14px "Space Mono", monospace';
  wrapText(ctx, song.title, canvas.width / 2, canvas.height - 74, 230, 16);
  ctx.font = 'bold 11px "DM Sans", sans-serif';
  ctx.fillText(song.artist, canvas.width / 2, canvas.height - 42, 200);

  return canvas.toDataURL('image/png');
}

function drawStripBase(ctx, canvas, layout) {
  const theme = layout.colors;
  ctx.fillStyle = theme.bg;
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.fillStyle = theme.border;
  roundedRect(ctx, 8, 10, canvas.width - 16, canvas.height - 20, 24);
  ctx.fill();

  ctx.fillStyle = '#ffffff';
  roundedRect(ctx, 17, 20, canvas.width - 34, canvas.height - 40, 20);
  ctx.fill();

  ctx.fillStyle = theme.panel;
  roundedRect(ctx, 48, 32, canvas.width - 96, 46, 12);
  ctx.fill();

  ctx.strokeStyle = theme.border;
  ctx.lineWidth = 3;
  roundedRect(ctx, 17, 20, canvas.width - 34, canvas.height - 40, 20);
  ctx.stroke();
  roundedRect(ctx, 48, 32, canvas.width - 96, 46, 12);
  ctx.stroke();

  ctx.font = 'bold 14px "DM Sans", sans-serif';
  ctx.fillStyle = theme.text;
  ctx.textAlign = 'center';
  ctx.fillText(layout.label.replace(' Strawberry', '').replace(' Mint', ''), canvas.width / 2, 60);

  ctx.fillStyle = '#111';
  ctx.font = 'bold 9px "Space Mono", monospace';
  ctx.fillText('Himig ng Alaala | 2026', canvas.width / 2, canvas.height - 15);
}

function drawCoverImage(ctx, img, slot) {
  const imgRatio = img.width / img.height;
  const slotRatio = slot.w / slot.h;
  let drawW, drawH, offsetX, offsetY;

  if (imgRatio > slotRatio) {
    drawH = slot.h;
    drawW = img.width * (slot.h / img.height);
    offsetX = slot.x - (drawW - slot.w) / 2;
    offsetY = slot.y;
  } else {
    drawW = slot.w;
    drawH = img.height * (slot.w / img.width);
    offsetX = slot.x;
    offsetY = slot.y - (drawH - slot.h) / 2;
  }

  ctx.save();
  roundedRect(ctx, slot.x, slot.y, slot.w, slot.h, 18);
  ctx.clip();
  ctx.drawImage(img, offsetX, offsetY, drawW, drawH);
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

function wrapText(ctx, text, x, y, maxWidth, lineHeight) {
  const words = text.split(' ');
  let line = '';
  let curY = y;
  for (let i = 0; i < words.length; i++) {
    const testLine = `${line}${words[i]} `;
    if (ctx.measureText(testLine).width > maxWidth && i > 0) {
      ctx.fillText(line.trim(), x, curY);
      line = `${words[i]} `;
      curY += lineHeight;
    } else {
      line = testLine;
    }
  }
  ctx.fillText(line.trim(), x, curY);
}

function populateResult() {
  document.getElementById('songTitle').textContent = finalSong.title;
  document.getElementById('songArtist').textContent = `by ${finalSong.artist}`;
  document.getElementById('finalStrip').src = finalStripDataUrl;

  const spotifyUrl = `https://open.spotify.com/search/${encodeURIComponent(`${finalSong.title} ${finalSong.artist}`)}`;
  document.getElementById('spotifyLink').href = spotifyUrl;
  document.getElementById('downloadLink').href = finalStripDataUrl;
  document.getElementById('qrImage').src = `https://api.qrserver.com/v1/create-qr-code/?size=240x240&data=${encodeURIComponent(spotifyUrl)}`;
}

document.getElementById('printBtn').addEventListener('click', () => {
  const stripSrc = document.getElementById('finalStrip').src;
  if (!stripSrc) {
    alert('No photostrip available to print yet.');
    return;
  }

  const printWindow = window.open('', '_blank', 'width=500,height=1200');
  printWindow.document.write(`
    <!DOCTYPE html>
    <html>
    <head>
      <title>Print Photostrip</title>
      <style>
        @page { size: auto; margin: 0; }
        html, body { margin: 0; padding: 0; background: white; text-align: center; }
        .print-wrap { width: 100%; display: flex; justify-content: center; align-items: flex-start; padding: 12px 0; }
        img { width: 300px; max-width: 100%; height: auto; display: block; }
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

document.getElementById('restartBtn').addEventListener('click', () => {
  stopCamera();
  capturedShots = [];
  finalSong = null;
  finalStripDataUrl = '';
  currentQuestionIndex = 0;
  Object.keys(answers).forEach(key => delete answers[key]);
  thumbSlots.forEach(img => img.removeAttribute('src'));
  backendStatus.textContent = 'Waiting for your layout choice. Final song comes from the backend.';
  showScreen('screen-home');
});

window.addEventListener('beforeunload', stopCamera);
renderQuiz();
