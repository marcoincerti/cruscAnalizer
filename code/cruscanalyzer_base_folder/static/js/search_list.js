/**
 * Function to change header tab.
 * @param {HTMLAnchorElement} $element - tab clicked by the user
 * @param {String} hideClassName - CSS class of the tab that have to be hidden
 * @param {String} showClassName - CSS class of the tab that have to be shown
 */
function changeHeaderTab($element, hideClassName, showClassName) {
    $('.' + hideClassName).hide();
    $('.'+ showClassName).show();

    let $previousActiveTab = $element.closest('.nav').find('.active');
    $previousActiveTab.removeClass('active');
    $previousActiveTab.removeClass('btn-outline-info');

    $element.addClass('active');
    $element.addClass('btn-outline-info');
}

$(function () {
    /** event on click tab "testi" on header nav */
    $('#search-text-header-testi').on('click', function () {
        let hideClassName = 'search-list-users-information';
        let showClassName = 'search-list-texts-information';
        changeHeaderTab($(this), hideClassName, showClassName);
    });

    /** event on click tab "utenti" on header nav */
    $('#search-text-header-utenti').on('click', function () {
        let hideClassName = 'search-list-texts-information';
        let showClassName = 'search-list-users-information';
        changeHeaderTab($(this), hideClassName, showClassName);
    });
});