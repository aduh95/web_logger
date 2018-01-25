const updateDate = elem => {
  setInterval(() => {
    elem.innerText = new Date().toLocaleTimeString();
  }, 1000);
};

document.addEventListener("DOMContentLoaded", () => {
  updateDate(document.getElementById("time"));

  const table = document.querySelector("main");

  for (let i = 0; i < 999; ++i) {
    let elem = document.createElement("div");
    elem.innerText = "message";
    table.appendChild(elem);
  }
});
