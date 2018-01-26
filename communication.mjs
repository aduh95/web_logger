//@ts-check
/**
 * @author aduh95
 * WebSocket client module
 */

import { displayMessage } from "/view.mjs";
import setMenu from "/menu.mjs";

const socket = new WebSocket("ws://" + window.location.host + "/");

// Listen for messages to reload the page
socket.addEventListener("message", event => {
  const data = JSON.parse(event.data);

  if (data.message) {
    displayMessage(data.message);
  }

  if (data.menu) {
    setMenu(data.menu);
  }
});

// When server closes the connection, let's close the tab
socket.addEventListener("close", () => window.close());

export default socket;
