let bottomFixed = true;

let scrollFrameID = null;

/**
 * Scrolls into view the last child of a given element on the next frame
 * @param {Element} parent
 */
const scrollIntoViewLastElement = parent => {
  if (scrollFrameID === null) {
    scrollFrameID = requestAnimationFrame(() => {
      parent.lastElementChild.scrollIntoView();
      scrollFrameID = null;
    });
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
    dialog.show();
    dialog.addEventListener(
      "click",
      function() {
        bottomFixed = true;
        doTheScroll(table);
        dialog.close();
      },
      { once: true }
    );
  }
};

document.addEventListener("DOMContentLoaded", () => {
  const scrollableElement = document.querySelector("main");

  scrollableElement.addEventListener(
    "scroll",
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
