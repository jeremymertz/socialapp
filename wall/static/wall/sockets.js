// Base notifications
var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
const username = JSON.parse(document.getElementById('user').textContent);
    const NotificationsSocket = new WebSocket(
        ws_scheme
        + '://'
        + window.location.host
        + '/ws/notifications/'
        + username
        + '/'
    );

    NotificationsSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        if (data.notification_type == "notification"){
            no_notif = document.getElementById('no-notification')
            if (no_notif){
                no_notif.remove();
            };
            document.getElementById('notification').classList.add("red-dot");

            new_notification =
            '<li><span class="dropdown-item-text"><div class="card" style="width: 18rem;">' +
            '<div class="card-body"><p class="card-text"><div class="row"><div class="col-sm-3">' +
            '<a href="' +
            data.sender_profile +
            '"><img class="rounded-circle avatar" src="' +
            data.sender_avatar +
            '" width="45" height="45"></a></div> <div class="col-sm-6 no-padding"><a href="' +
            data.sender_profile +
            '"><b>' +
            data.sender_username +
            '</b></a><a href="' +
            data.post_url +
            '"> ' +
            data.message +
            '</a></div><div class="col-sm-3"><a href="' +
            data.post_url +
            '"><img class="thumbnail" src="' +
            data.post_picture +
            '"></a></div></div></p></div></div></span></li>'

            $(new_notification).insertAfter($(".marker"));
        }
        else if (data.notification_type == "private_message"){
            document.getElementById('mailimg').src = "/static/wall/images/newmail.png"
            last_message_id = "last-message-" + data.channel
            last_date_id = "last-time-" + data.channel
            current_channel_id = "chat-" + data.channel
            console.log(current_channel_id)
            last_message = document.getElementById(last_message_id)
            last_date = document.getElementById(last_date_id)
            current_channel = document.getElementById(current_channel_id)
            console.log(current_channel)
            if (last_message){
                last_message.innerHTML = data.message;
                last_date.innerHTML = "Just now";
                current_channel.classList.add("new_message_chat");
            };
        }
    };

    NotificationsSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

// Send private message
function last_private_message(sender, receiver, message, roomName){
    const SendNotifications = new WebSocket(
        ws_scheme
        + '://'
        + window.location.host
        + '/ws/notifications/'
        + receiver
        + '/'
        );
    console.log("connected!")
    SendNotifications.onopen = () => SendNotifications.send(JSON.stringify({
        'liked': sender,
        'message': message,
        'channel': roomName,
    }));
}