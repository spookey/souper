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

  function photo(file) {
    const show = document.getElementById('show');
    const tell = document.getElementById('tell');

    const img = document.createElement('img');
    const span = document.createElement('span');

    img.src = '${ASSET}/' + file;
    span.innerText = file;

    while (show.hasChildNodes()) { show.removeChild(show.lastChild); }
    while (tell.hasChildNodes()) { tell.removeChild(tell.lastChild); }

    show.appendChild(img);
    tell.appendChild(span);

    smooth(show);
    smooth(tell);
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
