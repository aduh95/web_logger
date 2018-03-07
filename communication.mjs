//@ts-check
/**
 * @author aduh95
 * WebSocket client module
 */

//@ts-ignore
import PORT from "/webSocketPort.mjs";
//@ts-ignore
import { displayMessage } from "/view.mjs";
//@ts-ignore
import setMenu from "/menu.mjs";

const socket = new WebSocket(`ws://${window.location.hostname}:${PORT}/`);

const closeWindow = () => window.close();

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
socket.addEventListener("close", closeWindow);

window.addEventListener("beforeunload", () => {
  socket.removeEventListener("close", closeWindow);
});

export default socket;
