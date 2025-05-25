function showShopInfo(element) {
    const address = element.getAttribute('data-address');
    const shopName = element.querySelector('.shop-name').textContent;
    const iframeHtml = element.getAttribute('data-iframe');
    
    // Tạo element tạm để parse iframe HTML
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = iframeHtml;
    const iframeSrc = tempDiv.querySelector('iframe').src;

    // Cập nhật thông tin
    document.getElementById('shop-info').innerHTML = `
        <h3>${shopName}</h3>
        <p>${address}</p>
        <p>Hotline: 1800 9473</p>
        <p>Giờ mở cửa: 09:00 - 21:00 (Thứ 2 - Chủ nhật)</p>
        <div class="rating">
            <span>5.0 ★★★★★</span> <span>2 bài viết</span>
            <a href="#" onclick="showMapOverlay()">Xem bản đồ lộ trình</a>
        </div>
    `;

    // Cập nhật iframe
    const mapIframe = document.querySelector('#map-iframe iframe');
    if (mapIframe) {
        mapIframe.src = iframeSrc;
    } else {
        const newIframe = document.createElement('iframe');
        newIframe.src = iframeSrc;
        newIframe.width = "100%";
        newIframe.height = "450";
        newIframe.style.border = "0";
        document.getElementById('map-iframe').appendChild(newIframe);
    }

    // Cập nhật địa chỉ
    document.getElementById('map-address').textContent = `Địa chỉ: ${address}`;

    // Đánh dấu cửa hàng được chọn
    document.querySelectorAll('.shop-item').forEach(item => {
        item.classList.remove('selected');
    });
    element.classList.add('selected');
}

function searchShops() {
    const province = document.getElementById('province').value;
    const district = document.getElementById('district').value;
    const searchQuery = document.getElementById('search-input').value.toLowerCase();
    console.log(`Tìm kiếm: Tỉnh=${province}, Quận/Huyện=${district}, Từ khóa=${searchQuery}`);
}

function showMapOverlay() {
    const overlay = document.getElementById('map-overlay');
    if (overlay) {
        overlay.style.display = 'flex';
    }
}

function closeMapOverlay() {
    const overlay = document.getElementById('map-overlay');
    if (overlay) {
        overlay.style.display = 'none';
    }
}

// Khởi tạo mặc định
document.addEventListener('DOMContentLoaded', () => {
    const firstShop = document.querySelector('.shop-item');
    if (firstShop) {
        firstShop.classList.add('selected');
        showShopInfo(firstShop);
    }
});

//
function filterShops() {
    const province = document.getElementById('province').value.toLowerCase();
    const district = document.getElementById('district').value.toLowerCase();
    const query = document.getElementById('search-input').value.toLowerCase();
    
    document.querySelectorAll('.shop-item').forEach(item => {
        const address = item.dataset.address.toLowerCase();
        const matchProvince = province ? address.includes(province) : true;
        const matchDistrict = district ? address.includes(district) : true;
        const matchQuery = query ? address.includes(query) || item.textContent.toLowerCase().includes(query) : true;
        
        item.style.display = (matchProvince && matchDistrict && matchQuery) ? 'block' : 'none';
    });
}

// Gán sự kiện
document.getElementById('province').addEventListener('change', filterShops);
document.getElementById('district').addEventListener('change', filterShops);
document.getElementById('search-input').addEventListener('input', filterShops);