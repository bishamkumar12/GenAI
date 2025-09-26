const todoForm = document.getElementById('todo-form');
const todoInput = document.getElementById('todo-input');
const todoList = document.getElementById('todo-list');

function createTodoItem(text) {
  const li = document.createElement('li');
  const span = document.createElement('span');
  span.textContent = text;
  span.addEventListener('click', () => {
    li.classList.toggle('completed');
  });
  const deleteBtn = document.createElement('button');
  deleteBtn.textContent = 'Delete';
  deleteBtn.className = 'delete-btn';
  deleteBtn.onclick = () => {
    todoList.removeChild(li);
  };
  li.appendChild(span);
  li.appendChild(deleteBtn);
  return li;
}

todoForm.addEventListener('submit', function(e) {
  e.preventDefault();
  const text = todoInput.value.trim();
  if (text !== '') {
    const todoItem = createTodoItem(text);
    todoList.appendChild(todoItem);
    todoInput.value = '';
    todoInput.focus();
  }
});
