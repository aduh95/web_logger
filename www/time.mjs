class AutoUpdateTimeElement extends HTMLTimeElement {
  connectedCallback() {
    if (this.isConnected) {
      clearInterval(this._updateDateID);
      this._updateDateID = setInterval(() => {
        this.updateDate();
      }, 1000);
    }
  }

  disconnectedCallback() {
    clearInterval(this._updateDateID);
  }

  /**
   * Sets the date into an element
   */
  updateDate() {
    this.textContent = new Date().toLocaleTimeString();
  }
}

customElements.define("auto-update", AutoUpdateTimeElement, {
  extends: "time",
});
