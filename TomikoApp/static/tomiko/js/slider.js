const swiper = new Swiper('.swiper', {
    slidesPerView: 4,               // Количество видимых карточек
    spaceBetween: 20,               // Расстояние между карточками
    navigation: {
        nextEl: '.swiper-button-next',  // Элементы для переключения
        prevEl: '.swiper-button-prev',
    },
    loop: false,                     

    on: {
        slideChangeTransitionEnd: function () {
            
            document.querySelectorAll('.swiper-slide').forEach(slide => {
                slide.classList.remove('big');
            });

            
            const visibleSlides = swiper.slides.slice(swiper.activeIndex, swiper.activeIndex + swiper.params.slidesPerView);
            if (visibleSlides[0]) {
                visibleSlides[0].classList.add('big');
            }
        },
    },
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
