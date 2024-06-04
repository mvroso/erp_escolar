document.addEventListener('DOMContentLoaded', () => {
  const selects = document.querySelectorAll('select');
  const resetButton = document.getElementById('resetButton');

  selects.forEach(select => {
    select.addEventListener('change', (event) => {
      const selectedValue = event.target.value;
      if (selectedValue) {
        selects.forEach(otherSelect => {
          if (otherSelect !== event.target) {
            otherSelect.disabled = true;
          }
        });
      } else {
        selects.forEach(otherSelect => {
          otherSelect.disabled = false;
        });
      }
    });
  });

  resetButton.addEventListener('click', () => {
    selects.forEach(select => {
      select.value = ""; // Unselect all options
      select.disabled = false;  // Re-enable all selects
    });
  });
});