const dateToFooter = () => document.querySelector('#now').innerText = new Date()
const activateTooltips = () => document.querySelectorAll('[data-toggle="tooltip"]').forEach(link => $(link).tooltip())

document.addEventListener("DOMContentLoaded", function() {
    activateTooltips()
    dateToFooter()
});

const filterBookmarks = () => document.querySelectorAll(".row.bookmark div a.bookmark-link")
    .forEach(link => link.innerHTML.toLowerCase().includes(document.querySelector('#filter_field').value.toLowerCase())
        ? link.parentNode.parentNode.parentNode.classList.remove('d-none')
        : link.parentNode.parentNode.parentNode.classList.add('d-none'))

const filterCategories = () => document.querySelectorAll('.category-card .card-header')
    .forEach(link => link.innerText.toLowerCase().includes(document.querySelector('#filter_field').value.toLowerCase())
        ? link.parentNode.classList.remove('d-none')
        : link.parentNode.classList.add('d-none'))
