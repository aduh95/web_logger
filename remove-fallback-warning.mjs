const init = () =>
  document.getElementById("fallback-message").parentNode.remove();

if (window.document.readyState === "loading") {
  window.document.addEventListener("DOMContentLoaded", init);
} else {
  init.apply(window.document);
}
