// Lazy loading images
document.addEventListener('DOMContentLoaded', function() {
    // Kiểm tra xem browser có hỗ trợ Intersection Observer không
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    
                    // Nếu có data-src, load image
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.classList.remove('lazy');
                        img.classList.add('loaded');
                        observer.unobserve(img);
                    }
                    
                    // Nếu có data-srcset, load srcset
                    if (img.dataset.srcset) {
                        img.srcset = img.dataset.srcset;
                    }
                }
            });
        }, {
            rootMargin: '50px' // Load images 50px trước khi vào viewport
        });

        // Tìm tất cả images có class lazy
        const lazyImages = document.querySelectorAll('img.lazy');
        lazyImages.forEach(img => imageObserver.observe(img));
    } else {
        // Fallback cho browsers không hỗ trợ Intersection Observer
        const lazyImages = document.querySelectorAll('img.lazy');
        lazyImages.forEach(img => {
            if (img.dataset.src) {
                img.src = img.dataset.src;
            }
        });
    }
});

// Preload critical images
function preloadImage(src) {
    const link = document.createElement('link');
    link.rel = 'preload';
    link.as = 'image';
    link.href = src;
    document.head.appendChild(link);
}

