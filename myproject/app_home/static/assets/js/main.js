document.addEventListener('DOMContentLoaded', () => {
    // --- Overlay Authentication ---
    const loginOverlay = document.getElementById('login-overlay');
    const registerOverlay = document.getElementById('register-overlay');
    const forgotPasswordOverlay = document.getElementById('forgot-password-overlay');
    // Sử dụng ID duy nhất cho nút kích hoạt đăng nhập ở header, ví dụ: 'header-login-trigger'
    const headerLoginTrigger = document.getElementById('header-login-trigger'); 
    const showRegisterLink = document.getElementById('show-register');
    const showLoginLink = document.getElementById('show-login');
    const showForgotPasswordLink = document.getElementById('show-forgot-password'); // Đảm bảo phần tử này tồn tại trong HTML
    const showRegisterFromForgotLink = document.getElementById('show-register-from-forgot');
    const closeLoginBtn = document.getElementById('close-login-btn'); // Đảm bảo phần tử này tồn tại trong HTML
    const closeRegisterBtn = document.getElementById('close-register-btn');
    const closeForgotPasswordBtn = document.getElementById('close-forgot-password-btn');

    // Hiển thị form đăng nhập khi nhấn nút "Đăng nhập" (nếu tồn tại)
    if (headerLoginTrigger && loginOverlay) {
        headerLoginTrigger.addEventListener('click', (e) => {
            e.preventDefault();
            loginOverlay.classList.add('active');
            if (registerOverlay) registerOverlay.classList.remove('active');
            if (forgotPasswordOverlay) forgotPasswordOverlay.classList.remove('active');
        });
    }

    // Chuyển từ form đăng nhập sang form đăng ký
    if (showRegisterLink) {
        showRegisterLink.addEventListener('click', (e) => {
            e.preventDefault();
            if (loginOverlay) loginOverlay.classList.remove('active');
            if (registerOverlay) registerOverlay.classList.add('active');
        });
    }

    // Chuyển từ form đăng ký sang form đăng nhập
    if (showLoginLink) {
        showLoginLink.addEventListener('click', (e) => {
            e.preventDefault();
            if (registerOverlay) registerOverlay.classList.remove('active');
            if (loginOverlay) loginOverlay.classList.add('active');
        });
    }

    // Chuyển từ form đăng nhập sang form quên mật khẩu
    if (showForgotPasswordLink) {
        showForgotPasswordLink.addEventListener('click', (e) => {
            e.preventDefault();
            if (loginOverlay) loginOverlay.classList.remove('active');
            if (forgotPasswordOverlay) forgotPasswordOverlay.classList.add('active');
        });
    }

    // Chuyển từ form quên mật khẩu sang form đăng ký
    if (showRegisterFromForgotLink) {
        showRegisterFromForgotLink.addEventListener('click', (e) => {
            e.preventDefault();
            if (forgotPasswordOverlay) forgotPasswordOverlay.classList.remove('active');
            if (registerOverlay) registerOverlay.classList.add('active');
        });
    }

    // Đóng form đăng nhập
    if (closeLoginBtn) {
        closeLoginBtn.addEventListener('click', () => {
            if (loginOverlay) loginOverlay.classList.remove('active');
        });
    }

    // Đóng form đăng ký
    if (closeRegisterBtn) {
        closeRegisterBtn.addEventListener('click', () => {
            if (registerOverlay) registerOverlay.classList.remove('active');
        });
    }

    // Đóng form quên mật khẩu
    if (closeForgotPasswordBtn) {
        closeForgotPasswordBtn.addEventListener('click', () => {
            if (forgotPasswordOverlay) forgotPasswordOverlay.classList.remove('active');
        });
    }

    // Đóng form khi nhấn ngoài overlay
    if (loginOverlay) {
        loginOverlay.addEventListener('click', (e) => {
            if (e.target === loginOverlay) {
                loginOverlay.classList.remove('active');
            }
        });
    }

    if (registerOverlay) {
        registerOverlay.addEventListener('click', (e) => {
            if (e.target === registerOverlay) {
                registerOverlay.classList.remove('active');
            }
        });
    }

    if (forgotPasswordOverlay) {
        forgotPasswordOverlay.addEventListener('click', (e) => {
            if (e.target === forgotPasswordOverlay) {
                forgotPasswordOverlay.classList.remove('active');
            }
        });
    }

    // --- Banner Slider ---
    const slides = document.querySelectorAll('.slide');
    const dots = document.querySelectorAll('.dot');
    let currentSlide = 0;

    if (slides.length > 0 && dots.length > 0) {
        const totalSlides = slides.length;

        function showSlide(index) {
            slides.forEach((slide, i) => {
                slide.classList.remove('active');
                if (dots[i]) dots[i].classList.remove('active');
            });
            slides[index].classList.add('active');
            if (dots[index]) dots[index].classList.add('active');
            currentSlide = index;
        }

        function autoSlide() {
            currentSlide = (currentSlide + 1) % totalSlides;
            showSlide(currentSlide);
        }

        dots.forEach((dot, index) => {
            dot.addEventListener('click', () => {
                showSlide(index);
            });
        });

        showSlide(currentSlide); // Khởi động slide đầu tiên
        setInterval(autoSlide, 5000); // Tự động chuyển slide mỗi 5 giây
    }

    // --- Products Collection Slider ---
    const productList = document.querySelector('.product-list');
    const productItems = document.querySelectorAll('.product-item');
    const prevBtn = document.querySelector('.prev-btn');
    const nextBtn = document.querySelector('.next-btn');

    if (productList && productItems.length > 0 && prevBtn && nextBtn) {
        let currentIndex = 0;
        const itemsPerView = 5; // Số sản phẩm hiển thị trên 1 lần slide
        const totalItems = productItems.length;
        let itemWidth = 0;

        function calculateItemWidth() {
            if (productItems[0]) {
                // 20 là giá trị gap giữa các item, cần đảm bảo nó khớp với CSS
                itemWidth = productItems[0].offsetWidth + 20; 
            }
        }

        function updateSlider() {
            if (itemWidth > 0) {
                productList.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
            }
        }

        calculateItemWidth(); // Tính toán ban đầu
        updateSlider(); // Cập nhật slider ban đầu

        nextBtn.addEventListener('click', () => {
            if (currentIndex < totalItems - itemsPerView) {
                currentIndex++;
                updateSlider();
            }
        });

        prevBtn.addEventListener('click', () => {
            if (currentIndex > 0) {
                currentIndex--;
                updateSlider();
            }
        });

        window.addEventListener('resize', () => {
            calculateItemWidth(); // Tính lại chiều rộng khi resize
            // Điều chỉnh currentIndex nếu cần để không bị lệch quá nhiều
            currentIndex = Math.max(0, Math.min(currentIndex, totalItems - itemsPerView));
            updateSlider();
        });
    }

    // --- Voucher Overlay ---
    const voucherOverlay = document.getElementById('voucher-overlay');
    const openVoucherBtns = document.querySelectorAll('.open-voucher-btn');
    const closeVoucherBtn = document.getElementById('close-voucher-btn');

    if (voucherOverlay) {
        if (openVoucherBtns.length > 0) {
            openVoucherBtns.forEach(button => {
                button.addEventListener('click', () => {
                    voucherOverlay.classList.add('active');
                });
            });
        }

        if (closeVoucherBtn) {
            closeVoucherBtn.addEventListener('click', () => {
                voucherOverlay.classList.remove('active');
            });
        }

        voucherOverlay.addEventListener('click', (event) => {
            // Đóng khi click vào chính overlay (phần nền), không phải nội dung bên trong
            if (event.target === voucherOverlay) {
                voucherOverlay.classList.remove('active');
            }
        });
    }
});

