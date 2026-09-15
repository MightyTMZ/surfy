const stage = document.querySelector('#stage');
const snapButton = document.querySelector('#snapButton');
const particles = document.querySelector('#particles');
const thumb = document.querySelector('.finger--thumb');
const middleTip = document.querySelector('.middle-tip');

let snapping = false;
let resetTimer;
let fingerAnimationFrame;
const impactDelay = 0.68;

function easeOutCubic(value) {
  return 1 - Math.pow(1 - value, 3);
}

function between(progress, start, end, from, to) {
  const normalized = Math.max(0, Math.min(1, (progress - start) / (end - start)));
  return from + (to - from) * easeOutCubic(normalized);
}

function animateFingers() {
  const startedAt = performance.now();
  const duration = 780;

  function drawFrame(now) {
    const progress = Math.min(1, (now - startedAt) / duration);
    const thumbAngle = progress <= 0.46
      ? between(progress, 0, 0.46, 0, 88)
      : progress <= 0.57 ? 88 : between(progress, 0.57, 1, 88, 76);
    const middleAngle = progress <= 0.46
      ? between(progress, 0, 0.46, 0, -140)
      : progress <= 0.57 ? -140 : between(progress, 0.57, 1, -140, -180);

    thumb.setAttribute('transform', `rotate(${thumbAngle} 180 380)`);
    middleTip.setAttribute('transform', `rotate(${middleAngle} 300 130)`);

    if (progress < 1) fingerAnimationFrame = window.requestAnimationFrame(drawFrame);
  }

  fingerAnimationFrame = window.requestAnimationFrame(drawFrame);
}

function makeParticles() {
  particles.replaceChildren();
  const colors = ['#f4d8ff', '#c77dff', '#8f38d1', '#ffcf60', '#fff6c7'];
  const viewportScale = Math.min(window.innerWidth, window.innerHeight);

  for (let i = 0; i < 84; i += 1) {
    const particle = document.createElement('i');
    const angle = Math.random() * Math.PI * 2;
    const distance = viewportScale * (0.14 + Math.random() * 0.38);
    particle.className = 'particle';
    particle.style.setProperty('--x', `${Math.cos(angle) * distance}px`);
    particle.style.setProperty('--y', `${Math.sin(angle) * distance}px`);
    particle.style.setProperty('--size', `${2 + Math.random() * 5}px`);
    particle.style.setProperty('--duration', `${0.7 + Math.random() * 0.9}s`);
    particle.style.setProperty('--delay', `${impactDelay + Math.random() * 0.18}s`);
    particle.style.setProperty('--color', colors[Math.floor(Math.random() * colors.length)]);
    particles.appendChild(particle);
  }
}

function snap() {
  if (snapping) return;
  snapping = true;
  makeParticles();
  animateFingers();
  stage.classList.add('is-snapping');
  snapButton.disabled = true;

  if ('vibrate' in navigator) navigator.vibrate([35, 30, 70]);

  window.setTimeout(() => {
    stage.classList.add('is-complete');
    showComplete();
    notifyServer();
  }, 1650);
}

function reset() {
  stage.classList.remove('is-snapping', 'is-complete');
  window.cancelAnimationFrame(fingerAnimationFrame);
  thumb.removeAttribute('transform');
  middleTip.removeAttribute('transform');
  snapButton.disabled = false;
  particles.replaceChildren();
  snapping = false;
  window.clearTimeout(resetTimer);
}

// Check for autoplay mode (triggered after webcam snap detection)
const params = new URLSearchParams(window.location.search);
const autoplay = params.get('autoplay') === '1';

function notifyServer() {
  fetch('/snapped', { method: 'POST' }).catch(() => {});
}

function showComplete() {
  const overlay = document.getElementById('completeOverlay');
  if (overlay) {
    window.setTimeout(() => { overlay.classList.add('visible'); }, 600);
  }
}

snapButton.addEventListener('click', snap);
window.addEventListener('keydown', (event) => {
  if (event.code === 'Space') {
    event.preventDefault();
    snap();
  }
});

// Auto-play when triggered by webcam snap detection
if (autoplay) {
  window.requestAnimationFrame(snap);
}
