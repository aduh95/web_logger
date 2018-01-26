//@ts-check

const SPLIT_CHARACTER = ",";

/**
 * Sets the date into an element
 * @param elem {HTMLElement} The element to update
 */
const updateDate = elem => {
  setInterval(() => {
    elem.innerText = new Date().toLocaleTimeString();
  }, 1000);
};

/**
 * Plays an audio file
 * @param path {string} The URL of the audio file to play
 */
const playAudio = path => {
  const audio = new HTMLAudioElement(path).play();
  if (audio !== undefined) {
    audio.catch(e => console.error(e));
  }
};

/**
 * TODO
 * @param keyboardInput {any} TODO
 */
const decodeKeyboardInput = keyboardInput => null;

/**
 * Decodes a message from back-end into HTML elements
 * @param msg {string} The message to decode
 * @returns A DocumentFragment containing the HTML elements
 */
const decodeMessage = msg => {
  let i;
  const param = msg.split(SPLIT_CHARACTER);
  const frag = document.createDocumentFragment();

  for (i = 0; i < 4; ++i) {
    let elem = document.createElement("div");
    elem.appendChild(document.createTextNode(param[i]));
    frag.appendChild(elem);
  }

  let msgElement = document.createElement("div");
  msgElement.setAttribute("class", param[i++]);
  msgElement.appendChild(document.createTextNode(param[i++]));
  frag.appendChild(msgElement);

  if (param[i++]) {
    decodeKeyboardInput(param[i - 1]);
  }

  if (param[i++]) {
    playAudio(param[i - 1]);
  }

  return frag;
};

document.addEventListener("DOMContentLoaded", () => {
  updateDate(document.getElementById("time"));

  const table = document.querySelector("main");

  for (let i = 0; i < 999; ++i) {
    let elem = document.createElement("div");
    elem.innerText = "message";
    table.appendChild(decodeMessage("date,heure,AZERTY,0,error,Hello World"));
  }
});
