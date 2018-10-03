// @ts-check
// @ts-ignore
import socket from "/communication.mjs";

const SEPARATOR_CLASS_NAME = "separator";
const SECTION_DEFAULT_LABEL = "LABEL";
const nav = document.createElement("nav");

const createMenu = menu => {
  const list = document.createElement("ul");
  menu.map(createMenuSection).forEach(Node.prototype.appendChild.bind(list));
  return list;
};

const createMenuSection = section => {
  const frag = document.createElement("li");

  if (section.separator) {
    frag.classList.add(SEPARATOR_CLASS_NAME);
  } else {
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
  }

  if (section.submenu) {
    frag.appendChild(createMenu(section.submenu));
  }

  return frag;
};

document.addEventListener("DOMContentLoaded", () => {
  document.body.appendChild(nav);

  try {
    // Recover menu after reloading the page
    const { menu } = JSON.parse(sessionStorage.getItem("menu"));
    nav.appendChild(createMenu(menu));
  } catch (e) {}
});

export default menu => {
  const list = createMenu(menu);
  nav.innerHTML = "";
  nav.appendChild(list);
};
