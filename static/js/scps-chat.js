document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.getElementById('scps-chat-toggle');
  const panel = document.getElementById('scps-chat-panel');
  const close = document.getElementById('scps-chat-close');
  const form = document.getElementById('scps-chat-form');
  const input = document.getElementById('scps-chat-input');
  const log = document.getElementById('scps-chat-log');

  if (!toggle || !panel || !form || !input || !log) return;

  function show(open) {
    panel.hidden = !open;
    toggle.setAttribute('aria-expanded', String(open));
    if (open) input.focus();
  }

  toggle.addEventListener('click', () => show(panel.hidden));

  if (close) {
    close.addEventListener('click', () => show(false));
  }

  function bubble(text, who) {
    const el = document.createElement('div');
    el.className = 'scps-bubble ' + who;
    el.textContent = text;
    log.appendChild(el);
    log.scrollTop = log.scrollHeight;
    return el;
  }

  bubble(
    'Hi! I can help with parking and navigating this website. What would you like to know?',
    'ai'
  );

  form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const message = input.value.trim();
    if (!message) return;

    input.value = '';
    bubble(message, 'user');

    const waiting = bubble('Thinking…', 'ai');
    const btn = form.querySelector('button');
    btn.disabled = true;

    try {
      const csrf =
        document.cookie
          .split('; ')
          .find(row => row.startsWith('csrftoken='))
          ?.split('=')[1] ||
        form.querySelector('[name=csrfmiddlewaretoken]')?.value ||
        '';

      const data = new URLSearchParams({ message });

      const res = await fetch('/api/chatbot/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': csrf
        },
        body: data,
        credentials: 'same-origin'
      });

      const json = await res.json();

      waiting.textContent =
        json.response ||
        json.reply ||
        json.error ||
        'Sorry, something went wrong.';

    } catch (err) {
      waiting.textContent =
        'Could not connect to the server. Please try again.';
      console.error('Chatbot error:', err);

    } finally {
      btn.disabled = false;
      input.focus();
      log.scrollTop = log.scrollHeight;
    }
  });
});