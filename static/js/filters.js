/**
 * Generic Filter and Sort Functionality
 * Can be used for Shop, Gallery, and News pages
 */

class PageFilters {
    constructor(options) {
        this.containerId = options.containerId;
        this.itemSelector = options.itemSelector;
        this.searchInputId = options.searchInputId;
        this.categoryFilterId = options.categoryFilterId; // Can be a select or a container of buttons
        this.sortSelectId = options.sortSelectId;
        this.activeCategory = 'all';
        
        this.init();
    }

    init() {
        this.container = document.getElementById(this.containerId);
        if (!this.container) return;

        this.items = Array.from(this.container.querySelectorAll(this.itemSelector));
        
        // Search Listener
        if (this.searchInputId) {
            const searchInput = document.getElementById(this.searchInputId);
            if (searchInput) {
                searchInput.addEventListener('input', (e) => {
                    this.filterItems(e.target.value, this.activeCategory);
                });
            }
        }

        // Category Listener (if it's a select)
        if (this.categoryFilterId) {
            const categoryElement = document.getElementById(this.categoryFilterId);
            if (categoryElement) {
                if (categoryElement.tagName === 'SELECT') {
                    categoryElement.addEventListener('change', (e) => {
                        this.activeCategory = e.target.value;
                        this.filterItems(document.getElementById(this.searchInputId)?.value || '', this.activeCategory);
                    });
                } else {
                    // Assume it's a container of buttons
                    const buttons = categoryElement.querySelectorAll('[data-category]');
                    buttons.forEach(btn => {
                        btn.addEventListener('click', (e) => {
                            // Remove active class from all
                            buttons.forEach(b => {
                                b.classList.remove('bg-blue-600', 'text-white');
                                b.classList.add('bg-white', 'text-gray-600');
                            });
                            // Add active class to clicked
                            const target = e.currentTarget;
                            target.classList.remove('bg-white', 'text-gray-600');
                            target.classList.add('bg-blue-600', 'text-white');
                            
                            this.activeCategory = target.getAttribute('data-category');
                            this.filterItems(document.getElementById(this.searchInputId)?.value || '', this.activeCategory);
                        });
                    });
                }
            }
        }

        // Sort Listener
        if (this.sortSelectId) {
            const sortSelect = document.getElementById(this.sortSelectId);
            if (sortSelect) {
                sortSelect.addEventListener('change', (e) => {
                    this.sortItems(e.target.value);
                });
            }
        }
    }

    filterItems(searchTerm, category) {
        searchTerm = searchTerm.toLowerCase();
        
        this.items.forEach(item => {
            const title = item.getAttribute('data-title')?.toLowerCase() || '';
            const itemCategory = item.getAttribute('data-category') || '';
            const description = item.getAttribute('data-description')?.toLowerCase() || '';
            
            const matchesSearch = title.includes(searchTerm) || description.includes(searchTerm);
            const matchesCategory = category === 'all' || itemCategory === category;

            if (matchesSearch && matchesCategory) {
                item.classList.remove('hidden');
                item.classList.add('animate-fade-in');
            } else {
                item.classList.add('hidden');
                item.classList.remove('animate-fade-in');
            }
        });

        // Show "No results" message if needed
        this.checkEmptyState();
    }

    sortItems(criteria) {
        const sortedItems = this.items.sort((a, b) => {
            if (criteria === 'price-asc') {
                return parseFloat(a.getAttribute('data-price')) - parseFloat(b.getAttribute('data-price'));
            } else if (criteria === 'price-desc') {
                return parseFloat(b.getAttribute('data-price')) - parseFloat(a.getAttribute('data-price'));
            } else if (criteria === 'date-new') {
                return new Date(b.getAttribute('data-date')) - new Date(a.getAttribute('data-date'));
            } else if (criteria === 'date-old') {
                return new Date(a.getAttribute('data-date')) - new Date(b.getAttribute('data-date'));
            } else if (criteria === 'name-asc') {
                return a.getAttribute('data-title').localeCompare(b.getAttribute('data-title'));
            }
            return 0;
        });

        // Re-append items in new order
        sortedItems.forEach(item => this.container.appendChild(item));
    }

    checkEmptyState() {
        const visibleItems = this.items.filter(item => !item.classList.contains('hidden'));
        let emptyMsg = document.getElementById('no-results-message');
        
        if (visibleItems.length === 0) {
            if (!emptyMsg) {
                emptyMsg = document.createElement('div');
                emptyMsg.id = 'no-results-message';
                emptyMsg.className = 'col-span-full text-center py-12';
                emptyMsg.innerHTML = `
                    <span class="material-symbols-outlined text-4xl text-gray-300 mb-2">search_off</span>
                    <p class="text-gray-500">No se encontraron resultados.</p>
                `;
                this.container.appendChild(emptyMsg);
            }
            emptyMsg.classList.remove('hidden');
        } else {
            if (emptyMsg) {
                emptyMsg.classList.add('hidden');
            }
        }
    }
}
