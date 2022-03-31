$(function () {
    /** event on click of edit text list button */
    $('.main-edit-button').on('click', function () {
        if ($(this).hasClass('off')) {
            enableActions($(this));
        } else {
            disableActions($(this));
        }
    });
});
