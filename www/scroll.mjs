// @ts-ignore
import $ from "/onDocumentReady.mjs";
// @ts-ignore
import garbageCollect from "/garbageCollector.mjs";

const passiveEvent = { passive: true };
let bottomFixed = true;

/**
 * Scrolls into view the last child of a given element on the next frame
 * @param {Element} parent
 */
const scrollIntoViewLastElement = parent =>
  garbageCollect()
    .then(() => {
      const { matches } = matchMedia("(prefers-reduced-motion:reduce)");
      const behavior = matches ? "auto" : "smooth";
      parent.lastElementChild.scrollIntoView({
        behavior,
        block: "end",
      });
    })
    .catch(Function.prototype); // Ignoring garbage collection cancellation

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

  const computeScroll = () => {
    bottomFixed =
      scrollableElement.scrollTop + scrollableElement.clientHeight ===
      scrollableElement.scrollHeight;
  };

  scrollableElement.addEventListener("wheel", computeScroll, passiveEvent);
  scrollableElement.addEventListener("touchmove", computeScroll, passiveEvent);
  window.addEventListener("keyup", computeScroll, passiveEvent);
});

addEventListener(
  "resize",
  () => document.getElementById("scroll-message").click(),
  passiveEvent
);

export default doTheScroll;
