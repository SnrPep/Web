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



