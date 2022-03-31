/**
 * Function to replace an element text content with a substring.
 * @param {HTMLElement} $element - element that contains string to cut
 * @param {number} cut_length - number representing the length of the substring
 */
function cutElementTextContent($element, cut_length) {
    if ($element.text().length > cut_length) {
        let new_string = $element.text().substring(0, cut_length) + " ...";
        $element.text(new_string);
    }
}

$(function () {
    /** iterates on each class name element in the page */
    $('.user-text-list-item-title').each(function () {
        cutElementTextContent($(this), 50);
    });

    /** iterates on each class name element in the page */
    $('.user-text-list-item-author').each(function () {
        $(this).addClass('font-weight-light');
        cutElementTextContent($(this), 25);
    });

    /** gradually increase body opacity */
    setTimeout(function(){$('body').animate({opacity:'1'},300)},100);
});