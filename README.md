# souper

This project used to be my image crawler for `soup.io`.

There isn't much to crawl anymore as the site is dead now (still crying).

So this project has been refactored to replace the crawler
with some very simple image copying logic.

It generates a simple webpage with an image slideshow.

## command line

Main entry point is `./run.py`.

- for a complete list of options see `./run.py --help`
- set the logging level with `-v` or `--verbose`
- change the page title with `-t` or `--title`
- set the duration to wait between images with `-d` or `--delay`
  (in milliseconds)
- final two required arguments are the `source` and `target` folders

## running

Although the generated webpage is static, it won't work when not
served through a webserver.

For a local preview change into the `target` folder and use this command:

```sh
python3 -m http.server 8000 --bind localhost
```

[localhost:8000](http://localhost:8000)
