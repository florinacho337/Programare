$(document).ready(function () {
    const slides = $('.slide');
    let currentIndex = 0;

    setInterval(function () {
        currentIndex = (currentIndex + 1) % slides.length;
        slides.removeClass('active').eq(currentIndex).addClass('active');
    }, 3000);

    $('#prev', '#next').on('click', function () {
        currentIndex = (currentIndex + $(this).is('#prev') ? -1 : 1 + slides.length) % slides.length;
        slides.removeClass('active').eq(currentIndex).addClass('active');
    });
});