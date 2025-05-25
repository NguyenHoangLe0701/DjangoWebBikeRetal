document.addEventListener('DOMContentLoaded', function () {
    const swiper = new Swiper('.store-slider', {
        // Optional parameters
        slidesPerView: 1, // Hiển thị 1 slide mỗi lần trên màn hình nhỏ
        spaceBetween: 20, // Khoảng cách giữa các slide
        loop: true, // Lặp lại slide

        // Pagination
        pagination: {
            el: '.swiper-pagination',
            clickable: true, // Cho phép click vào chấm tròn để chuyển slide
        },

        // Navigation arrows (tùy chọn, nếu bạn muốn thêm nút next/prev)
        // navigation: {
        //   nextEl: '.swiper-button-next',
        //   prevEl: '.swiper-button-prev',
        // },

        // Breakpoints (responsive)
        // Điều chỉnh số lượng slide hiển thị trên các kích thước màn hình khác nhau
        breakpoints: {
            // when window width is >= 640px
            640: {
                slidesPerView: 2,
                spaceBetween: 20
            },
            // when window width is >= 768px
            768: {
                slidesPerView: 2,
                spaceBetween: 30
            },
            // when window width is >= 1024px
            1024: {
                slidesPerView: 3, // Hiển thị 3 slide trên màn hình lớn hơn hoặc bằng 1024px
                spaceBetween: 30
            }
        }
    });
});