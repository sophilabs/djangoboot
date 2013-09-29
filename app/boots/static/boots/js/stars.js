/*
 * Star boot button.
 */
(function() {
    $(document).on('click', '.btn-star-boot', function(e) {
        e.preventDefault();
        e.stopPropagation();

        var button = $(this);
        var bootId = button.data('boot-id');
        var value = button.data('value');

        button.addClass('btn-star-boot-change');
        setTimeout(function() {
            button.removeClass('btn-star-boot-change');
        }, 200);

        var showMessage = function(text) {
            button.tooltip({
                'title': text,
                'placement': 'top',
                'trigger': 'manual'
            }).tooltip('show');
            setTimeout(function() {
                button.tooltip('hide');
            }, 1000);
        };

        var csrf_token = $.cookie('csrftoken');

        $.post(STAR_BOOT_URL, {
            'boot_id': bootId,
            'value': value,
            'csrfmiddlewaretoken': csrf_token
        }, function(response) {
            var message = response['message'];
            if (message) {
                showMessage(message);
            }

            var value = response['value'];
            if (value) {
                button.data('value', 'true');
                button.find('i').attr('class', 'icon-heart');
            } else {
                button.data('value', 'false');
                button.find('i').attr('class', 'icon-heart-empty');
            }

            var count = response['count'];
            if (count != undefined) {
                button.find('.count').text(count);
            }
        });
    });
})();