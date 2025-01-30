const popup = document.getElementById('popup');
const checkBtn = document.getElementById('check__btn');
const closeBtn = document.querySelector('.popup__close');

// Открытие попапа
checkBtn.addEventListener('click', () => {
    popup.classList.add('open');
});

// Закрытие попапа
closeBtn.addEventListener('click', (e) => {
    e.preventDefault();
    popup.classList.remove('open');
});

// Закрытие попапа при клике вне его
window.addEventListener('click', (event) => {
    if (event.target === popup) {
        popup.classList.remove('open');
    }
});


// Слайдер
const sliders = document.querySelectorAll('.slider-wrapper');
const swiper = new Swiper('.swiper', {
    slidesPerView: 4,               // Количество видимых карточек
    spaceBetween: 20,               // Расстояние между карточками

    loop: false,
<<<<<<< HEAD
=======

>>>>>>> 972de62e93b15d3f2a0fd376b5386b636bccf64e
    navigation: {
        nextEl: '.swiper-button-next',  // Элементы для переключения
        prevEl: '.swiper-button-prev',
    },

<<<<<<< HEAD
    on: {
        slideChangeTransitionEnd: function () {

=======

    on: {
        slideChangeTransitionEnd: function () {
>>>>>>> 972de62e93b15d3f2a0fd376b5386b636bccf64e
            document.querySelectorAll('.swiper-slide').forEach(slide => {
                slide.classList.remove('big');
            });

<<<<<<< HEAD

=======
>>>>>>> 972de62e93b15d3f2a0fd376b5386b636bccf64e
            const visibleSlides = swiper.slides.slice(swiper.activeIndex, swiper.activeIndex + swiper.params.slidesPerView);
            if (visibleSlides[0]) {
                visibleSlides[0].classList.add('big');
            }
        },
    },
});

<<<<<<< HEAD
const swiperVideo = new Swiper('.swiper-clips', {
    loop: false,
    slidesPerView: 9,
    spaceBetween: 1,
=======

const swiperVideo = new Swiper('.swiper-clips', {
    loop: true,
>>>>>>> 972de62e93b15d3f2a0fd376b5386b636bccf64e
    slidesPerView: 9,
    spaceBetween: 40,
    freeMode: true,
    loop: 'true',
    mousewheel: {
        forceToAxis: true
    },
    wrapperClass: 'swiper-wrapper',
    slideClass: 'swiper-slide-clip',
    
    
});

var swiperMedia = new Swiper('.media-swiper', {
    direction: 'horizontal',
    loop: false,
    slidesPerView: 4, // Количество слайдов, видимых одновременно
    spaceBetween: 16, // Расстояние между слайдами
    grid: {
        rows: 2,        // Только для отзывов!
        fill: "row"    // Заполнение сверху вниз
    },

    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },
<<<<<<< HEAD

=======
>>>>>>> 972de62e93b15d3f2a0fd376b5386b636bccf64e
});






















/*Слайдер 

let currentIndex = 0;
const items = document.querySelectorAll('.card-item');
const totalItems = items.length;

function showSlide(index) {
    items.forEach((item, i) => {
        item.style.display = (i === index) ? 'block' : 'none';
    });
}

function changeSlide(direction) {
    currentIndex = (currentIndex + direction + totalItems) % totalItems;
    showSlide(currentIndex);
}


showSlide(currentIndex);


document.querySelector('.slider-btn__left').addEventListener('click', () => changeSlide(-1));
document.querySelector('.slider-btn__right').addEventListener('click', () => changeSlide(1));
*/
