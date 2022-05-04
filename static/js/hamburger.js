const header__hamburger = document.querySelector('.header__hamburger'),
      menu = document.querySelector('.accordion-mobile'),
      closeElem = document.querySelector('.accordion-mobile__close');

header__hamburger.addEventListener('click', () => {
	menu.classList.add('activeme');
        map_hamburger.classList.add('hideB');
});

closeElem.addEventListener('click', () => {
	menu.classList.remove('activeme');
        map_hamburger.classList.remove('hideB');
});

const map_hamburger = document.querySelector('.map-hamburger'),
      menu_map = document.querySelector('.wrapper-center__map_accordion'),
      closeElemMap = document.querySelector('.wrapper-center__map_accordion_close');

map_hamburger.addEventListener('click', () => {
      menu_map.classList.add('active_map');
      map_hamburger.classList.add('hideB');
});

closeElemMap.addEventListener('click', () => {
      menu_map.classList.remove('active_map');
      map_hamburger.classList.remove('hideB');
});

const district_infoMenu = document.querySelector('.district-info'); 
      closeElemMenu = document.querySelector('.district-info__close');

closeElemMenu.addEventListener('Click', () => {
      district_infoMenu.classList.remove('.active_mapMenu');
});
