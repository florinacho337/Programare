const selectCount = document.querySelectorAll("select").length;

document.querySelectorAll("select").forEach((select, index) => {
  select.addEventListener("dblclick", () => {
    if (index < selectCount - 1) {
      const nextSelect = document.querySelectorAll("select")[index + 1];
      nextSelect.appendChild(select.options[select.selectedIndex]);
    } else {
      const firstSelect = document.querySelectorAll("select")[0];
      firstSelect.appendChild(select.options[select.selectedIndex]);
    }
  });
});