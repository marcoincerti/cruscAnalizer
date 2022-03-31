/**
 * Function call when the user click the translate button on the table.
 * It fills the original word field, with corresponding table row word.
 * @param {HTMLButtonElement} $element - button which the user clicked
 */
function loadTranslateModal($element) {
    let word = $element.closest('tr').find('.text-word').text();
    $("#translate-modal-original-word").val(word);
    translateWord(true);
}

/**
 * Function to translate a word.
 * It retrieve the original word and the source and destination languages from relative input fields.
 * @param {Boolean} detect_language - true if we are loading modal and detect source language
 */
function translateWord(detect_language) {
    let language_source;
    if (detect_language) {
         language_source = null;
    } else {
        language_source = $('#translate-modal-source-language-select').val();
    }
    let language_destination = $('#translate-modal-destination-language-select').val();
    let word = $('#translate-modal-original-word').val();
    ajaxTranslateWord(word, language_source, language_destination, detect_language);
}

$(function () {
    /** event on click of translate button */
    $('.translate-word').on('click', function () {
        loadTranslateModal($(this));
    });

    /** event on change of select picker:
     *      - source language
     *      - destination language
     */
    $('.language-select').on('change', function () {
        if (!$(this).hasClass('bootstrap-select'))
            translateWord(false);
    });
});