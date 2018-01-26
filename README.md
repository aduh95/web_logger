# Apex web client

### Getting started

First, you have to ensure that these dependencies are installed and available on
your path:

* [Node (v8.5+)](//nodejs.org)
* [Yarn](//yarnpkg.com) or [npm](//npmjs.com)

```bash
yarn install
```

Then you are good to go:

```bash
yarn start
```

### Communication with the server

The client expect a JSON string send through the WebSocket of this form:

```json
[
  "date",
  "time",
  "mnemonic",
  "target",
  "message type (CSS class)",
  "message",
  "optional keyboard input",
  "optional audio file path"
]
```

You can try it by adding example in the `example.json` file.
