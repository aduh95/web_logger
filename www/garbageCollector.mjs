/**
 * When the number of cells in the grid overflows the threshold, the oldest
 * cells will be removed. This is to limit memory usage.
 */
const GARBAGE_COLLECTOR_THRESHOLD = 999;

const requestIdleCallback =
  window.requestIdleCallback || window.requestAnimationFrame;

/**
 * @type {number | null}
 */
let idleCallbackID = null;

/**
 * @returns {void}
 */
let garbageCollect = () => {
  throw new Error("garbage collection is not ready");
};

const init = () => {
  const table = document.querySelector("main");
  const titles = table.querySelectorAll("h3");
  const MESSAGE_LENGTH = titles.length;
  const GC_THRESHOLD =
    GARBAGE_COLLECTOR_THRESHOLD -
    (GARBAGE_COLLECTOR_THRESHOLD % MESSAGE_LENGTH);
  const LAST_TITLE = titles.item(MESSAGE_LENGTH - 1);

  garbageCollect = () => {
    for (let i = table.childElementCount - GC_THRESHOLD; i > 0; --i) {
      table.removeChild(LAST_TITLE.nextSibling);
    }
    idleCallbackID = null;
  };
};

if (document.readyState === "loading") {
  // Loading hasn't finished yet
  document.addEventListener("DOMContentLoaded", init);
} else {
  // `DOMContentLoaded` has already fired
  init();
}

export default () => {
  if (idleCallbackID === null) {
    idleCallbackID = requestIdleCallback(garbageCollect);
  }
};
