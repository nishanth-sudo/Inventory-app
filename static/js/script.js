// Inventory Management System JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        if (!alert.querySelector('.btn-close')) return;
        
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Form validation enhancements
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            // Only prevent submission if there are actual validation errors
            // Don't prevent submission for missing required fields if they're not critical
            const requiredFields = form.querySelectorAll('[required]');
            let hasErrors = false;
            
            requiredFields.forEach(function(field) {
                if (!field.value.trim()) {
                    hasErrors = true;
                }
            });
            
            if (hasErrors) {
                event.preventDefault();
                event.stopPropagation();
                form.classList.add('was-validated');
            }
        });
    });

    // Confirm delete actions
    const deleteButtons = document.querySelectorAll('[onclick*="confirm"]');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            if (!confirm('Are you sure you want to delete this item?')) {
                event.preventDefault();
            }
        });
    });

    // Movement form validation
    const movementForm = document.querySelector('form[action*="movement"]');
    if (movementForm) {
        const fromLocation = document.getElementById('from_location');
        const toLocation = document.getElementById('to_location');
        
        if (fromLocation && toLocation) {
            function validateMovementForm() {
                const fromValue = fromLocation.value;
                const toValue = toLocation.value;
                
                if (!fromValue && !toValue) {
                    fromLocation.setCustomValidity('Either From Location or To Location must be specified');
                    toLocation.setCustomValidity('Either From Location or To Location must be specified');
                } else if (fromValue === toValue && fromValue !== '') {
                    fromLocation.setCustomValidity('From Location and To Location cannot be the same');
                    toLocation.setCustomValidity('From Location and To Location cannot be the same');
                } else {
                    fromLocation.setCustomValidity('');
                    toLocation.setCustomValidity('');
                }
            }
            
            fromLocation.addEventListener('change', validateMovementForm);
            toLocation.addEventListener('change', validateMovementForm);
        }
    }

    // Search functionality for tables
    const searchInputs = document.querySelectorAll('.table-search');
    searchInputs.forEach(function(input) {
        input.addEventListener('keyup', function() {
            const filter = this.value.toLowerCase();
            const table = this.closest('.card').querySelector('table');
            const rows = table.querySelectorAll('tbody tr');
            
            rows.forEach(function(row) {
                const text = row.textContent.toLowerCase();
                if (text.indexOf(filter) > -1) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    });

    // Add search functionality to tables
    const tables = document.querySelectorAll('.table-responsive');
    tables.forEach(function(tableContainer) {
        const table = tableContainer.querySelector('table');
        if (!table || !table.querySelector('thead')) return;
        
        const thead = table.querySelector('thead');
        const searchRow = document.createElement('tr');
        searchRow.className = 'table-search-row bg-light';
        
        // Add search input for each column
        const headerCells = thead.querySelectorAll('th');
        headerCells.forEach(function(headerCell) {
            const searchCell = document.createElement('th');
            const searchInput = document.createElement('input');
            searchInput.type = 'text';
            searchInput.className = 'form-control form-control-sm table-search';
            searchInput.placeholder = 'Search...';
            searchCell.appendChild(searchInput);
            searchRow.appendChild(searchCell);
        });
        
        thead.appendChild(searchRow);
        
        // Add search functionality
        const searchInputs = searchRow.querySelectorAll('.table-search');
        searchInputs.forEach(function(input, index) {
            input.addEventListener('keyup', function() {
                const filter = this.value.toLowerCase();
                const rows = table.querySelectorAll('tbody tr');
                
                rows.forEach(function(row) {
                    const cell = row.children[index];
                    if (cell) {
                        const text = cell.textContent.toLowerCase();
                        if (text.indexOf(filter) > -1) {
                            row.style.display = '';
                        } else {
                            row.style.display = 'none';
                        }
                    }
                });
            });
        });
    });

    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(function(card, index) {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(function() {
            card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });

    // Print functionality
    window.printReport = function() {
        window.print();
    };

    // Export functionality (placeholder)
    window.exportData = function(format) {
        alert('Export functionality will be implemented in future versions.');
    };

    // Real-time clock for timestamps
    function updateClock() {
        const now = new Date();
        const timeString = now.toLocaleString();
        const clockElements = document.querySelectorAll('.current-time');
        clockElements.forEach(function(element) {
            element.textContent = timeString;
        });
    }
    
    setInterval(updateClock, 1000);
    updateClock();

    // Quantity validation
    const quantityInputs = document.querySelectorAll('input[name="qty"]');
    quantityInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            if (this.value < 1) {
                this.setCustomValidity('Quantity must be at least 1');
            } else {
                this.setCustomValidity('');
            }
        });
    });

    // Auto-generate IDs
    const idInputs = document.querySelectorAll('input[name$="_id"]');
    idInputs.forEach(function(input) {
        if (!input.value) {
            const generateButton = document.createElement('button');
            generateButton.type = 'button';
            generateButton.className = 'btn btn-outline-secondary btn-sm ms-2';
            generateButton.innerHTML = '<i class="fas fa-magic"></i> Generate';
            generateButton.addEventListener('click', function() {
                const prefix = input.name.replace('_id', '').toUpperCase();
                const timestamp = Date.now().toString().slice(-6);
                input.value = prefix + '_' + timestamp;
                input.dispatchEvent(new Event('input'));
            });
            
            input.parentNode.appendChild(generateButton);
        }
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', function(event) {
        // Ctrl/Cmd + N for new items
        if ((event.ctrlKey || event.metaKey) && event.key === 'n') {
            event.preventDefault();
            const addButtons = document.querySelectorAll('a[href*="/add"]');
            if (addButtons.length > 0) {
                addButtons[0].click();
            }
        }
        
        // Ctrl/Cmd + S for save (if in a form)
        if ((event.ctrlKey || event.metaKey) && event.key === 's') {
            const form = document.querySelector('form');
            if (form && form.querySelector('button[type="submit"]')) {
                event.preventDefault();
                form.querySelector('button[type="submit"]').click();
            }
        }
        
        // Escape to go back
        if (event.key === 'Escape') {
            const backButton = document.querySelector('a[href*="cancel"], .btn-secondary');
            if (backButton) {
                backButton.click();
            }
        }
    });

    // Add loading states to forms
    const submitButtons = document.querySelectorAll('button[type="submit"]');
    submitButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            const form = this.closest('form');
            if (form) {
                // Check if form has required fields and they are filled
                const requiredFields = form.querySelectorAll('[required]');
                let canSubmit = true;
                
                requiredFields.forEach(function(field) {
                    if (!field.value.trim()) {
                        canSubmit = false;
                    }
                });
                
                if (canSubmit) {
                    // Add a small delay to allow form submission to proceed
                    setTimeout(() => {
                        this.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Saving...';
                        this.disabled = true;
                    }, 100);
                }
            }
        });
    });

    // Initialize all components
    console.log('Inventory Management System initialized successfully');
});

// Utility functions
function formatNumber(num) {
    return new Intl.NumberFormat().format(num);
}

function formatDate(date) {
    return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    }).format(new Date(date));
}

function showToast(message, type = 'info') {
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    // Add to toast container
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
        document.body.appendChild(toastContainer);
    }
    
    toastContainer.appendChild(toast);
    
    // Show toast
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Remove from DOM after hiding
    toast.addEventListener('hidden.bs.toast', function() {
        toast.remove();
    });
}



