function checkUnreadNotifications() {
    if ($('.notifications li.unread').length == 0) {
        // Hide bulk button, if there are no unread notifications.
        $('button[name="bulk_mark"]').parents('li').hide();
    }
}

$(document).ready(function() {
    $('#notificationBar').hide();
    $('#notificationBtn').click(function() {
        $('#notificationBar').show();
        return false;
    });
    $('html').click(function() {
        $('#notificationBar:visible').hide();
    });
    $('#notificationBar').click(function(event){
        event.stopPropagation();
    });
    checkUnreadNotifications();
    $('.notifications li').click(function() {
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
                        var unread_amount = $('#notificationBtn .badge').text();
                        if (unread_amount <= 1) {
                            $('#notificationBtn .badge').removeClass('badge-important');
                        }
                        $('#notificationBtn .badge').text(unread_amount - 1);
                        checkUnreadNotifications();
                    }
                }
            );
        }
    });
    $('.notifications button[name="bulk_mark"]').click(function() {
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
                    var unread_notifs = $('.notifications').first().find('li.unread');
                    var unread_amount = $('#notificationBtn .badge').text();

                    // Remove all unread classes, though
                    $('.notifications li.unread').removeClass('unread');
                    if ((unread_amount - unread_notifs.length) <= 1) {
                        $('#notificationBtn .badge').removeClass('badge-important');
                    }
                    $('#notificationBtn .badge').text(unread_amount - unread_notifs.length);
                    checkUnreadNotifications();
                }
            }
        );
        return false;
    });
});