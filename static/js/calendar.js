document.addEventListener('DOMContentLoaded', function() {
    const calendarGrid = document.getElementById('calendar-grid');
    const currentMonthElement = document.getElementById('current-month');
    const prevMonthBtn = document.getElementById('prev-month');
    const nextMonthBtn = document.getElementById('next-month');
    const eventsContainer = document.getElementById('events-container');
    const eventItems = document.querySelectorAll('.event-item');
    const noEventsMessage = document.getElementById('no-events-message');
    const noEventsFilterMessage = document.getElementById('no-events-filter-message');
    const clearFilterBtn = document.getElementById('clear-filter-btn');

    let currentDate = new Date();
    let selectedDate = null;

    // Map month numbers to Spanish names
    const monthNames = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ];

    function renderCalendar(date) {
        const year = date.getFullYear();
        const month = date.getMonth();

        // Update header
        currentMonthElement.innerHTML = `
            <span class="material-symbols-outlined mr-2 text-blue-600">calendar_month</span>
            ${monthNames[month]} ${year}
        `;

        // Clear grid
        calendarGrid.innerHTML = '';

        // Get first day of the month
        const firstDay = new Date(year, month, 1).getDay();
        
        // Get number of days in the month
        const daysInMonth = new Date(year, month + 1, 0).getDate();

        // Get number of days in previous month
        const daysInPrevMonth = new Date(year, month, 0).getDate();

        // Add empty slots for previous month days
        for (let i = 0; i < firstDay; i++) {
            const dayDiv = document.createElement('div');
            dayDiv.className = 'py-2 text-gray-300';
            dayDiv.textContent = daysInPrevMonth - firstDay + 1 + i;
            calendarGrid.appendChild(dayDiv);
        }

        // Add days of the month
        const today = new Date();
        for (let i = 1; i <= daysInMonth; i++) {
            const dayDiv = document.createElement('div');
            dayDiv.className = 'py-2 rounded cursor-pointer transition-colors relative';
            dayDiv.textContent = i;

            // Check if it's today
            if (i === today.getDate() && month === today.getMonth() && year === today.getFullYear()) {
                dayDiv.classList.add('bg-blue-600', 'text-white', 'font-bold', 'shadow-md');
            } else {
                dayDiv.classList.add('hover:bg-gray-50');
            }

            // Check if it's selected
            if (selectedDate && i === selectedDate.getDate() && month === selectedDate.getMonth() && year === selectedDate.getFullYear()) {
                dayDiv.classList.add('ring-2', 'ring-blue-400', 'ring-offset-1');
            }

            // Check if there are events on this day
            const dateString = `${year}-${String(month + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`;
            const hasEvents = Array.from(eventItems).some(item => item.dataset.date === dateString);
            
            if (hasEvents) {
                const dot = document.createElement('div');
                dot.className = 'w-1.5 h-1.5 bg-blue-400 rounded-full absolute bottom-1 left-1/2 transform -translate-x-1/2';
                if (i === today.getDate() && month === today.getMonth() && year === today.getFullYear()) {
                    dot.className = 'w-1.5 h-1.5 bg-white rounded-full absolute bottom-1 left-1/2 transform -translate-x-1/2';
                }
                dayDiv.appendChild(dot);
            }

            dayDiv.addEventListener('click', () => {
                selectedDate = new Date(year, month, i);
                renderCalendar(currentDate); // Re-render to update selection style
                filterEvents(selectedDate);
            });

            calendarGrid.appendChild(dayDiv);
        }
    }

    function filterEvents(date) {
        const dateString = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
        let visibleCount = 0;

        eventItems.forEach(item => {
            if (item.dataset.date === dateString) {
                item.classList.remove('hidden');
                visibleCount++;
            } else {
                item.classList.add('hidden');
            }
        });

        // Handle messages
        if (visibleCount === 0) {
            noEventsFilterMessage.classList.remove('hidden');
            if (noEventsMessage) noEventsMessage.classList.add('hidden');
        } else {
            noEventsFilterMessage.classList.add('hidden');
            if (noEventsMessage) noEventsMessage.classList.add('hidden');
        }
    }

    function clearFilter() {
        selectedDate = null;
        renderCalendar(currentDate);
        eventItems.forEach(item => item.classList.remove('hidden'));
        noEventsFilterMessage.classList.add('hidden');
        if (eventItems.length === 0 && noEventsMessage) {
            noEventsMessage.classList.remove('hidden');
        }
    }

    // Event Listeners
    prevMonthBtn.addEventListener('click', () => {
        currentDate.setMonth(currentDate.getMonth() - 1);
        renderCalendar(currentDate);
    });

    nextMonthBtn.addEventListener('click', () => {
        currentDate.setMonth(currentDate.getMonth() + 1);
        renderCalendar(currentDate);
    });

    if (clearFilterBtn) {
        clearFilterBtn.addEventListener('click', clearFilter);
    }

    // Initial render
    renderCalendar(currentDate);
});
