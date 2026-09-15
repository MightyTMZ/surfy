const stage = document.querySelector('#stage');
const snapButton = document.querySelector('#snapButton');
const particles = document.querySelector('#particles');
const impactPoint = document.querySelector('#impactPoint');

let snapping = false;
let resetTimer;
const impactDelay = 0.56;

function positionImpact() {
  const svg = impactPoint.ownerSVGElement;
  const matrix = impactPoint.getScreenCTM();
  if (!matrix) return;

  const point = svg.createSVGPoint();
  point.x = Number(impactPoint.getAttribute('cx'));
  point.y = Number(impactPoint.getAttribute('cy'));
  const screenPoint = point.matrixTransform(matrix);
  stage.style.setProperty('--impact-x', `${screenPoint.x}px`);
  stage.style.setProperty('--impact-y', `${screenPoint.y}px`);
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
  positionImpact();
  makeParticles();
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
window.addEventListener('resize', positionImpact);
positionImpact();
window.addEventListener('keydown', (event) => {
  if (event.code === 'Space') {
    event.preventDefault();
    snap();
  }
});

// Auto-play when triggered by webcam snap detection
if (autoplay) {
  window.setTimeout(snap, 500);
}
