//@ts-check
let bottomFixed = true;

/**
 * Scroll to the last item (or displays a dialog if the user has scrolled)
 * @param table {HTMLElement} The element to scroll
 */
const doTheScroll = table => {
  if (bottomFixed) {
    table.scrollTo(0, 1 << 30);
  } else {
    /** @type {HTMLDialogElement} */
    const dialog = document.getElementById("scroll-message");
    dialog.show();
    dialog.addEventListener("click", function() {
      bottomFixed = true;
      doTheScroll(table);
      dialog.close();
    });
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

export default doTheScroll;
