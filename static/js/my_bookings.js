// Booking filter tabs
document.querySelectorAll('#filterTabs .filter-chip').forEach(btn => {
  btn.addEventListener('click', function () {
    document.querySelectorAll('#filterTabs .filter-chip').forEach(b => b.classList.remove('active'));
    this.classList.add('active');
    const filter = this.dataset.filter;
    document.querySelectorAll('#bookingsList .booking-item').forEach(item => {
      const show = filter === 'all' || item.dataset.status === filter;
      item.style.display = show ? '' : 'none';
    });
  });
});
