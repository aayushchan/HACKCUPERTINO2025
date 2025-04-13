// Sample Items
export const sampleItems = [
    {
        id: 1,
        name: "Eco-friendly Water Bottle",
        type: "Swap",
        location: "San Francisco, CA",
        description: "Reusable stainless steel water bottle, barely used",
        price: "$15",
        link: "https://example.com/water-bottle",
        dateAdded: "2024-04-13"
    }
];

// Sustainable Marketplaces by Category
export const sustainableMarketplaces = {
    swap: [
        {
            name: "Facebook Marketplace",
            url: "https://www.facebook.com/marketplace/",
            description: "Local buying and selling platform"
        },
        {
            name: "Craigslist",
            url: "https://craigslist.org",
            description: "Community marketplace"
        }
    ],
    repair: [
        {
            name: "iFixit",
            url: "https://www.ifixit.com/",
            description: "Repair guides and parts"
        }
    ],
    recycle: [
        {
            name: "Earth911",
            url: "https://earth911.com/",
            description: "Recycling center locator"
        }
    ]
};

// Load Scraped Items from Local JSON
export async function loadScrapedItems() {
    try {
        const response = await fetch('marketplace_items.json');
        if (!response.ok) throw new Error('Failed to load items');
        const data = await response.json();
        console.log(`Loaded ${data.length} scraped items`);
        return data;
    } catch (error) {
        console.error('Error loading items:', error);
        return [];
    }
}

// Filter Items by Search and Type
export function filterItems(items, searchText, filterType) {
    if (!items) return [];

    const filtered = items.filter(item => {
        const searchMatch = !searchText ||
            item.name.toLowerCase().includes(searchText.toLowerCase()) ||
            item.description.toLowerCase().includes(searchText.toLowerCase()) ||
            item.location.toLowerCase().includes(searchText.toLowerCase());

        const typeMatch = filterType === 'All' || item.type === filterType;

        return searchMatch && typeMatch;
    });

    console.log(`Filtered ${items.length} items to ${filtered.length}`);
    return filtered;
}

// Merge Sample Items with Scraped Items
export async function getAllItems() {
    const scrapedItems = await loadScrapedItems();
    return [...sampleItems, ...scrapedItems];
}
