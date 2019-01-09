// @ts-ignore
import $ from "/onDocumentReady.mjs";
// @ts-ignore
import socket from "/communication.mjs";

const SEPARATOR_CLASS_NAME = "separator";
const SECTION_DEFAULT_LABEL = "LABEL";
const nav = document.createElement("nav");

/**
 * @typedef {Object} MenuSection
 * @property {boolean} separator
 * @property {string} label
 * @property {number} click
 * @property {MenuSection[]} submenu
 */

/**
 * Creates the menu and submenu elements
 * @param {MenuSection[]} menu The content of the menu
 * @returns {HTMLUListElement}
 */
const createMenu = menu => {
  const list = document.createElement("ul");
  menu.map(createMenuSection).forEach(Node.prototype.appendChild.bind(list));
  return list;
};

/**
 * Creates a submenu element
 * @param {MenuSection} section
 * @returns {HTMLLIElement}
 */
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

$(() => {
  document.body.appendChild(nav);

  try {
    // Recover menu after reloading the page
    const { menu } = JSON.parse(sessionStorage.getItem("menu"));
    nav.appendChild(createMenu(menu));
  } catch (e) {}
});

/**
 * @param {MenuSection[]} menu The content of the menu to create
 */
export default menu => {
  const list = createMenu(menu);
  nav.innerHTML = "";
  nav.appendChild(list);
};
