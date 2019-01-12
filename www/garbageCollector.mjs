// @ts-ignore
import $ from "/onDocumentReady.mjs";

/**
 * When the number of cells in the grid overflows the threshold, the oldest
 * cells will be removed. This is to limit memory usage.
 */
const GARBAGE_COLLECTOR_THRESHOLD = 999;

let alreadySummoned = false;

const requestIdleCallback =
  window.requestIdleCallback || window.requestAnimationFrame;

/**
 * @returns {void}
 */
let garbageCollect = () => {
  throw new Error("garbage collection is not ready");
};

$(() => {
  const table = document.querySelector("main");
  const titles = table.querySelectorAll("h3");
  const MESSAGE_LENGTH = titles.length;
  const GC_THRESHOLD =
    GARBAGE_COLLECTOR_THRESHOLD -
    (GARBAGE_COLLECTOR_THRESHOLD % MESSAGE_LENGTH);
  const LAST_TITLE = titles.item(MESSAGE_LENGTH - 1);

  while (LAST_TITLE.nextSibling) {
    // Cleaning up eventual comments or fallback elements
    table.removeChild(LAST_TITLE.nextSibling);
  }

  garbageCollect = () => {
    for (let i = table.childElementCount - GC_THRESHOLD; i > 0; --i) {
      table.removeChild(LAST_TITLE.nextSibling);
    }
  };
});

export default () =>
  new Promise((done, cancel) => {
    if (alreadySummoned) {
      cancel();
    } else {
      alreadySummoned = true;
      requestIdleCallback(() => {
        garbageCollect();
        alreadySummoned = false;
        done();
      });
    }
  });
