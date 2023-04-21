const hamburger = document.querySelector(".hamburger");
const navMenu = document.querySelector(".nav-menu");
const labels = document.querySelectorAll('.label');
const navLink = document.querySelectorAll(".nav-link");
const navToggle = document.getElementById('nav-toggle');
const teleHamburger = document.querySelector('.tele-hamburger');

const burgerNav = document.querySelector('.burger-nav-link');
const dropdown = document.querySelector('.dropdown');
const dropdownClose = document.querySelector('.dropdown-close');

hamburger.addEventListener("click", toggleMenu);

burgerNav.addEventListener('click', () => {
  dropdown.classList.toggle('active');

  if (dropdown.classList.contains('active')) {
    setTimeout(() => {
      dropdown.style.opacity = '1';
      dropdown.style.transform = 'translateY(0)';
    }, 10);
  } else {
    dropdown.style.opacity = '0';
    dropdown.style.transform = 'translateY(-10px)';
  }
});

dropdownClose.addEventListener('click', () => {
  dropdown.classList.remove('active');
});

function toggleMenu() {
    hamburger.classList.toggle('active');
    navMenu.classList.toggle('active');

    navLink.forEach(link => {
      link.addEventListener('click', () => {
        navMenu.classList.remove('active');
        navMenu.classList.add('hidden');
        navToggle.checked = false;
      });
    });

    labels.forEach((label) => {
      label.classList.toggle('active');
    });
    if (navMenu.classList.contains('active') && hamburger.classList.contains('active')) {
      navMenu.classList.remove('hidden');
    } else {
      navMenu.classList.add('hidden');
    }
}

navLink.forEach(n => n.addEventListener("click", closeMenu));

function closeMenu() {
    hamburger.classList.remove('active');
    navMenu.classList.remove('active');
    labels.forEach((label) => {
      label.classList.remove('active');
    });
}

const labelContainer = document.createElement('div');
labelContainer.classList.add('label-container');

const courses = document.createElement('a');
courses.textContent = "Курсы";
courses.classList.add('label');
courses.href = "#";
labelContainer.appendChild(courses);

const assignments = document.createElement('a');
assignments.textContent = "Задания";
assignments.classList.add('label');
assignments.href = "#";
labelContainer.appendChild(assignments);

const messages = document.createElement('a');
messages.textContent = "Чат";
messages.classList.add('label');
messages.href = "#";
labelContainer.appendChild(messages);

const journal = document.createElement('a');
journal.textContent = "Журнал";
journal.classList.add('label');
journal.href = "#";
labelContainer.appendChild(journal);

const settings = document.createElement('a');
settings.textContent = "Настройки";
settings.classList.add('label');
settings.href = "#";
labelContainer.appendChild(settings);

navMenu.insertBefore(labelContainer, navMenu.firstChild);

function hideNavItems() {
  if (!navMenu.classList.contains('active') && hamburger.classList.contains('active')) {
    navLink.forEach((link) => {
      link.style.opacity = '0';
    });
  } else {
    navLink.forEach((link) => {
      link.style.opacity = '1';
    });
  }
}

function showNavMenuForSmallDisplay(x) {
  if (x.matches) {
    if (navMenu.classList.contains('active') && hamburger.classList.contains('active')) {
      navMenu.classList.remove('active');
      navMenu.classList.add('hidden');
    } else {
      navMenu.classList.remove('hidden');
      navMenu.classList.add('active');
    }
  }
}

let x = window.matchMedia("(max-width: 425px)")
showNavMenuForSmallDisplay(x)
x.addListener(showNavMenuForSmallDisplay)




