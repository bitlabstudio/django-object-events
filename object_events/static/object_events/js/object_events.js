function checkUnreadNotifications() {
    if ($('[data-class="notification"].unread').length == 0) {
        // Hide bulk button, if there are no unread notifications.
        $('button[name="bulk_mark"]').parents('[data-class="notification"]').hide();
    }
}

$(document).ready(function() {
    $('[data-class="notifications"]').hide();
    $('[data-class="notification-btn"]').click(function() {
        $('[data-class="notifications"]').show();
        return false;
    });
    $('html').click(function() {
        $('[data-class="notifications"]:visible').hide();
    });
    $('[data-class="notifications"]').click(function(event){
        event.stopPropagation();
    });
    checkUnreadNotifications();
    $('[data-class="notification"]').click(function() {
        var notif = $(this);
        if (notif.hasClass('unread')) {
            var form = notif.parents('form');
            $.post(
                form.attr('action')
                ,{
                    'single_mark': notif.find('[name="single_mark"]').val()
                    ,'csrfmiddlewaretoken':  form.find('input[name="csrfmiddlewaretoken"]').val()
                }
                ,function(data) {
                    if (data == 'marked') {
                        notif.removeClass('unread');
                        // Decrease notification counter
                        var unread_amount = $('[data-id="notification-unread"]').text();
                        if (unread_amount <= 1) {
                            $('[data-id="notification-unread"]').removeClass('unread');
                        }
                        $('[data-id="notification-unread"]').text(unread_amount - 1);
                        checkUnreadNotifications();
                    }
                }
            );
        }
    });
    $('[data-class="notifications"] button[name="bulk_mark"]').click(function() {
        var form = $(this).parents('form');
        $.post(
            form.attr('action')
            ,{
                'bulk_mark': $(this).val()
                ,'csrfmiddlewaretoken':  form.find('input[name="csrfmiddlewaretoken"]').val()
            }
            ,function(data) {
                if (data == 'marked') {
                    // Get only unread notifications from first notification wrapper
                    // In case you are watching both, list view and tag, only one of them is tracked
                    var unread_notifs = $('[data-class="notifications"]').first().find('[data-class="notification"].unread');
                    var unread_amount = $('[data-id="notification-unread"]').text();

                    // Remove all unread classes, though
                    $('[data-class="notifications"] [data-class="notification"].unread').removeClass('unread');
                    if ((unread_amount - unread_notifs.length) <= 1) {
                        $('[data-id="notification-unread"]').removeClass('unread');
                    }
                    $('[data-id="notification-unread"]').text(unread_amount - unread_notifs.length);
                    checkUnreadNotifications();
                }
            }
        );
        return false;
    });
});