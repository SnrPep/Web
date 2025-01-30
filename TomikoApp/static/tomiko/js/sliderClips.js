const swiperVideo = new Swiper('.swiper_clip', {
    loop: false,
    slidesPerView: 'auto',
    spaceBetween: 40,
    freeMode: true,
    mousewheel: {
        forceToAxis: true
    },
    wrapperClass: 'swiper-wrapper',
    slideClass: 'swiper-slide-clip',
    noSwiping: true
});