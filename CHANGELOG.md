# Changelog

### v0.6.0 (2022-04-26)

- BREAKING: Minimal supported Python version: 3.7
- Fix compatibility with websockets 10.x (and drop support for older versions)

### v0.5.1 (2019-10-23)

- Fix a bug causing audio files to overlap

### v0.5.0 (2019-09-17)

- BREAKING: Change browser support (now requiring Chromium 67+)
- Disable smooth auto-scrolling when Reduce Motion is on (require a compatible
  OS+browser)
- Queue DOM modification on IDLE time to improve the perceived perf

### v0.4.0 (2019-05-08)

- BREAKING: Change browser support (now requiring Chromium 66+)
- Add support for touchscreen and keyboard scrolling

### v0.3.5 (2019-01-12)

- Improve perf on the client

### v0.3.4 (2019-01-12)

- Fix JS error

### v0.3.3 (2019-01-11)

- Defer scrolling after garbage collection on the client

### v0.3.2 (2019-01-08)

- Fix JS error on malformed messages
- Improve JS garbage collection and auto-scroll perf
- Fix a rare bug on startup

### v0.3.1 (2018-11-04)

- Fix a bug blocking program infinitely when browser subprocess terminates
  before UI ready event is fired

### v0.3.0 (2018-10-23)

- Initial public release
