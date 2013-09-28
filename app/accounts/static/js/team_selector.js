/*
 * Team selector using dropdown.
 */
(function() {
    var teamDisplay = $('.team');
    var teamDropdown = $('.team-dropdown');
    var teamInput = $('#id_team')

    var initialValue = teamInput.val();
    if (initialValue) {
        teamDisplay.text(teamDropdown.find('li a[data-value="' + initialValue + '"]').text());
    }

    teamDropdown.on('click', 'li a', function(e) {
        e.stopPropagation();
        e.preventDefault();

        var option = $(this);
        var value = option.data('value');
        var display = option.text();

        teamInput.val(value);
        teamDisplay.text(display);

        teamDropdown.dropdown('toggle');
    });
})();
