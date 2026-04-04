// Live price estimate
const pricePerNight = window.ROOM_PRICE || 0;
const startInput = document.getElementById('id_start_time');
const endInput   = document.getElementById('id_end_time');
const priceBox   = document.getElementById('priceEstimate');
const priceVal   = document.getElementById('estimateValue');
const priceDays  = document.getElementById('estimateDays');

function calcEstimate() {
  if (!startInput || !endInput) return;
  const s = new Date(startInput.value);
  const e = new Date(endInput.value);
  if (!isNaN(s) && !isNaN(e) && e > s) {
    const diffH  = (e - s) / 36e5;
    const nights = Math.ceil(diffH / 24);
    const total  = (nights * pricePerNight).toLocaleString('uk-UA');
    priceVal.textContent = total + ' ₴';
    priceDays.textContent = nights + ' ' +
      (nights === 1 ? 'ніч' : nights < 5 ? 'ночі' : 'ночей');
    priceBox.style.display = 'block';
  } else {
    if (priceBox) priceBox.style.display = 'none';
  }
}

startInput?.addEventListener('change', calcEstimate);
endInput?.addEventListener('change',   calcEstimate);
