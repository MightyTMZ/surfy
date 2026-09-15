const stage = document.querySelector('#stage');
const snapButton = document.querySelector('#snapButton');
const snapCta = document.querySelector('#snapCta');
const replayButton = document.querySelector('#replayButton');
const particles = document.querySelector('#particles');
const helper = document.querySelector('#helper');

let snapping = false;
const impactDelay = 0.56;

function makeParticles() {
  particles.replaceChildren();
  const colors = ['#f4d8ff', '#c77dff', '#8f38d1', '#ffcf60', '#fff6c7'];

  for (let i = 0; i < 84; i += 1) {
    const particle = document.createElement('i');
    const angle = Math.random() * Math.PI * 2;
    const distance = 140 + Math.random() * 430;
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
  stage.classList.add('is-snapping');
  snapButton.disabled = true;
  snapCta.disabled = true;
  helper.textContent = 'Reality is shifting…';

  if ('vibrate' in navigator) navigator.vibrate([35, 30, 70]);

  window.setTimeout(() => stage.classList.add('is-complete'), 1650);
  window.setTimeout(() => {
    helper.textContent = 'Sequence complete';
  }, 2150);
}

function reset() {
  stage.classList.remove('is-snapping', 'is-complete');
  snapButton.disabled = false;
  snapCta.disabled = false;
  helper.textContent = 'Click the gauntlet or press space';
  particles.replaceChildren();
  snapping = false;
  snapCta.focus();
}

snapButton.addEventListener('click', snap);
snapCta.addEventListener('click', snap);
replayButton.addEventListener('click', reset);
window.addEventListener('keydown', (event) => {
  if (event.code === 'Space') {
    event.preventDefault();
    snap();
  }
});
