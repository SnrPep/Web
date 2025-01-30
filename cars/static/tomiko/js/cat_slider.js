var swiper = new Swiper('.swiper', {
    slidesPerView: "auto",
    spaceBetween: 20,
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },
    loop: false,

    on: {
        slideChangeTransitionEnd: function () {
            document.querySelectorAll('.swiper-slide').forEach(slide => {
                slide.classList.remove('big');
            });

            const visibleSlides = Array.from(swiper.slides).slice(swiper.activeIndex, swiper.activeIndex + swiper.params.slidesPerView);
            if (visibleSlides[0]) {
                visibleSlides[0].classList.add('big');
            }
        },
    },
});
