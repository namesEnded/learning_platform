// const editableText = document.querySelector('.editable-text');
// const editButton = document.querySelector('.edit-button');
// const content = editableText.querySelector('p');

// editButton.addEventListener('click', () => {
//   editableText.classList.add('editing');
//   const textarea = document.createElement('textarea');
//   textarea.value = content.textContent;
//   textarea.classList.add("memsui--edit--area");
//   editableText.appendChild(textarea);
//   textarea.focus();

//   textarea.addEventListener('blur', () => {
//     content.textContent = textarea.value;
//     editableText.removeChild(textarea);
//     editableText.classList.remove('editing');
//   });
// });

const editableTextField = document.querySelector('.memsui--editable--text--field');
  const textContainer = editableTextField.querySelector('.text-container');
  const editButton = editableTextField.querySelector('.edit-button');
//   const textField = document.createElement('div');
//   textField.textContent = textContainer.textContent;
//   textContainer.replaceWith(textField);

  editButton.addEventListener('click', () => {
    textContainer.setAttribute('contenteditable', 'true');
    textContainer.focus();
  });

  textContainer.addEventListener('blur', () => {
    textContainer.setAttribute('contenteditable', 'false');
    // textContainer.textContent = textField.textContent;
  });

  textContainer.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
      event.preventDefault();
      textContainer.blur();
    }
  });