const userInfoBtn = document.getElementById('user-info-btn');
const userInfoOverlay = document.getElementById('user-info-overlay');

if (userInfoBtn && userInfoOverlay) {
    userInfoBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        userInfoOverlay.classList.toggle('active');
    });

    // Ẩn overlay khi click ra ngoài
    document.addEventListener('click', (e) => {
        if (!userInfoOverlay.contains(e.target) && e.target !== userInfoBtn) {
            userInfoOverlay.classList.remove('active');
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    // Login overlay
    const loginOverlay = document.getElementById('login-overlay');
    const showLoginBtn = document.getElementById('show-login-btn');
    const closeLoginBtn = document.getElementById('close-login-btn');

    if (showLoginBtn) {
        showLoginBtn.addEventListener('click', function() {
            loginOverlay.style.display = 'flex';
        });
    }

    if (closeLoginBtn) {
        closeLoginBtn.addEventListener('click', function() {
            loginOverlay.style.display = 'none';
        });
    }

    // Register overlay
    const registerOverlay = document.getElementById('register-overlay');
    const showRegisterBtn = document.getElementById('show-register-btn');
    const closeRegisterBtn = document.getElementById('close-register-btn');
    const showRegisterFromLogin = document.getElementById('show-register');
    const showLoginFromRegister = document.getElementById('show-login');

    if (showRegisterBtn) {
        showRegisterBtn.addEventListener('click', function() {
            registerOverlay.style.display = 'flex';
        });
    }

    if (closeRegisterBtn) {
        closeRegisterBtn.addEventListener('click', function() {
            registerOverlay.style.display = 'none';
        });
    }

    if (showRegisterFromLogin) {
        showRegisterFromLogin.addEventListener('click', function(e) {
            e.preventDefault();
            loginOverlay.style.display = 'none';
            registerOverlay.style.display = 'flex';
        });
    }

    if (showLoginFromRegister) {
        showLoginFromRegister.addEventListener('click', function(e) {
            e.preventDefault();
            registerOverlay.style.display = 'none';
            loginOverlay.style.display = 'flex';
        });
    }

    // Forgot password overlay
    const forgotPasswordOverlay = document.getElementById('forgot-password-overlay');
    const showForgotPasswordBtn = document.getElementById('show-forgot-password');
    const closeForgotPasswordBtn = document.getElementById('close-forgot-password-btn');
    const showRegisterFromForgot = document.getElementById('show-register-from-forgot');

    if (showForgotPasswordBtn) {
        showForgotPasswordBtn.addEventListener('click', function(e) {
            e.preventDefault();
            loginOverlay.style.display = 'none';
            forgotPasswordOverlay.style.display = 'flex';
        });
    }

    if (closeForgotPasswordBtn) {
        closeForgotPasswordBtn.addEventListener('click', function() {
            forgotPasswordOverlay.style.display = 'none';
        });
    }

    if (showRegisterFromForgot) {
        showRegisterFromForgot.addEventListener('click', function(e) {
            e.preventDefault();
            forgotPasswordOverlay.style.display = 'none';
            registerOverlay.style.display = 'flex';
        });
    }

    // Close overlays when clicking outside
    window.addEventListener('click', function(e) {
        if (e.target === loginOverlay) {
            loginOverlay.style.display = 'none';
        }
        if (e.target === registerOverlay) {
            registerOverlay.style.display = 'none';
        }
        if (e.target === forgotPasswordOverlay) {
            forgotPasswordOverlay.style.display = 'none';
        }
    });
});