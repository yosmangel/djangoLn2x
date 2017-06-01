$(".profile-image a").click(function() {
    content = $($(this).attr('href')).html();
    container = $("#bio-container");
    if(container.html() != content) {
        container.slideUp().html(content).slideDown();
    } else {
        container.slideToggle();
    }

});
