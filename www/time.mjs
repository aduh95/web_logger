function scheduleNext(time) {
  const elapsed = time - this._start;
  const roundedElapsed = Math.round(elapsed / 1000) * 1000;
  const targetNext = this._start + roundedElapsed + 1000;
  this._timeout = setTimeout(
    () => (this._raf = requestAnimationFrame(this._scheduleNext)),
    targetNext - performance.now()
  );

  this.updateDate();
}

class AutoUpdateTimeElement extends HTMLTimeElement {
  constructor() {
    super();
    this._scheduleNext = scheduleNext.bind(this);
  }

  connectedCallback() {
    if (this.isConnected) {
      this.disconnectedCallback();
      this._scheduleNext((this._start = performance.now()));
    }
  }

  disconnectedCallback() {
    clearTimeout(this._timeout);
    cancelAnimationFrame(this._raf);
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
