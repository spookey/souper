document.addEventListener('DOMContentLoaded', () => {
  const SHOW = document.getElementById('show');
  const TELL = document.getElementById('tell');
  const DELAY = parseInt('${DELAY}');

  const smooth = (elem) => {
    elem.style.setProperty('opacity', 0);
    (async function fade() {
      const val = parseFloat(elem.style.opacity);
      if (val < 1.0) {
        elem.style.setProperty('opacity', 0.025 + val);
        requestAnimationFrame(fade);
      }
    })();
    return elem;
  };

  const photo = (file) => {
    const show = document.createElement('img');
    show.setAttribute('src', `${ASSET}/$${file}`);

    const tell = document.createElement('span');
    tell.append(document.createTextNode(file));

    SHOW.replaceChildren(smooth(show));
    TELL.replaceChildren(smooth(tell));
  };

  fetch('${STORE}')
    .then((res) => res.json())
    .then((data) => {
      [...Array(data.length).keys()]
        .forEach((pos) => setTimeout(
          () => photo(data[Math.floor(Math.random() * data.length)]),
          pos * DELAY
        ));

      setTimeout(
        () => window.location.reload(true),
        data.length * DELAY
      );
    })
    .catch(console.error);
});
