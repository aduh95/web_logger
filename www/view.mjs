// @ts-check
// @ts-ignore
import scrollToNewMessage from "/scroll.mjs";
// @ts-ignore
import socket from "/communication.mjs";

/**
 * When the number of cells in the grid overflows the threshold, the oldest
 * cells will be removed. This is to limit memory usage.
 */
const GARBAGE_COLLECTOR_THRESHOLD = 999;

/**
 * Sets the date into an element
 * @param elem {HTMLElement} The element to update
 */
const updateDate = elem => {
  elem.innerText = new Date().toLocaleTimeString();
};

/**
 * Plays an audio file
 * @param path {string} The URL of the audio file to play
 */
const playAudio = path => {
  const audio = new Audio(path).play();
  if (audio !== undefined) {
    audio.catch(e => console.error(e));
  }
};

const keyListeners = [];

/**
 * Add a keyboard input to listen to
 * @param keyboardInput {string} The key you want to listen to
 */
const decodeKeyboardInput = keyboardInput =>
  keyListeners.includes(keyboardInput) || keyListeners.push(keyboardInput);

/**
 * Displays a message from back-end into HTML elements
 * @param param {string[]}
 */
export const displayMessage = param => {
  const table = document.querySelector("main");
  const messageToAppend = deserializeMessage(param);

  if (table.childElementCount > GARBAGE_COLLECTOR_THRESHOLD) {
    for (let i = messageToAppend.childElementCount; i; --i) {
      table.querySelector("div").remove();
    }
  }
  table.appendChild(messageToAppend);
  scrollToNewMessage(table);
};

export const handleCommand = command => {
  switch (command) {
    case "clean":
      const messages = document.querySelectorAll("main>div");
      for (const message of messages) {
        message.remove();
      }
      // @ts-ignore
      document.getElementById("scroll-message").close();
      break;
  }
};

/**
 * Creates the HTMLElement objects for a given message
 * @param param {string[]} The message to display
 * @returns A DocumentFragment containing the HTML elements
 */
const deserializeMessage = param => {
  const { length } = param;
  const frag = document.createDocumentFragment();

  if (length > 2) {
    for (var i = 1; i < length - 2; ++i) {
      let elem = document.createElement("div");
      elem.appendChild(document.createTextNode(param[i]));
      frag.appendChild(elem);
    }
    frag.lastElementChild.setAttribute("class", param[0]);

    if (param[i++]) {
      decodeKeyboardInput(param[i - 1]);
    }

    if (param[i++]) {
      playAudio(param[i - 1]);
    }
  }

  return frag;
};

document.addEventListener("DOMContentLoaded", () => {
  const time = document.getElementById("time");
  updateDate(time);
  setInterval(() => {
    updateDate(time);
  }, 1000);
});

window.addEventListener("keyup", event => {
  if (keyListeners.includes(event.key)) {
    socket.send(event.key);
    keyListeners.splice(keyListeners.indexOf(event.key), 1);
  }
});
