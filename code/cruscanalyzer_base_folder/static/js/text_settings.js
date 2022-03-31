/**
 * Function to clone content of an element and append to another one.
 * @param {HTMLElement} $element_clone_content - element of which clone content
 * @param {HTMLElement} $element_append_clone - element to append cloned content
 */
function cloneContent($element_clone_content, $element_append_clone) {
    let clone = $element_clone_content.contents().clone();
    $element_append_clone.append(clone);
}

/**
 * Function to disable word input fields.
 * @param {HTMLElement} $element - element clicked by user
 */
function disableWordFields($element) {
    let $container = $element.closest('.box-width-radius2');
    $container.find('input').attr('disabled', true);
    $container.find('#blacklist-add-word-button').hide();
    if (($container.find('form').find('input').length - 1) === 0)
        $container.find('.empty-blacklist-message').show();
}

/**
 * Function to enable word input fields.
 * @param {HTMLElement} $element - element clicked by user
 */
function enableWordFields($element) {
    let $container = $element.closest('.box-width-radius2');
    $container.find('input').attr('disabled', false);
    $container.find('#blacklist-add-word-button').show();
    $container.find('.empty-blacklist-message').hide();
}


/**
 * Function to remove a black word input field.
 * @param {HTMLAnchorElement} $delete_button - delete button clicked by the user
 */
function removeBlackWord($delete_button) {
    $delete_button.closest('.row').remove();
}

$(function () {
    /** event on click of new word button */
    $('#blacklist-add-word-button').on('click', function () {
        cloneContent($('#blacklist-clone-input-word'), $('#words-list'));
    });

    /** event on click of edit button */
    $('.main-edit-button').on('click', function () {
        if ($(this).hasClass('off')) {
            enableActions($(this));
            enableWordFields($(this));
        } else {
            disableActions($(this));
            disableWordFields($(this));
        }
    });

    /** event on click of delete word button, needs delegate for appended elements */
    $(document).delegate(".delete-black-word", 'click', function () {
        removeBlackWord($(this));
    });

    /**
     * event on FIRST click of submit button,
     * it enable input fields before submit the form for allowing get the data from back-end (TextSettingsView, post).
     */
    $('#settings-save-changes').one('click', function (event) {
        event.preventDefault();
        $('input').attr('disabled', false);
        $(this).trigger('click');
    });
});