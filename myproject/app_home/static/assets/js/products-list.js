document.addEventListener('DOMContentLoaded', () => {
    const productList = document.querySelector('.product-list');
    const prevButton = document.querySelector('.prev-button');
    const nextButton = document.querySelector('.next-button');
    
    const itemWidth = 680 + 380 * 2 + 20 * 2; // Tổng chiều rộng của 3 sản phẩm
    const totalItems = productList.children.length - 1; // Trừ 1 container .product-items
    const visibleItems = 3;
    let currentIndex = 0;

    function updateButtons() {
        prevButton.disabled = currentIndex === 0;
        nextButton.disabled = currentIndex >= totalItems - visibleItems;
        prevButton.style.opacity = currentIndex === 0 ? 0.5 : 1;
        nextButton.style.opacity = currentIndex >= totalItems - visibleItems ? 0.5 : 1;
    }

    function slide() {
        const offset = -currentIndex * (itemWidth / visibleItems);
        productList.style.transform = `translateX(${offset}px)`;
        updateButtons();
    }

    nextButton.addEventListener('click', () => {
        if (currentIndex < totalItems - visibleItems) {
            currentIndex++;
            slide();
        }
    });

    prevButton.addEventListener('click', () => {
        if (currentIndex > 0) {
            currentIndex--;
            slide();
        }
    });

    updateButtons();
});