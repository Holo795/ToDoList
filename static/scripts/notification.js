function notifier(title="ToDo List", message, icon_image=null, bg_image=null) {
    /* On demande la permission si les notifications ne sont pas permises */
    if (Notification.permission !== 'granted')
        Notification.requestPermission();
    /* Sinon on affiche la notification */
    else {

        var notification = new Notification(title, {
            icon: icon_image,
            body: message,
            image: bg_image,
        });

    }
}