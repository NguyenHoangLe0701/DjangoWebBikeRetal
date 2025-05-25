    // Ví dụ: JS cơ bản để thêm các chấm phân trang hoặc xử lý sự kiện cuộn
document.addEventListener('DOMContentLoaded', function() {
    const container = document.querySelector('.articles-container');
    const wrapper = document.querySelector('.articles-wrapper');
    const dotsContainer = document.querySelector('.pagination-dots');

    if (!container || !wrapper || !dotsContainer) return;

    // Hàm tạo các chấm phân trang (ví dụ)
    function createPaginationDots() {
        dotsContainer.innerHTML = ''; // Xóa các chấm hiện có
        const numberOfCards = wrapper.children.length;
        // Đây là một ví dụ đơn giản; bạn sẽ cần tính toán có bao nhiêu "trang" cần thiết
        // dựa trên chiều rộng container và chiều rộng thẻ.
        const numberOfDots = Math.ceil(wrapper.scrollWidth / container.offsetWidth);
         // Đảm bảo không tạo quá nhiều chấm nếu số lượng thẻ ít và vừa với container
        const maxVisibleCards = Math.floor(container.offsetWidth / (wrapper.firstElementChild.offsetWidth + 20)); // 20px là gap
        if (numberOfCards <= maxVisibleCards) {
             dotsContainer.style.display = 'none'; // Ẩn chấm nếu không cần cuộn
             return;
        } else {
             dotsContainer.style.display = 'flex';
        }


        for (let i = 0; i < numberOfDots; i++) {
            const dot = document.createElement('span');
            dot.classList.add('pagination-dot');
            dot.dataset.index = i;
            dotsContainer.appendChild(dot);

            dot.addEventListener('click', function() {
                // Ví dụ: Cuộn đến phần tương ứng
                const sectionIndex = parseInt(this.dataset.index);
                const scrollToPosition = container.offsetWidth * sectionIndex;
                container.scrollTo({
                    left: scrollToPosition,
                    behavior: 'smooth' // Cuộn mượt
                });
            });
        }
        // Làm nổi bật chấm đầu tiên ban đầu
        if (dotsContainer.children.length > 0) {
            dotsContainer.children[0].classList.add('active');
        }
    }

    // Gọi hàm tạo chấm khi trang tải xong
    // createPaginationDots(); // Bỏ comment dòng này để thêm chấm

    // Ví dụ: Cập nhật chấm active khi cuộn (cần logic phức tạp hơn để theo dõi chính xác)
    // container.addEventListener('scroll', function() {
    //     // Tính toán phần nào đang hiển thị và cập nhật class active
    //     // Cái này yêu cầu tính toán vị trí cuộn so với vị trí các thẻ
    // });

    // Tạo lại chấm nếu thay đổi kích thước cửa sổ (tùy chọn)
    // window.addEventListener('resize', createPaginationDots);


    // Chức năng kéo để cuộn cơ bản (có nhiều cách triển khai nâng cao hơn)
    let isDragging = false;
    let startPos = 0;
    let scrollLeft = 0;

    container.addEventListener('mousedown', (e) => {
        isDragging = true;
        container.classList.add('dragging'); // Tùy chọn: thêm class để styling khi kéo
        startPos = e.pageX - container.offsetLeft;
        scrollLeft = container.scrollLeft;
    });

    container.addEventListener('mouseleave', () => {
        isDragging = false;
        container.classList.remove('dragging');
    });

    container.addEventListener('mouseup', () => {
        isDragging = false;
        container.classList.remove('dragging');
    });

    container.addEventListener('mousemove', (e) => {
        if (!isDragging) return;
        e.preventDefault(); // Ngăn chặn hành vi mặc định (ví dụ: chọn văn bản)
        const x = e.pageX - container.offsetLeft;
        const walk = (x - startPos) * 1.5; // Điều chỉnh tốc độ cuộn
        container.scrollLeft = scrollLeft - walk;
    });

     // Ngăn chặn kéo ảnh khi kéo container
    container.querySelectorAll('img').forEach(img => {
        img.addEventListener('dragstart', (e) => {
            e.preventDefault();
        });
    });
});
