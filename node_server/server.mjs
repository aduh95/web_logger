import open from "open";
import path from "path";
import fs from "fs/promises";
import express from "express";
import webSocket from "websocket";

const WAIT_FOR_BROWSER_TO_OPEN = 2500;
let waitForBrowserToOpen = null;

const SERVED_FILES_FOLDER = path.resolve("./www");
const INDEX_FILE = path.join(SERVED_FILES_FOLDER, "index.html");
const WEBSOCKET_SERVER = "/webSocketPort.mjs";
export const FONT_FILES = ["/arial.woff2", "/arialbd.woff2"];
export const CSS_FILES = [
  "/layout.css",
  "/messages.css",
  "/fallback-message.css",
  "/scroll-message.css",
];
export const JS_MODULES = [
  "/communication.mjs",
  "/menu.mjs",
  "/remove-fallback-warning.mjs",
  "/scroll.mjs",
  "/view.mjs",
  WEBSOCKET_SERVER,
];
export const JS_SCRIPTS = [];
export const JS_NO_MODULES_FALLBACK = [];

const app = express();

app.get("/", function(req, res) {
  res.sendFile(INDEX_FILE);
});

for (let serverFile of [
  {
    type: "text/css",
    files: CSS_FILES,
    folder: "",
  },
  {
    type: "application/javascript",
    files: JS_MODULES,
    folder: "",
  },
  {
    type: "application/javascript",
    files: JS_SCRIPTS.concat(JS_NO_MODULES_FALLBACK),
    folder: "",
  },
  {
    type: "font/woff2",
    files: FONT_FILES,
    folder: "",
  },
]) {
  for (let file of serverFile.files) {
    app.get(file, (req, res) => {
      fs
        .readFile(path.join(SERVED_FILES_FOLDER, serverFile.folder + file))
        .then(result => res.set("Content-Type", serverFile.type).send(result))
        .catch(err => (console.error(err), res.sendStatus(404)));
    });
  }
}

const readExampleFile = () =>
  fs.readFile("./example.json").then(buffer => JSON.parse(buffer));

let wsConnection = null;

export default CONFIG => {
  // Waiting for the CONFIG to be loaded before starting the server

  let server = app.listen(CONFIG.PORT_NUMBER, "localhost", function() {
    console.log(`Listening on port ${CONFIG.PORT_NUMBER}!`);
  });
  let wsServer = new webSocket.server({
    httpServer: server,
    autoAcceptConnections: true,
  });
  wsServer.on("connect", connection => {
    wsConnection && wsConnection.close();
    wsConnection = connection;

    connection.ping(1);
    connection.on("message", msg => {
      console.log(msg);
      if (msg.utf8Data === "quit") {
        wsConnection.close();
        process.exit();
      }
    });

    let i = 0;

    fs.readFile("./menu.json").then(buffer => {
      wsConnection.send(buffer.toString("utf-8"));
    });

    readExampleFile().then(examples => {
      for (let example of examples) {
        setTimeout(d => {
          wsConnection.send(JSON.stringify({ message: example }));
        }, 1000 + i++ * 100);
      }
    });
  });

  fs
    .writeFile(
      SERVED_FILES_FOLDER + WEBSOCKET_SERVER,
      "export default " + CONFIG.PORT_NUMBER
    )
    .then(() => refreshBrowser(CONFIG));
};

export const refreshBrowser = CONFIG => {
  if (wsConnection && wsConnection.connected) {
    console.log("Sending socket to refresh browser");
    wsConnection.send("refresh");
  } else if (CONFIG.AUTO_OPEN_BROWSER && !waitForBrowserToOpen) {
    console.log("Opening browser");
    open("http://localhost:" + CONFIG.PORT_NUMBER, CONFIG.BROWSER_NAME);
    waitForBrowserToOpen = setTimeout(() => {
      waitForBrowserToOpen = null;
    }, WAIT_FOR_BROWSER_TO_OPEN);
  } else {
    console.log("Document ready");
  }
};