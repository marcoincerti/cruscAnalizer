$(function () {
    /** event on click of save analysis button */
    $('#save-text-button').click(function () {
        let button = $(this);
        ajaxSaveTextAnalysis(button);
    });
});
