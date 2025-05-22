document.addEventListener('DOMContentLoaded', () => {
    const menuItems = document.querySelectorAll('.menu-item');
    menuItems.forEach(item => {
        item.addEventListener('click', () => {
            alert(`You selected ${item.querySelector('h2').textContent}!`);
        });
    });
});