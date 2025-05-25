document.addEventListener('DOMContentLoaded', () => {
    const slider = document.querySelector('.product-list');
    const prevBtn = document.querySelector('.slider-prev');
    const nextBtn = document.querySelector('.slider-next');
    const cardWidth = 320; // Chiều rộng thẻ (256px) + khoảng cách (20px)
    const cards = document.querySelectorAll('.product-card');
    const cardsPerView = 4; // Số thẻ hiển thị trên màn hình

    let currentPosition = 0;
    const totalCards = cards.length;
    const maxScroll = -(totalCards - cardsPerView) * cardWidth; // Giới hạn cuộn tối đa

    // Xử lý nút Previous
    prevBtn.addEventListener('click', () => {
        if (currentPosition < 0) {
            currentPosition += cardWidth;
            slider.style.transform = `translateX(${currentPosition}px)`;
            updateButtons();
        }
    });

    // Xử lý nút Next
    nextBtn.addEventListener('click', () => {
        if (currentPosition > maxScroll) {
            currentPosition -= cardWidth;
            slider.style.transform = `translateX(${currentPosition}px)`;
            updateButtons();
        }
    });

    // Cập nhật trạng thái nút (không thay đổi opacity, chỉ điều chỉnh pointerEvents)
    const updateButtons = () => {
        prevBtn.style.pointerEvents = currentPosition < 0 ? 'auto' : 'none'; // Vô hiệu hóa nếu không thể nhấn
        nextBtn.style.pointerEvents = currentPosition > maxScroll ? 'auto' : 'none'; // Vô hiệu hóa nếu không thể nhấn
    };

    // Cập nhật trạng thái ban đầu
    updateButtons();

    // Cập nhật khi thay đổi kích thước màn hình
    window.addEventListener('resize', () => {
        const newMaxScroll = -(totalCards - cardsPerView) * cardWidth;
        currentPosition = Math.min(0, Math.max(currentPosition, newMaxScroll));
        slider.style.transform = `translateX(${currentPosition}px)`;
        updateButtons();
    });
});


//Video 
document.addEventListener('DOMContentLoaded', () => {
    const playButtons = document.querySelectorAll('.play-button');
    const videoOverlay = document.getElementById('videoOverlay');
    const videoFrame = document.getElementById('videoFrame');
    const closeButton = document.getElementById('closeButton');
    const videoTitle = document.getElementById('videoTitle');

    // Mở overlay khi nhấn nút play
    playButtons.forEach(button => {
        button.addEventListener('click', () => {
            let videoUrl = button.getAttribute('data-video');
            const title = button.getAttribute('data-title');

            // Chuyển đổi URL từ dạng youtu.be sang dạng nhúng
            if (videoUrl.includes('youtu.be')) {
                const videoId = videoUrl.split('youtu.be/')[1].split('?')[0];
                videoUrl = `https://www.youtube.com/embed/${videoId}`;
            }

            videoFrame.setAttribute('src', videoUrl + '?autoplay=1');
            videoTitle.textContent = title;
            videoOverlay.style.display = 'flex';
            document.body.style.overflow = 'hidden';
        });
    });

    // Đóng overlay khi nhấn nút đóng
    closeButton.addEventListener('click', () => {
        videoOverlay.style.display = 'none';
        videoFrame.setAttribute('src', ''); // Dừng video
        document.body.style.overflow = 'auto'; // Cho phép cuộn lại
    });

    // Đóng overlay khi nhấn ngoài video
    videoOverlay.addEventListener('click', (e) => {
        if (e.target === videoOverlay) {
            videoOverlay.style.display = 'none';
            videoFrame.setAttribute('src', ''); // Dừng video
            document.body.style.overflow = 'auto';
        }
    });
});