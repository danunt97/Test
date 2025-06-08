// JavaScript helper to trigger photo capture without page reload
window.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('capture-btn');
  if (!btn) return;
  btn.addEventListener('click', async (e) => {
    e.preventDefault();
    btn.disabled = true;
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
      btn.disabled = false;
    }
  });
});
