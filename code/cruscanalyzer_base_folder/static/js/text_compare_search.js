/**
 * Function to get data from the search form to pass to ajax.
 * @param {HTMLFormElement} $element - form that the user submitted
 */
function getSearchFormData($element){
    let search = $element.find('.search-field').val();
    let text_pk = $element.attr('value');
    let categories = [];
    let y = 0;
    $element.find('.select-categories').find('option').each(function () {
        if($(this).is(':selected')) {
            categories[y] = parseInt($(this).attr('value'));
            y++;
        }
    });
    ajaxSearchText(search, text_pk, categories);
}

/**
 * Function to set the value of the compare modal to a primary key.
 * @param {string} pk - primary key which want to set
 */
function putPkOnModal(pk) {
    $('#compare-modal-search-form').attr('value', pk);
}

/**
 * Function to reset compare modal fields:
 *  - remove value attribute (primary key of the first text)
 *  - select the default option in the categories select picker
 *  - reset search input field
 *  - remove search results
 */
function resetCompareModal() {
    let search_form = $('#compare-modal-search-form');
    search_form.removeAttr('value');
    search_form.find('.select-categories').selectpicker('val', '0');
    search_form.find('.search-field').val('');
    let modal = $('#compare-modal');
    modal.find('.compare-modal-search-result').contents().remove();
}

$(function () {
    /** event on click of the compare texts button */
    $('.text-analysis-confronta-testo').on('click', function () {
        let text_pk = $(this).attr('value');
        putPkOnModal(text_pk);
    });

    /** event on submit search bar form in compare modal */
    $('#compare-modal-search-form').submit(function (event) {
        event.preventDefault();
        getSearchFormData($(this));
    });

    /** event on hidden of the compare modal */
    $('#compare-modal').on('hidden.bs.modal', function () {
        resetCompareModal();
    });
});
