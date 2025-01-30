var gallerySwiper = new Swiper('.gallery-top', {
    slidesPerView: 1,
    spaceBetween: 10,
    loop: true,
    navigation: {
        nextEl: '.gallery-next',
        prevEl: '.gallery-prev',
    }
});

var popularSwiper = new Swiper('.swiper', {
    slidesPerView: "auto",
    spaceBetween: 16,
    navigation: {
        nextEl: '.popular-next',
        prevEl: '.popular-prev',
    },
    loop: false,

    on: {
        slideChangeTransitionEnd: function () {
            document.querySelectorAll('.swiper-slide').forEach(slide => {
                slide.classList.remove('big');
            });

            const visibleSlides = Array.from(popularSwiper.slides).slice(popularSwiper.activeIndex, popularSwiper.activeIndex + popularSwiper.params.slidesPerView);
            if (visibleSlides[0]) {
                visibleSlides[0].classList.add('big');
            }
        },
    },
});
