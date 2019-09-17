// @ts-ignore
import appendNewMessageAndScroll from "./scroll.mjs";
// @ts-ignore
import decodeKeyboardInput from "/keyboardHandler.mjs";

/**
 * @type {HTMLAudioElement}
 */
let currentAudio;

/**
 * Plays an audio file
 * @param {string} path The URL of the audio file to play
 */
const playAudio = path => {
  if (currentAudio) {
    currentAudio.pause();
    currentAudio.remove();
  }
  currentAudio = new Audio(path);
  currentAudio
    .play()
    .then(() => {
      currentAudio.remove();
      currentAudio = null;
    })
    .catch(console.error);
};

/**
 * Displays a message from back-end into HTML elements
 * @param {string[]} param
 */
export const displayMessage = param => {
  const messageToAppend = deserializeMessage(param);

  appendNewMessageAndScroll(messageToAppend);
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
