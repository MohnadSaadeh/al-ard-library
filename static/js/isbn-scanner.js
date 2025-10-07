// ISBN Scanner helper
// Listens to keyboard input from a barcode scanner that sends the code followed by Enter.
// When Enter is pressed, it POSTs the scanned ISBN to the server endpoint and expects a JSON reply.

(function(){
  let buffer = '';
  let lastTime = Date.now();
  const interKeyThreshold = 30; // ms between keystrokes to treat as scanner

  function sendScan(url, isbn) {
    const form = new FormData();
    form.append('isbn', isbn);

    // read CSRF token from cookie (Django default)
    function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');

    fetch(url, {
      method: 'POST',
      body: form,
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': csrftoken || ''
      },
      credentials: 'same-origin'
    }).then(r => r.json()).then(json => {
      if (!json) return;
      if (json.status === 'not_found') {
        alert('Product not found');
        return;
      }
      if (json.status === 'ok') {
        // call a global renderer if available
        if (window.onScannerUpdate) {
          window.onScannerUpdate(json);
        } else {
          console.log('scan result', json);
        }
      }
    }).catch(err => {
      console.error('scan post error', err);
    });
  }

  window.addEventListener('keydown', function(e){
    // Only listen when the dedicated scanner input has focus
    const active = document.activeElement && document.activeElement.id === 'scanner-input';
    if (!active) return; // ignore global keys when not focused
    const now = Date.now();
    if (now - lastTime > 1000) {
      // reset buffer if long pause
      buffer = '';
    }
    lastTime = now;

    if (e.key === 'Enter') {
      const code = buffer.trim();
      buffer = '';
      if (!code) return;
      // choose endpoint by page
      const salePath = '/scan/add-to-sale/';
      const purchasePath = '/scan/add-to-purchase/';
      const pathname = window.location.pathname;
      const endpoint = pathname.startsWith('/purchases') ? purchasePath : salePath;
      sendScan(endpoint, code);
      e.preventDefault();
      return;
    }

    // ignore modifier keys
    if (e.key.length === 1) {
      buffer += e.key;
    }
  });

  // helper to focus scanner input from other code (e.g., a button)
  window.focusScannerInput = function(){
    const el = document.getElementById('scanner-input');
    if (el) el.focus();
  };
})();
