import { sustainableMarketplaces, getAllItems } from './data.js';

export class ItemManager {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.items = [];
        this.marketplaces = sustainableMarketplaces;
        this.handleUpload = this.handleUpload.bind(this);
        this.init();
        this.setupEventListeners();

        // Auto-refresh every 5 minutes
        this.autoRefresh = setInterval(async () => {
            await this.loadItems();
            this.renderItems(this.items);
        }, 300000);
    }

    async init() {
        await this.loadItems();
        this.renderItems(this.items);
    }

    async loadItems() {
        const allItems = await getAllItems();
        const storedItems = this.loadFromLocalStorage();
        this.items = [...allItems, ...storedItems];
    }

    filterItems() {
        const searchInput = document.getElementById('searchInput');
        const filterType = document.getElementById('filterType');
        
        if (!searchInput || !filterType) return;

        const searchText = searchInput.value.toLowerCase();
        const filterValue = filterType.value;

        const filteredItems = this.items.filter(item => {
            const matchesSearch = 
                item.name.toLowerCase().includes(searchText) ||
                item.description.toLowerCase().includes(searchText) ||
                item.location.toLowerCase().includes(searchText);

            const matchesType = filterValue === 'All' || item.type === filterValue;

            return matchesSearch && matchesType;
        });

        console.log(`Filtered ${this.items.length} items to ${filteredItems.length}`);
        this.renderItems(filteredItems);
    }

    setupEventListeners() {
        const searchInput = document.getElementById('searchInput');
        const filterType = document.getElementById('filterType');

        if (searchInput) {
            searchInput.addEventListener('input', () => {
                this.filterItems();
            });
        }

        if (filterType) {
            filterType.addEventListener('change', () => {
                this.filterItems();
            });
        }
    }

    handleUpload() {
        const name = document.getElementById('itemName').value;
        const type = document.getElementById('itemType').value;
        const description = document.getElementById('itemDescription').value;
        const location = document.getElementById('itemLocation').value;
        const price = document.getElementById('itemPrice').value;
        const link = document.getElementById('itemLink').value;

        if (!name || !type || !description || !location || !price || !link) {
            alert('Please fill in all fields');
            return;
        }

        const newItem = {
            id: Date.now(),
            name,
            type,
            description,
            location,
            price,
            link,
            dateAdded: new Date().toISOString().split('T')[0],
            source: 'user'
        };

        this.items.push(newItem);
        this.saveToLocalStorage();
        this.renderItems(this.items);

        // Clear form
        document.querySelectorAll('.upload-form input, .upload-form select').forEach(
            input => input.value = ''
        );
    }

    renderItems(items) {
        this.container.innerHTML = '';
        items.forEach(item => {
            const itemElement = this.createItemElement(item);
            this.container.appendChild(itemElement);
        });
    }

    createItemElement(item) {
        const div = document.createElement('div');
        div.className = 'item-card';
        div.innerHTML = `
            <h3>${item.name}</h3>
            <p><strong>Type:</strong> ${item.type}</p>
            <p><strong>Location:</strong> ${item.location}</p>
            <p><strong>Description:</strong> ${item.description}</p>
            <p><strong>Price:</strong> ${item.price}</p>
            <p><strong>Date Added:</strong> ${item.dateAdded}</p>
            <a href="${item.link}" target="_blank" class="btn">View Details</a>
        `;
        return div;
    }

    saveToLocalStorage() {
        const itemsToSave = this.items.filter(item => item.source === 'user');
        localStorage.setItem('items', JSON.stringify(itemsToSave));
    }

    loadFromLocalStorage() {
        const stored = localStorage.getItem('items');
        return stored ? JSON.parse(stored) : [];
    }
}