/*
const popup = document.getElementById('popup-cost-c');
const checkBtn = document.getElementById('check__btn-c');
const closeBtn = document.querySelector('.popup__close-c');

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

*/
const popup1 = document.getElementById('popup-cost-c');
const checkBtn1 = document.getElementById('check__btn-c');
const closeBtn1 = document.querySelector('.popup__close-c');

// Открытие попапа
checkBtn1.addEventListener('click', () => {
    popup1.classList.add('open');
});

// Закрытие попапа
closeBtn1.addEventListener('click', (e) => {
    e.preventDefault();
    popup1.classList.remove('open');
});

// Закрытие попапа при клике вне его
window.addEventListener('click', (event) => {
    if (event.target === popup1) {
        popup1.classList.remove('open');
    }
});
