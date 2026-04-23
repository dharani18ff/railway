// Contact form submission handler
document.addEventListener('DOMContentLoaded', () => {
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', (event) => {
            event.preventDefault();
            const name = contactForm.elements['name'].value.trim();
            let successMsg = contactForm.querySelector('.form-success');
            if (!successMsg) {
                successMsg = document.createElement('p');
                successMsg.className = 'form-success';
                contactForm.appendChild(successMsg);
            }
            successMsg.textContent = `Thank you, ${name}! Your message has been received. We will get back to you shortly.`;
            contactForm.reset();
        });
    }

    // Simple add to cart functionality scoped to product cards
    const buttons = document.querySelectorAll('.product button');
    buttons.forEach(button => {
        button.addEventListener('click', (e) => {
            const product = e.target.closest('.product');
            const productName = product?.querySelector('h3')?.textContent || 'Item';
            alert(`${productName} added to cart!`);
        });
    });
});