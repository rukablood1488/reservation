// Stagger cards on filter click
document.querySelectorAll('.filter-chip').forEach(chip => {
  chip.addEventListener('click', () => {
    document.querySelectorAll('.room-card').forEach((c, i) => {
      c.style.animation = 'none';
      void c.offsetWidth;
      c.style.animation = `fadeUp .5s ${i * 80}ms both`;
    });
  });
});
