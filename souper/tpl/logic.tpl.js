window.onload = function() {

  function smooth(elem) {
    elem.style.opacity = 0.0;
    (function fade() {
      let val = parseFloat(elem.style.opacity);
      if ((val += 0.05) <= 1.0) {
        elem.style.opacity = val;
        requestAnimationFrame(fade);
      }
    })();
  }

  function photo(elem) {
    const text = document.getElementById('text');
    const tell = document.getElementById('tell');

    const img = document.createElement('img');
    const href = document.createElement('a');

    img.src = '${ASSET}/' + elem.file;
    href.innerHTML = elem.file;
    href.title = elem.time;
    href.href = elem.href;

    while (tell.hasChildNodes()) { tell.removeChild(tell.lastChild); }
    while (text.hasChildNodes()) { text.removeChild(text.lastChild); }

    tell.appendChild(img);
    text.appendChild(href);

    smooth(tell);
    smooth(text);
  }

  function fetch(location, callback) {
    const req = new XMLHttpRequest();
    req.onreadystatechange = function() {
      if (req.readyState === 4 && req.status === 200) {
        callback(JSON.parse(req.responseText));
      }
    };
    req.open('GET', location);
    req.send();
  }

  fetch('${STORE}', function(data) {
    const delay = parseInt('${DELAY}');
    const len = data.length;

    function fire() { photo(data[Math.floor(Math.random() * len)]); }

    let pos = len;
    while(pos--) { setTimeout(fire, pos * delay); }

    setTimeout(function() { window.location.reload(true); }, len * delay);
  });

};
