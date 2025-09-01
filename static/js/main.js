// BMW Configurator JavaScript

class BMWConfigurator {
    constructor() {
        this.currentModel = null;
        this.currentConfiguration = {};
        this.basePrice = 0;
        this.totalPrice = 0;
        
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.loadSavedState();
    }
    
    bindEvents() {
        // Configuration option changes
        document.addEventListener('change', (e) => {
            if (e.target.matches('input[type="radio"], input[type="checkbox"]')) {
                this.handleOptionChange(e.target);
            }
        });
        
        // Save configuration button
        document.addEventListener('click', (e) => {
            if (e.target.matches('[data-action="save"]')) {
                this.saveConfiguration();
            }
        });
        
        // Load configuration button
        document.addEventListener('click', (e) => {
            if (e.target.matches('[data-action="load"]')) {
                this.loadConfiguration(e.target.dataset.configId);
            }
        });
        
        // Compare configurations
        document.addEventListener('click', (e) => {
            if (e.target.matches('[data-action="compare"]')) {
                this.compareConfigurations();
            }
        });
    }
    
    handleOptionChange(input) {
        const optionName = input.name;
        const optionValue = input.value;
        const optionPrice = parseFloat(input.dataset.price) || 0;
        
        if (input.type === 'radio') {
            this.currentConfiguration[optionName] = {
                value: optionValue,
                price: optionPrice
            };
        } else if (input.type === 'checkbox') {
            if (input.checked) {
                if (!this.currentConfiguration[optionName]) {
                    this.currentConfiguration[optionName] = [];
                }
                this.currentConfiguration[optionName].push({
                    value: optionValue,
                    price: optionPrice
                });
            } else {
                if (this.currentConfiguration[optionName]) {
                    this.currentConfiguration[optionName] = 
                        this.currentConfiguration[optionName].filter(item => item.value !== optionValue);
                }
            }
        }
        
        this.updatePrice();
        this.updatePreview();
        this.saveState();
    }
    
    updatePrice() {
        let total = this.basePrice;
        
        Object.keys(this.currentConfiguration).forEach(key => {
            const option = this.currentConfiguration[key];
            if (Array.isArray(option)) {
                option.forEach(item => total += item.price);
            } else {
                total += option.price;
            }
        });
        
        this.totalPrice = total;
        this.displayPrice(total);
        this.calculatePriceBreakdown();
    }
    
    displayPrice(price) {
        const priceElement = document.getElementById('totalPrice');
        if (priceElement) {
            priceElement.textContent = this.formatPrice(price);
            
            // Add animation effect
            priceElement.classList.add('price-update');
            setTimeout(() => {
                priceElement.classList.remove('price-update');
            }, 500);
        }
    }
    
    calculatePriceBreakdown() {
        const breakdown = {
            base: this.basePrice,
            options: {},
            packages: {},
            total: this.totalPrice
        };
        
        Object.keys(this.currentConfiguration).forEach(key => {
            const option = this.currentConfiguration[key];
            if (Array.isArray(option)) {
                option.forEach(item => {
                    if (key.includes('package')) {
                        breakdown.packages[item.value] = item.price;
                    } else {
                        breakdown.options[item.value] = item.price;
                    }
                });
            } else {
                if (key.includes('package')) {
                    breakdown.packages[option.value] = option.price;
                } else {
                    breakdown.options[option.value] = option.price;
                }
            }
        });
        
        this.displayPriceBreakdown(breakdown);
    }
    
    displayPriceBreakdown(breakdown) {
        const container = document.getElementById('priceBreakdown');
        if (!container) return;
        
        let html = `
            <div class="price-item">
                <span>Base Price</span>
                <span>${this.formatPrice(breakdown.base)}</span>
            </div>
        `;
        
        Object.keys(breakdown.options).forEach(option => {
            html += `
                <div class="price-item">
                    <span>${option}</span>
                    <span>+${this.formatPrice(breakdown.options[option])}</span>
                </div>
            `;
        });
        
        Object.keys(breakdown.packages).forEach(pkg => {
            html += `
                <div class="price-item">
                    <span>${pkg}</span>
                    <span>+${this.formatPrice(breakdown.packages[pkg])}</span>
                </div>
            `;
        });
        
        html += `
            <div class="price-item">
                <span><strong>Total MSRP</strong></span>
                <span><strong>${this.formatPrice(breakdown.total)}</strong></span>
            </div>
        `;
        
        container.innerHTML = html;
    }
    
