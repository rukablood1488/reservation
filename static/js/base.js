// Navbar scroll effect
const nav = document.getElementById('mainNav');
window.addEventListener('scroll', () => {
  nav.classList.toggle('scrolled', window.scrollY > 30);
});

// Mobile toggle
const toggle = document.getElementById('navToggle');
const center = document.getElementById('navCenter');
toggle?.addEventListener('click', () => {
  center.classList.toggle('open');
  const spans = toggle.querySelectorAll('span');
  if (center.classList.contains('open')) {
    spans[0].style.transform = 'rotate(45deg) translate(4px,4px)';
    spans[1].style.opacity  = '0';
    spans[2].style.transform = 'rotate(-45deg) translate(4px,-4px)';
  } else {
    spans.forEach(s => { s.style.transform = ''; s.style.opacity = ''; });
  }
});

// Auto-dismiss toast messages
setTimeout(() => {
  document.querySelectorAll('.toast-msg').forEach(el => {
    el.style.transition = 'opacity .5s';
    el.style.opacity = '0';
    setTimeout(() => el.remove(), 500);
  });
}, 4000);
