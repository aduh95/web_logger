// @ts-ignore
import socket from "/communication.mjs";

const keyListeners = [];

/**
 * Add a keyboard input to listen to
 * @param {string} keyboardInput The key you want to listen to
 */
const decodeKeyboardInput = keyboardInput =>
  keyListeners.includes(keyboardInput) || keyListeners.push(keyboardInput);

window.addEventListener("keyup", event => {
  if (keyListeners.includes(event.key)) {
    socket.send(event.key);
    keyListeners.splice(keyListeners.indexOf(event.key), 1);
  }
});

export default decodeKeyboardInput;
