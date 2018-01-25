const updateDate = elem => {
  setInterval(() => {
    elem.innerText = new Date().toLocaleTimeString();
  }, 1000);
};

document.addEventListener("DOMContentLoaded", () => {
  updateDate(document.getElementById("time"));

  const table = document.getElementById("data-wrapper");

  for (let i = 0; i < 999; ++i) {
    let elem = document.createElement("tr");
    elem.innerHTML = "<td>0</td><td>0</td><td>0</td><td>0</td><td>0</td>";
    table.appendChild(elem);
  }
});
