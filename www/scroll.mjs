// @ts-ignore
import $ from "/onDocumentReady.mjs";
// @ts-ignore
import garbageCollect from "/garbageCollector.mjs";

let bottomFixed = true;

/**
 * Scrolls into view the last child of a given element on the next frame
 * @param {Element} parent
 */
const scrollIntoViewLastElement = async parent => {
  try {
    await garbageCollect();

    parent.lastElementChild.scrollIntoView({
      behavior: "smooth",
      block: "end",
    });
  } finally {
    // Ignoring garbage collection cancellation
  }
};

/**
 * Scroll to the last item (or displays a dialog if the user has scrolled)
 * @param {HTMLElement} table The element to scroll
 */
const doTheScroll = table => {
  if (bottomFixed) {
    scrollIntoViewLastElement(table);
  } else {
    /** @type {HTMLDialogElement} */
    // @ts-ignore
    const dialog = document.getElementById("scroll-message");
    if (!dialog.open) {
      dialog.show();
      dialog.addEventListener(
        "click",
        function() {
          bottomFixed = true;
          scrollIntoViewLastElement(table);
          dialog.close();
        },
        { once: true }
      );
    }
  }
};

$(() => {
  const scrollableElement = document.querySelector("main");

  scrollableElement.addEventListener(
    "wheel",
    () => {
      bottomFixed =
        scrollableElement.scrollTop + scrollableElement.clientHeight ===
        scrollableElement.scrollHeight;
    },
    { passive: true }
  );
});

addEventListener(
  "resize",
  () => document.getElementById("scroll-message").click(),
  { passive: true }
);

export default doTheScroll;
