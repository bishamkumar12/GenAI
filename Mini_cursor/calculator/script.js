const display = document.getElementById('display');
const buttons = document.querySelectorAll('.btn');
const equals = document.getElementById('equals');
const clear = document.getElementById('clear');

let currentInput = '';

display.value = '';

buttons.forEach(btn => {
  btn.addEventListener('click', function() {
    const value = this.getAttribute('data-value');
    if (value) {
      currentInput += value;
      display.value = currentInput;
    }
  });
});

equals.addEventListener('click', function() {
  try {
    const result = eval(currentInput);
    display.value = result;
    currentInput = result.toString();
  } catch (e) {
    display.value = 'Error';
    currentInput = '';
  }
});

clear.addEventListener('click', function() {
  currentInput = '';
  display.value = '';
});
