/**
 * Main JavaScript - Form handling, AJAX calls, UI interactions
 */

// Utility: Format numbers with thousand separators
function formatNumber(num) {
    return num.toLocaleString('en-US', { maximumFractionDigits: 2 });
}

// Utility: Show toast notification
function showToast(message, type = 'info') {
    // You can enhance this with a toast library like Toastr
    console.log(`[${type.toUpperCase()}] ${message}`);
}

// Ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('Oil Optimization System - Ready!');
});
