const darkSwitch = document.getElementById('darkSwitch');
window.addEventListener('load', () => {
  if (darkSwitch) {
    initTheme();
    darkSwitch.addEventListener('change', () => {
      resetTheme();
    });
  }
});

/**
 * Summary: function that adds or removes the attribute 'data-theme' depending if
 * the switch is 'on' or 'off'.
 *
 * Description: initTheme is a function that uses localStorage from JavaScript DOM,
 * to store the value of the HTML switch. If the switch was already switched to
 * 'on' it will set an HTML attribute to the body named: 'data-theme' to a 'dark'
 * value. If it is the first time opening the page, or if the switch was off the
 * 'data-theme' attribute will not be set.
 * @return {void}
 */
function initTheme() {
  const darkThemeSelected =
      localStorage.getItem('darkSwitch') !== null &&
      localStorage.getItem('darkSwitch') === 'dark';
  darkSwitch.checked = darkThemeSelected;
  if(darkThemeSelected){
      document.body.setAttribute('data-theme', 'dark');
      $('.data-table').addClass('table-dark');
      $('thead').addClass('thead-dark');
      $('.transparent-box-width-radius-white').addClass('transparent-box-width-radius-black').removeClass('transparent-box-width-radius-white');
  }
  else{
    document.body.removeAttribute('data-theme');
      $('.data-table').removeClass('table-dark');
      $('thead').removeClass('thead-dark');
      $('.transparent-box-width-radius-black').addClass('transparent-box-width-radius-white').removeClass('transparent-box-width-radius-black');
    }
}

/**
 * Summary: resetTheme checks if the switch is 'on' or 'off' and if it is toggled
 * on it will set the HTML attribute 'data-theme' to dark so the dark-theme CSS is
 * applied.
 * @return {void}
 */
function resetTheme() {
  if (darkSwitch.checked) {
      document.body.setAttribute('data-theme', 'dark');
      $('.data-table').addClass('table-dark');
      $('thead').addClass('thead-dark');
      $('.transparent-box-width-radius-white').addClass('transparent-box-width-radius-black').removeClass('transparent-box-width-radius-white');
    localStorage.setItem('darkSwitch', 'dark');
  } else {
      document.body.removeAttribute('data-theme');
      $('.data-table').removeClass('table-dark');
      $('thead').removeClass('thead-dark');
      $('.transparent-box-width-radius-black').addClass('transparent-box-width-radius-white').removeClass('transparent-box-width-radius-black');
      localStorage.removeItem('darkSwitch');
  }
}

/**
 * Function to deselect all options in a multiple options selectpicker.
 * After deselect all, it select the 'all options' option.
 * @param {HTMLSelectElement} $select - select picker element
 */
function deselectAll($select){
    $select.selectpicker('deselectAll');
    $select.selectpicker('val', '0');
    $select.selectpicker('refresh');
}

/**
 * Function to select the 'all options' option in a multiple options selectpicker.
 * @param {HTMLSelectElement} $select - select picker element
 */
function selectSelectAllOption($select) {
    let $selectAllOption = $select.find('.select-all');
    $selectAllOption.prop('selected', true);
    $select.selectpicker('refresh');
}

/**
 * Function to deselect the 'all options' option in a multiple options selectpicker.
 * @param {HTMLSelectElement} $select - select picker element
 */
function deselectSelectAllOption($select) {
    let $selectAllOption = $select.find('.select-all');
    $selectAllOption.prop('selected', false);
    $select.selectpicker('refresh');
}

$(function () {
    /** event on change of select picker of categories in search bar */
    $('#navbar-select-categories, #compare-modal-select-categories').on('changed.bs.select',
        function (e, clickedIndex, isSelected, previousValue) {
            if (clickedIndex !== 0 && isSelected === true)
                deselectSelectAllOption($(this));
            if (clickedIndex === 0) {
                if (isSelected === true)
                    deselectAll($(this));
                else {
                    if(previousValue.length === 1)
                        selectSelectAllOption($(this));
                }
            }
            if (clickedIndex !== 0 && isSelected === false) {
                if (previousValue.length === 1)
                    selectSelectAllOption($(this));
            }
    });
    $(document).ready( function () {
        $('.data-table').DataTable( {
            'columnDefs': [{
                'targets': 3,
                'orderable': false
            }],
            'language': {
                'lengthMenu': '_MENU_ Parole per pagina',
                'zeroRecords': 'Nessuna parola presente - ci dispiace',
                'info': 'Pagina _PAGE_ di _PAGES_',
                'infoEmpty': 'Nessuna parola disponibile',
                'infoFiltered': '(Filtrati da _MAX_ parole totali)',
                'search': 'Cerca: ',
                'paginate': {
                    'first': 'Prima',
                    'last': 'Ultima',
                    'next': 'Prossima',
                    'previous': 'Precedente'
                }
            },
            'initComplete': () => { $('.data-table').fadeIn(); $('.graph').fadeIn(); }
        } );
    } );
});