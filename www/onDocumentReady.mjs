/**
 * Equivalent to jQuery(document).ready
 * @param {EventListener} init Callback to be executed once the DOM is ready
 */
export default function(init) {
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init.apply(window.document);
  }
}
