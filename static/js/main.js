// const label = document.querySelector('#kek');

// // создаем экземпляр MutationObserver
// const observer = new MutationObserver((mutationsList) => {
//   for(let mutation of mutationsList) {
//     if(mutation.type === 'attributes' && mutation.attributeName === 'flex-wrap') {
//       console.log('Стиль элемента был изменен');
//       break;
//     }
//   }
// });

// // настраиваем наблюдатель для отслеживания изменений в атрибуте style
// const config = { attributes: true, attributeFilter: ['flex-wrap'] };
// observer.observe(label, config);