const dateToFooter = () => document.querySelector('#now').innerText = new Date()
const activateTooltips = () => document.querySelectorAll('[data-toggle="tooltip"]').forEach(link => $(link).tooltip())

document.addEventListener("DOMContentLoaded", function() {
    activateTooltips()
    dateToFooter()
});
