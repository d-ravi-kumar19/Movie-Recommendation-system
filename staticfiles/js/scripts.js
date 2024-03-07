$(document).ready(function () {
    // Add scrollspy to the navbar
    $('nav').scrollspy({ target: '#navbarNav' });

    // Add smooth scrolling to all links
    $('a').on('click', function (event) {
        if (this.hash !== '') {
            event.preventDefault();
            var hash = this.hash;
            $('html, body').animate(
                {
                    scrollTop: $(hash).offset().top
                },
                800
            );
        }
    });

    // Add sticky navbar
    $(window).scroll(function () {
        if ($(this).scrollTop() > 56) {
            $('#header').addClass('sticky');
        } else {
            $('#header').removeClass('sticky');
        }
    });

    // Initialize Swiper for Top English Movies
    var swiper = new Swiper('.swiper-container', {
        slidesPerView: 5,
        spaceBetween: 20,
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
    });

    // Initialize Swiper for Top Hindi Movies
    var swiperHindi = new Swiper('.swiper-container', {
        slidesPerView: 5,
        spaceBetween: 20,
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
    });

    // Initialize Swiper for Top Romance Movies
    var swiperRomance = new Swiper('#carouselTopRomanceMovies', {
        slidesPerView: 5,
        spaceBetween: 10,
        navigation: {
            nextEl: '.carousel-control-next',
            prevEl: '.carousel-control-prev',
        },
    });
});

const watchedCheckbox = document.getElementById('watchedCheckbox');
const favoriteCheckbox = document.getElementById('favoriteCheckbox');
const updateStatusButton = document.getElementById('updateStatusButton');

watchedCheckbox.addEventListener('change', () => {
    updateStatusButton.click();
});

favoriteCheckbox.addEventListener('change', () => {
    updateStatusButton.click();
});

updateStatusButton.addEventListener('click', (event) => {
    event.preventDefault();
    const form = document.getElementById('statusForm');
    const formData = new FormData(form);

    const statusCheckbox = document.getElementsByName('statusCheckbox');
    const statuses = [];
    for (let i = 0; i < statusCheckbox.length; i++) {
        statuses.push(statusCheckbox[i].value);
    }

    if (statuses.includes('watched')) {
        formData.append('watched', 'watched');
    } else {
        formData.append('watched', 'unwatched');
    }

    if (statuses.includes('favorite')) {
        formData.append('favorite', 'favorite');
    } else {
        formData.append('favorite', 'unfavorite');
    }

    fetch('{% url "update_status" %}', {
        method: 'POST',
        body: formData,
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
});

document.addEventListener('DOMContentLoaded', function () {
    const searchIcon = document.getElementById('searchIcon');
    const searchPopup = document.getElementById('searchPopup');

    searchIcon.addEventListener('click', function () {
        searchPopup.style.display = (searchPopup.style.display === 'block') ? 'none' : 'block';
    });

    window.addEventListener('click', function (event) {
        if (event.target !== searchIcon && event.target !== searchPopup) {
            searchPopup.style.display = 'none';
        }
    });
});
