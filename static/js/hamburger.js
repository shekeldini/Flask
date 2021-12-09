const header__hamburger = document.querySelector('.header__hamburger'),
      menu = document.querySelector('.accordion-mobile'),
      closeElem = document.querySelector('.accordion-mobile__close');

header__hamburger.addEventListener('click', () => {
	menu.classList.add('activeme');
});

closeElem.addEventListener('click', () => {
	menu.classList.remove('activeme');
});
