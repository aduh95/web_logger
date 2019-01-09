// @ts-ignore
import $ from "/onDocumentReady.mjs";

$(
  () =>
    "HTMLDialogElement" in window &&
    document.getElementById("fallback-message").parentNode.remove()
);
