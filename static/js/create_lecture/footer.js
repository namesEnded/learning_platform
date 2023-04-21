let mediaQuery = window.matchMedia("(max-width: 714px)");
let icons = document.querySelector(".ICONS");
let email = document.querySelector(".E-MAIL");
let footerContainer = document.querySelector(".memsui--footer--container");
let logo = document.querySelector(".LOGO");
let home = document.querySelector(".HOME");
let courses = document.querySelector(".COURSES");
let faq = document.querySelector(".FAQ");
let about = document.querySelector(".ABOUT");
let contacts = document.querySelector(".CONTACTS");

function addElementInDiv(element, parentElement) {
  parentElement.appendChild(element);
}

function unwrapElementInDiv(element) {
  if (element && element.parentNode) {
    const parent = element.parentNode;
    while (element.firstChild) {
      parent.insertBefore(element.firstChild, element);
    }
    parent.removeChild(element);
  }
}

function handleScreenResize(mq) {
  if (mq.matches) {
    let footerSubContainerUp = document.createElement("div");
    footerSubContainerUp.classList.add("memsui--footer--sub--container--up");

    let footerContainerUp = document.createElement("div");
    footerContainerUp.classList.add("memsui--footer--container--up");

    let footerContainerDown = document.createElement("div");
    footerContainerDown.classList.add("memsui--footer--container--down");

    addElementInDiv(footerContainerUp, footerContainer);
    addElementInDiv(footerContainerDown, footerContainer);

    footerContainerUp = document.querySelector(
      ".memsui--footer--container--up"
    );
    footerContainerDown = document.querySelector(
      ".memsui--footer--container--down"
    );

    // Обернуть элементы в div с классом "memsui--footer--container--up"
    addElementInDiv(logo, footerContainerUp);

    addElementInDiv(footerSubContainerUp, footerContainerUp);
    footerSubContainerUp = document.querySelector(
      ".memsui--footer--sub--container--up"
    );

    // Обернуть элементы в div с классом "memsui--footer--sub--container--up"
    addElementInDiv(icons, footerSubContainerUp);
    addElementInDiv(email, footerSubContainerUp);

    // Обернуть элементы в div с классом "memsui--footer--container--down"
    addElementInDiv(home, footerContainerDown);
    addElementInDiv(courses, footerContainerDown);
    addElementInDiv(faq, footerContainerDown);
    addElementInDiv(about, footerContainerDown);
    addElementInDiv(contacts, footerContainerDown);
  } else {
    // Удалить оберточные div
    let footerContainerDown = document.querySelector(
      ".memsui--footer--container--down"
    );
    unwrapElementInDiv(footerContainerDown);

    let footerContainerUp = document.querySelector(
      ".memsui--footer--container--up"
    );
    unwrapElementInDiv(footerContainerUp);

    let footerSubContainerUp = document.querySelector(
      ".memsui--footer--sub--container--up"
    );
    unwrapElementInDiv(footerSubContainerUp);
  }
}

// Вызов функции при загрузке страницы, чтобы проверить размер экрана
handleScreenResize(mediaQuery);

// Вызов функции при изменении размера экрана
mediaQuery.addListener(handleScreenResize);
