function notifier(title="ToDo List", message, icon_image=null, bg_image=null) {
    /* On demande la permission si les notifications ne sont pas permises */
    if (Notification.permission !== 'granted')
        Notification.requestPermission().then(r => {
            if (r === 'granted') {
                new Notification(title, {
                    body: message,
                    icon: icon_image,
                    image: bg_image
                });
            }
        });
    /* Sinon on affiche la notification */
    else {
        new Notification(title, {
            icon: icon_image,
            body: message,
            image: bg_image,
        });
    }
}