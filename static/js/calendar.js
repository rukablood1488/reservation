document.addEventListener('DOMContentLoaded', function () {
  const calEl  = document.getElementById('calendar');
  const events = window.CALENDAR_EVENTS || [];

  const cal = new FullCalendar.Calendar(calEl, {
    initialView: 'dayGridMonth',
    locale: 'uk',
    headerToolbar: {
      left:   'prev,next today',
      center: 'title',
      right:  'dayGridMonth,listMonth'
    },
    buttonText: { today: 'Сьогодні', month: 'Місяць', list: 'Список' },
    events: events,
    eventDisplay: 'block',
    eventTimeFormat: { hour: '2-digit', minute: '2-digit', hour12: false },
    eventClick: function (info) {
      const p = info.event.extendedProps;
      alert(
        ` ${info.event.title}\n` +
        ` ${p.guest || ''}\n` +
        ` ${info.event.startStr} → ${info.event.endStr}\n` +
        ` Статус: ${p.status_display || ''}`
      );
    },
  });

  cal.render();

  // Room filter chips
  document.querySelectorAll('.room-filter-chip').forEach(chip => {
    chip.addEventListener('click', function () {
      document.querySelectorAll('.room-filter-chip').forEach(c => c.classList.remove('active'));
      this.classList.add('active');
      const roomId = this.dataset.room;
      cal.removeAllEvents();
      if (roomId === 'all') {
        cal.addEventSource(events);
      } else {
        cal.addEventSource(events.filter(e => String(e.roomId) === roomId));
      }
    });
  });
});
