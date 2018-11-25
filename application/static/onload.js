document.addEventListener("DOMContentLoaded", function() {
    // activate bootstrap tooltips
    $('[data-toggle="tooltip"]').tooltip()

    // date to footer
    let now = new Date();
    $('#now').text(now);
});
