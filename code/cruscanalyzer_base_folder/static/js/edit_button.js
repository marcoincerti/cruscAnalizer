/**
 * Function to show actions buttons.
 * @param {HTMLAnchorElement} $main_edit - edit button clicked by user
 */
function enableActions($main_edit) {
    $main_edit.removeClass('off');
    $main_edit.addClass('on');
    $main_edit.find('.show-actions-button').hide();
    $main_edit.find('.hide-actions-button').show();
    $main_edit.closest('.box-width-radius2').find('.actions').css('display', 'flex');
}

/**
 * Function to hide actions buttons.
 * @param {HTMLButtonElement} $main_edit - edit button clicked by user
 */
function disableActions($main_edit) {
    $main_edit.removeClass('on');
    $main_edit.addClass('off');
    $main_edit.find('.show-actions-button').show();
    $main_edit.find('.hide-actions-button').hide();
    $main_edit.closest('.box-width-radius2').find('.actions').hide();
}