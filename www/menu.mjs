// @ts-check
// @ts-ignore
import socket from "/communication.mjs";

const SECTION_DEFAULT_LABEL = "LABEL";
const nav = document.createElement("nav");

const createMenu = (menu, parent) => {
  const list = document.createElement("ul");
  menu.map(createMenuSection).forEach(cv => list.appendChild(cv));
  return list;
};

const createMenuSection = section => {
  const frag = document.createElement("li");

  const button = document.createElement("button");
  button.appendChild(
    document.createTextNode(section.label || SECTION_DEFAULT_LABEL)
  );
  if (section.click) {
    button.onclick = function() {
      socket.send(section.click);
    };
  }
  frag.appendChild(button);

  if (section.submenu) {
    frag.appendChild(createMenu(section.submenu));
  }

  return frag;
};

document.addEventListener("DOMContentLoaded", () => {
  document.body.appendChild(nav);
});

export default menu => {
  const list = createMenu(menu, nav);
  nav.innerHTML = "";
  nav.appendChild(list);
};
