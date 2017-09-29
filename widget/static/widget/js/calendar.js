(function($){
    var calendar;
    calendar = {
        initWidget : function(data) {
            var widget = new TimekitBooking();
            widget.init({
                app:      data.app,
                email:    data.email,
                apiToken: data.apiToken,
                calendar: data.calendarId,
                bookingGraph: data.bookingGraph,
                timekitFindTime:{
                    filters: data.filters,
                    future: data.future,
                    length: data.length
                },
                timekitCreateBooking:{
                    send_confirm_decline_email_to_owner : {
                        enabled: false
                    },
                    notify_customer_by_email: {
                        enabled: false
                    },
                    notify_customer_declined_by_email: {
                        enabled: false
                    },
                    notify_customer_cancelled_by_email: {
                        enabled: false
                    },
                    notify_owner_cancelled_by_email: {
                        enabled: false
                    },
                    customer:data.customer_params
                }
            });
        }
    };
    window.calendar = calendar;
})(jQuery);
