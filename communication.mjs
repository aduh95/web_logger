//@ts-check
/**
 * @author aduh95
 * WebSocket client module
 */

import { displayMessage } from "./view.mjs";

const socket = new WebSocket("ws://" + window.location.host + "/");

// Listen for messages to reload the page
socket.addEventListener("message", event =>
  displayMessage(JSON.parse(event.data))
);

// When server closes the connection, let's close the tab
socket.addEventListener("close", () => window.close());

export default socket;