    updatePreview() {
        // Update car image based on selected options
        const exteriorColor = this.getSelectedOption('exterior_color');
        const model = this.currentModel;
        
        if (exteriorColor && model) {
            const imagePath = `/static/images/${model.toLowerCase()}-${exteriorColor.toLowerCase().replace(/\s+/g, '-')}.jpg`;
            const carImage = document.getElementById('carImage');
            if (carImage) {
                carImage.src = imagePath;
                carImage.onerror = () => {
                    // Fallback to default image
                    carImage.src = `/static/images/${model.toLowerCase()}-default.jpg`;
                };
            }
        }
        
        // Update feature highlights
        this.updateFeatureHighlights();
    }
    
    updateFeatureHighlights() {
        const highlightsContainer = document.getElementById('featureHighlights');
        if (!highlightsContainer) return;
        
        const selectedFeatures = [];
        
        Object.keys(this.currentConfiguration).forEach(key => {
            const option = this.currentConfiguration[key];
            if (Array.isArray(option)) {
                option.forEach(item => selectedFeatures.push(item.value));
            } else {
                selectedFeatures.push(option.value);
            }
        });
        
        const html = selectedFeatures.map(feature => 
            `<span class="badge bg-primary me-1 mb-1">${feature}</span>`
        ).join('');
        
        highlightsContainer.innerHTML = html;
    }
    
    getSelectedOption(optionName) {
        const option = this.currentConfiguration[optionName];
        return option ? option.value : null;
    }
    
    saveConfiguration() {
        const name = prompt('Enter a name for this configuration:');
        if (!name) return;
        
        const configData = {
            name: name,
            model: this.currentModel,
            configuration: this.currentConfiguration,
            totalPrice: this.totalPrice,
            timestamp: new Date().toISOString()
        };
        
        fetch('/api/save-configuration', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(configData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                this.showNotification('Configuration saved successfully!', 'success');
            } else {
                this.showNotification('Failed to save configuration.', 'error');
            }
        })
        .catch(error => {
            console.error('Error saving configuration:', error);
            this.showNotification('Failed to save configuration.', 'error');
        });
    }
    
    loadConfiguration(configId) {
        fetch(`/api/load-configuration/${configId}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                this.currentConfiguration = data.configuration;
                this.applyConfiguration();
                this.showNotification('Configuration loaded successfully!', 'success');
            } else {
                this.showNotification('Failed to load configuration.', 'error');
            }
        })
        .catch(error => {
            console.error('Error loading configuration:', error);
            this.showNotification('Failed to load configuration.', 'error');
        });
    }
    
    applyConfiguration() {
        // Clear all current selections
        document.querySelectorAll('input[type="radio"], input[type="checkbox"]')
            .forEach(input => input.checked = false);
        
        // Apply saved configuration
        Object.keys(this.currentConfiguration).forEach(optionName => {
            const option = this.currentConfiguration[optionName];
            
            if (Array.isArray(option)) {
                option.forEach(item => {
                    const input = document.querySelector(`input[name="${optionName}"][value="${item.value}"]`);
                    if (input) input.checked = true;
                });
            } else {
                const input = document.querySelector(`input[name="${optionName}"][value="${option.value}"]`);
                if (input) input.checked = true;
            }
        });
        
        this.updatePrice();
        this.updatePreview();
    }
    
    compareConfigurations() {
        // Implementation for comparing multiple configurations
        console.log('Compare configurations feature coming soon!');
    }
    
    formatPrice(price) {
        return '$' + price.toLocaleString('en-US', {
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        });
    }
    
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show`;
        notification.style.cssText = 'position: fixed; top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 5000);
    }
    
    saveState() {
        localStorage.setItem('bmw_configurator_state', JSON.stringify({
            model: this.currentModel,
            configuration: this.currentConfiguration,
            totalPrice: this.totalPrice
        }));
    }
    
    loadSavedState() {
        const savedState = localStorage.getItem('bmw_configurator_state');
        if (savedState) {
            try {
                const state = JSON.parse(savedState);
                this.currentModel = state.model;
                this.currentConfiguration = state.configuration || {};
                this.totalPrice = state.totalPrice || this.basePrice;
            } catch (error) {
                console.error('Error loading saved state:', error);
            }
        }
    }
}

// Initialize the configurator when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.bmwConfigurator = new BMWConfigurator();
});

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = BMWConfigurator;
}
