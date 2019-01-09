// @ts-ignore
import $ from "/onDocumentReady.mjs";
// @ts-ignore
import scrollToNewMessage from "/scroll.mjs";
// @ts-ignore
import decodeKeyboardInput from "/keyboardHandler.mjs";
// @ts-ignore
import garbageCollect from "/garbageCollector.mjs";

/**
 * Sets the date into an element
 * @param {HTMLElement} elem The element to update
 */
const updateDate = elem => {
  elem.textContent = new Date().toLocaleTimeString();
};

/**
 * Plays an audio file
 * @param {string} path The URL of the audio file to play
 */
const playAudio = path => {
  const audio = new Audio(path).play();
  if (audio !== undefined) {
    audio.catch(e => console.error(e));
  }
};

/**
 * Displays a message from back-end into HTML elements
 * @param {string[]} param
 */
export const displayMessage = param => {
  const table = document.querySelector("main");
  const messageToAppend = deserializeMessage(param);

  garbageCollect();
  table.appendChild(messageToAppend);
  scrollToNewMessage(table);
};

/**
 * Creates the HTMLElement objects for a given message
 * @param {string[]} param The message to display
 * @returns {DocumentFragment} containing the HTML elements
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

$(() => {
  const time = document.getElementById("time");
  updateDate(time);
  setInterval(() => {
    updateDate(time);
  }, 1000);
});
