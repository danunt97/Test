// JavaScript helper to trigger photo capture without page reload
window.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('capture-btn');
  const liveview = document.getElementById('liveview');
  const countdown = document.getElementById('countdown');
  const flash = document.getElementById('flash');

  function startLiveview() {
    if (!liveview) return;
    async function next() {
      try {
        const resp = await fetch('/api/liveview?ts=' + Date.now());
        if (resp.ok) {
          const blob = await resp.blob();
          liveview.src = URL.createObjectURL(blob);
        }
      } catch (err) {
        // ignore errors to keep loop running
      }
      requestAnimationFrame(next);
    }
    next();
  }

  startLiveview();

  if (!btn) return;
  btn.addEventListener('click', async (e) => {
    e.preventDefault();
    btn.disabled = true;

    if (countdown) {
      for (let i = 3; i > 0; i--) {
        countdown.textContent = i;
        await new Promise(r => setTimeout(r, 1000));
      }
      countdown.textContent = '';
    }

    if (flash) flash.classList.add('show');

    try {
      const resp = await fetch('/api/capture', { method: 'POST' });
      const data = await resp.json();
      if (data.success && data.filename) {
        const gallery = document.querySelector('.gallery');
        if (gallery) {
          const li = document.createElement('li');
          const a = document.createElement('a');
          a.href = `/image/${data.filename}`;
          const img = document.createElement('img');
          img.src = `/static/${data.filename}`;
          img.alt = data.filename;
          a.appendChild(img);
          li.appendChild(a);
          gallery.prepend(li);
        } else {
          window.location.reload();
        }
      } else if (data.error) {
        alert(data.error);
      }
    } catch (err) {
      alert('Failed to capture image');
    } finally {
      setTimeout(() => flash && flash.classList.remove('show'), 200);
      btn.disabled = false;
    }
  });
});
