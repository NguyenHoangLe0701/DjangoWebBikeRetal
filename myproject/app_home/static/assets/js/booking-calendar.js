/**
 * Booking Calendar Component
 * Visual calendar for selecting rental dates with availability checking
 */

class BookingCalendar {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        if (!this.container) {
            console.error(`Container #${containerId} not found`);
            return;
        }
        
        this.options = {
            bikeId: options.bikeId || null,
            bikeType: options.bikeType || null,
            quantity: options.quantity || 1,
            minDate: options.minDate || new Date(),
            maxDate: options.maxDate || null,
            onDateSelect: options.onDateSelect || null,
            pickupDate: options.pickupDate || null,
            returnDate: options.returnDate || null,
            ...options
        };
        
        this.currentDate = new Date();
        this.selectedPickupDate = this.options.pickupDate ? new Date(this.options.pickupDate) : null;
        this.selectedReturnDate = this.options.returnDate ? new Date(this.options.returnDate) : null;
        this.availabilityData = {};
        this.mode = 'pickup'; // 'pickup' or 'return'
        
        this.init();
    }
    
    init() {
        this.render();
        this.loadAvailability();
        this.attachEventListeners();
    }
    
    render() {
        const year = this.currentDate.getFullYear();
        const month = this.currentDate.getMonth();
        
        this.container.innerHTML = `
            <div class="booking-calendar">
                <div class="calendar-header">
                    <button class="calendar-nav-btn prev-month" type="button">
                        <i class="fa-solid fa-chevron-left"></i>
                    </button>
                    <div class="calendar-month-year">
                        <span class="month-name">${this.getMonthName(month)}</span>
                        <span class="year">${year}</span>
                    </div>
                    <button class="calendar-nav-btn next-month" type="button">
                        <i class="fa-solid fa-chevron-right"></i>
                    </button>
                </div>
                <div class="calendar-weekdays">
                    ${['CN', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7'].map(day => 
                        `<div class="weekday">${day}</div>`
                    ).join('')}
                </div>
                <div class="calendar-days" id="calendar-days-${this.container.id}">
                    ${this.renderDays(year, month)}
                </div>
                <div class="calendar-legend">
                    <div class="legend-item">
                        <span class="legend-color available"></span>
                        <span>Còn hàng</span>
                    </div>
                    <div class="legend-item">
                        <span class="legend-color low-stock"></span>
                        <span>Sắp hết</span>
                    </div>
                    <div class="legend-item">
                        <span class="legend-color unavailable"></span>
                        <span>Hết hàng</span>
                    </div>
                    <div class="legend-item">
                        <span class="legend-color selected"></span>
                        <span>Đã chọn</span>
                    </div>
                </div>
            </div>
        `;
    }
    
    renderDays(year, month) {
        const firstDay = new Date(year, month, 1);
        const lastDay = new Date(year, month + 1, 0);
        const daysInMonth = lastDay.getDate();
        const startingDayOfWeek = firstDay.getDay();
        
        let html = '';
        
        // Empty cells for days before month starts
        for (let i = 0; i < startingDayOfWeek; i++) {
            html += '<div class="calendar-day empty"></div>';
        }
        
        // Days of the month
        for (let day = 1; day <= daysInMonth; day++) {
            const date = new Date(year, month, day);
            const dateStr = this.formatDate(date);
            const availability = this.availabilityData[dateStr] || {};
            
            let classes = ['calendar-day'];
            let tooltip = '';
            
            // Check if date is in the past
            if (date < this.options.minDate) {
                classes.push('disabled');
            }
            // Check availability
            else if (availability.is_out_of_stock) {
                classes.push('unavailable');
                tooltip = `Hết hàng (${availability.rented_count}/${this.getTotalQuantity()} đã thuê)`;
            }
            else if (availability.is_low_stock) {
                classes.push('low-stock');
                tooltip = `Còn ${availability.available_count} xe`;
            }
            else if (availability.is_available) {
                classes.push('available');
                tooltip = `Còn ${availability.available_count} xe`;
            }
            
            // Check if selected
            if (this.isDateSelected(date)) {
                classes.push('selected');
            }
            
            // Check if in range
            if (this.isDateInRange(date)) {
                classes.push('in-range');
            }
            
            html += `
                <div class="${classes.join(' ')}" 
                     data-date="${dateStr}"
                     ${tooltip ? `title="${tooltip}"` : ''}>
                    <span class="day-number">${day}</span>
                    ${availability.available_count !== undefined ? 
                        `<span class="availability-badge">${availability.available_count}</span>` : ''}
                </div>
            `;
        }
        
        return html;
    }
    
    isDateSelected(date) {
        const dateStr = this.formatDate(date);
        return (this.selectedPickupDate && this.formatDate(this.selectedPickupDate) === dateStr) ||
               (this.selectedReturnDate && this.formatDate(this.selectedReturnDate) === dateStr);
    }
    
    isDateInRange(date) {
        if (!this.selectedPickupDate || !this.selectedReturnDate) {
            return false;
        }
        const dateStr = this.formatDate(date);
        const pickupStr = this.formatDate(this.selectedPickupDate);
        const returnStr = this.formatDate(this.selectedReturnDate);
        return dateStr > pickupStr && dateStr < returnStr;
    }
    
    formatDate(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }
    
    getMonthName(month) {
        const months = [
            'Tháng 1', 'Tháng 2', 'Tháng 3', 'Tháng 4', 'Tháng 5', 'Tháng 6',
            'Tháng 7', 'Tháng 8', 'Tháng 9', 'Tháng 10', 'Tháng 11', 'Tháng 12'
        ];
        return months[month];
    }
    
    getTotalQuantity() {
        // This should be fetched from API, for now return a default
        return Object.values(this.availabilityData)[0]?.total_quantity || 0;
    }
    
    async loadAvailability() {
        const year = this.currentDate.getFullYear();
        const month = this.currentDate.getMonth() + 1;
        const monthStr = `${year}-${String(month).padStart(2, '0')}`;
        
        const params = new URLSearchParams({
            month: monthStr,
            quantity: this.options.quantity
        });
        
        if (this.options.bikeId) {
            params.append('bike_id', this.options.bikeId);
        } else if (this.options.bikeType) {
            params.append('bike_type', this.options.bikeType);
        }
        
        try {
            const response = await fetch(`/api/bikes/calendar-availability/?${params}`);
            const data = await response.json();
            
            if (data.status === 'success') {
                this.availabilityData = data.calendar_data;
                this.render();
            }
        } catch (error) {
            console.error('Error loading availability:', error);
        }
    }
    
    attachEventListeners() {
        // Previous/Next month
        const prevBtn = this.container.querySelector('.prev-month');
        const nextBtn = this.container.querySelector('.next-month');
        
        if (prevBtn) {
            prevBtn.addEventListener('click', () => {
                this.currentDate.setMonth(this.currentDate.getMonth() - 1);
                this.loadAvailability();
            });
        }
        
        if (nextBtn) {
            nextBtn.addEventListener('click', () => {
                this.currentDate.setMonth(this.currentDate.getMonth() + 1);
                this.loadAvailability();
            });
        }
        
        // Day clicks
        const daysContainer = this.container.querySelector(`#calendar-days-${this.container.id}`);
        if (daysContainer) {
            daysContainer.addEventListener('click', (e) => {
                const dayElement = e.target.closest('.calendar-day');
                if (!dayElement || dayElement.classList.contains('empty') || dayElement.classList.contains('disabled')) {
                    return;
                }
                
                const dateStr = dayElement.getAttribute('data-date');
                const date = new Date(dateStr);
                
                if (this.options.onDateSelect) {
                    this.options.onDateSelect(date, dateStr, this.mode);
                }
            });
        }
    }
    
    setMode(mode) {
        this.mode = mode;
    }
    
    setPickupDate(date) {
        this.selectedPickupDate = date;
        this.render();
    }
    
    setReturnDate(date) {
        this.selectedReturnDate = date;
        this.render();
    }
    
    updateQuantity(quantity) {
        this.options.quantity = quantity;
        this.loadAvailability();
    }
}

// Export for use in other scripts
if (typeof window !== 'undefined') {
    window.BookingCalendar = BookingCalendar;
}

