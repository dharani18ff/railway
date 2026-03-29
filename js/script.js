// Simple add to cart functionality scoped to product cards
document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('.product button');
    buttons.forEach(button => {
        button.addEventListener('click', (e) => {
            const product = e.target.closest('.product');
            const productName = product?.querySelector('h3')?.textContent || 'Item';
            alert(`${productName} added to cart!`);
        });
    });
});