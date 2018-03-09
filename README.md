# Apex web client

### Getting started

First, you have to ensure that these dependencies are installed and available on
your path:

* [Python 3.5+](//python.org)

```bash
python3.5 -m pip install websockets
```

Then you are good to go:

```bash
./demo.py -h # prints the help
./demo.py # launch with default arguments

# If python3.5 is not in your path, you have to execute the following
python3 demo.py
```

> There is also a demo server in Node.js that you can run with `yarn start` or
> `npm start`.

### Browser support

A banner pops in on browsers which don't support the needed feature. Also, it
has been developed for those browsers:

* Chrome 62+
* Firefox 57+ (please activate the following flags:
  `dom.dialog_element.enabled`, `dom.moduleScripts.enabled`,
  `dom.allow_scripts_to_close_windows`) (Warning: Doesn't seem to work when
  launched from python CLI)

### Communication with the server

The client expect a JSON string send through the WebSocket of this form:

```json
{
  "message": [
    "date",
    "time",
    "mnemonic",
    "target",
    "message type (CSS class)",
    "message",
    "optional keyboard input",
    "optional audio file path"
  ]
}
```

The server can set a menu which will be displayed on the top of the interface.
There is an example of menu definition in the `menu.json` file. When several
menu definitions are sent, the last one will be displayed. This allows you to
override a menu definition on the fly.

You can try it by adding example in the `example.json` file.

### Python API

The methods are available via the `ClientApex` class. You can give a function as
the `onReady` parameter of the constructor to interact with the client. Please
check `demo.py` to see how to get started.
