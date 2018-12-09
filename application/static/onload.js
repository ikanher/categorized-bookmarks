const activateTooltips = () => $('[data-toggle="tooltip"]').tooltip()
const dateToFooter = () => { let now = new Date(); $('#now').text(now) }

document.addEventListener("DOMContentLoaded", function() {
    activateTooltips()
    dateToFooter()
});
