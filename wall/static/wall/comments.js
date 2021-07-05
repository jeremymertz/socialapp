comment_box = document.getElementById("comment-form");
comment_form = document.getElementById("new_comment_form");
new_comment_submit_off = document.getElementById("submit_new_comment_off");
new_comment_submit_on = document.getElementById("submit_new_comment_on");
new_reply_submit_off = document.getElementById("submit_new_reply_off");
avatar = document.getElementById("my_avatar");
profile_link = document.getElementById("profile");
username = document.getElementById("my_username");
this_comment_text_box = document.getElementById('new_comment_content')
new_comments_box = document.getElementById('new_comments')
csrf_meta = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";

// Post comment button
function typing_comment(){
    if (this_comment_text_box.value == ""){
        new_comment_submit_off.style.display = "inline";
        new_comment_submit_on.style.display = "none";
        }
    else {
        new_comment_submit_off.style.display = "none";
        new_comment_submit_on.style.display = "inline";
        }
    };

function typing_reply(value){
    submit_id = "submit-" + value
    text_id = "text-" + value
    no_submit_id = "no-submit-" + value
    new_reply_submit_on = document.getElementById(submit_id);
    this_reply_text_box = document.getElementById(text_id);
    new_reply_submit_off = document.getElementById(no_submit_id);

    if (this_reply_text_box.value == ""){
        new_reply_submit_off.style.display = "inline";
        new_reply_submit_on.style.display = "none";
        }
    else {
        new_reply_submit_off.style.display = "none";
        new_reply_submit_on.style.display = "inline";
        }
    };

// Submit comment
if (new_comment_submit_on){
    comment_form.addEventListener('submit', function(e){
        e.preventDefault();
        new_comment_text = this_comment_text_box.value;
        no_comment = document.getElementById('nocomments');
        const fd = new FormData();
        test_meta = csrf_meta
        fd.append('csrfmiddlewaretoken', csrf_meta);
        fd.append('new_comment', new_comment_text);
        $.ajax({
            type: "POST",
            url: new_comment_submit_on.getAttribute('data-url'),
            data: fd,
            success: function(response) {
                if (response.success==true){
                    this_comment_text_box.value = ""
                    new_comment_submit_off.style.display = "inline";
                    new_comment_submit_on.style.display = "none";
                    if (response.author != response.user){
                        const SendNotifications = new WebSocket(
                            ws_scheme +
                            '://' +
                            window.location.host +
                            '/ws/notifications/' +
                            response.author +
                            '/'
                        );
                        SendNotifications.onopen = () => SendNotifications.send(JSON.stringify({
                            'liked': response.user,
                            'post-no': response.post_number,
                            'comment-no': response.id
                        }));
                    }
                    if (no_comment){
                        no_comment.remove()
                    };
                    new_comments_box.innerHTML = '<div class="comments comment-main-level"><div class="comment-avatar">' +
                                                '<a href="' + profile.href + '"><img class="rounded-circle avatar follow-avatars" src="' +
                                                avatar.src +
                                                '"></a></div><div class="comment-box"><div class="comment-head">' +
                                                '<h6 class="comment-name"><a href="' + profile.href + '">' +
                                                response.user +
                                                '</a></h6><span>Now</span><i class="fa fa-reply" id="new_reply" data-post="' +
                                                response.id +
                                                '"></i><div class="arrows"><i class="new_like_arrow_down fa fa-arrow-down" data-url="' +
                                                response.unlike_url +
                                                '"data-id="' + response.id + '" id="down-' + response.id +
                                                '"></i><i class="new_like_arrow_up fa fa-arrow-up" data-url="' +
                                                response.like_url + '" data-id="' + response.id +
                                                '" id="up-' + response.id + '"></i>' +
                                                '<i id="clcounter-' + response.id + '" data-ratio="0' +
                                                '">' + 0 + '</i></div>' +
                                                '<i class="fa fa-trash" data-bs-toggle="modal" data-bs-target="#delete_comment-' +
                                                response.id + '"></i>' +
                                                '<div class="modal fade" id="delete_comment-' +
                                                response.id + '" tabindex="-1" aria-labelledby="delete_comment_label-' +
                                                response.id + '" aria-hidden="true"><div class="modal-dialog"><div class="modal-content">' +
                                                '<div class="modal-header"><h5 class="modal-title black" id="delete_comment_label-' +
                                                response.id + '">Delete Comment</h5>' +
                                                '<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>' +
                                                '</div><div class="modal-body">Are you sure you want to delete your comment?</div>' +
                                                '<div class="modal-footer"><button type="button" class="btn btn-secondary" ' +
                                                'data-bs-dismiss="modal">Cancel</button><a class="btn btn-danger" href="' +
                                                response.delete_url + '">Delete Comment</a>' +
                                                '</div></div></div></div></div><div class="comment-content">' +
                                                new_comment_text + '</div></div></div>' +
                                                '<div class="reply-form" id="comment-' + response.id + '">' +
                                                '<form method="POST" id="reply_form-' + response.id +'">' +
                                                '<div class="input-group"><div class="input-group-prepend"><div class="input-group-text">' +
                                                '<img class="rounded-circle avatar mx-auto" src="' +
                                                avatar.src +
                                                '" width="30" height="30"> </div></div>' +
                                                '<input name="csrfmiddlewaretoken" type="hidden" value="' + test_meta + '">' +
                                                '<input type="text" id="text-' + response.id +
                                                '" onkeyup="typing_reply(' + response.id + ')" ' +
                                                'class="form-control" placeholder="Leave your reply here..." required>' +
                                                '<div class="input-group-prepend"><div class="input-group-text">' +
                                                '<span class="btn" id="no-submit-' + response.id + '">Post</span>' +
                                                '<button class="btn submit_new_reply_on" type="submit" data-url="' +
                                                response.reply_url  + '" value="Post" id="submit-' +
                                                response.id + '">Post</button>' +
                                                '</div></div></div></form></div>' +
                                                new_comments_box.innerHTML;

                    // Click on reply button
                    $('.comments').on('click', '#new_reply', function(e){
                        e.preventDefault();
                        this_button = $(this);
                        comment_number = $(this).attr('data-post');
                        // Select current button
                        reply(this_button, comment_number);
                    })

                    // Click on arrow_up button
                    $('.arrows').on('click', '.new_like_arrow_up', function(e){
                        e.preventDefault();
                        this_button = $(this);
                        url = $(this).attr('data-url');
                        likeArrowUp(this_button, url);
                    })

                    // Click on arrow_up button
                    $('.arrows').on('click', '.new_like_arrow_down', function(e){
                        e.preventDefault();
                        this_button = $(this);
                        url = $(this).attr('data-url');
                        likeArrowDown(this_button, url);
                    })
                }
                else if (response.success==false){
                    console.log('Error')
                }
            },
            contentType: false,
            processData: false,
        })
    })
}




// Click on reply button
$('.comments').on('click', '#reply', function(e){
    e.preventDefault();
    this_button = $(this);
    comment_number = $(this).attr('data-post');
    // Select current button
    reply(this_button, comment_number);
})

function reply(this_button, comment_number){
        // Close any other reply buttons
        var open_buttons = document.getElementsByClassName('reply-form');
        if (open_buttons) {
            for (var x = 0; x < open_buttons.length; x++) {
              open_buttons[x].style.visibility = "hidden";
              open_buttons[x].style.height = "0px";
            };
        };
        // Find parent and submit button
        this_reply = "comment-" + comment_number;
        submit_reply = "submit-" + comment_number;
        submit_reply_off = "no-submit-" + comment_number;
        this_reply_box = document.getElementById(this_reply);
        if (this_reply_box.style.visibility == "visible"){
            this_reply_box.style.visibility = "hidden";
            this_reply_box.style.height = '0px';
        } else {
            this_reply_box.style.visibility = "visible";
            this_reply_box.style.height = 'auto';
        }
        // submit_button
        this_submit_reply = document.getElementById(submit_reply);
        this_submit_reply_off = document.getElementById(submit_reply_off);
        reply_form = "reply_form-" + comment_number
        this_reply_form = document.getElementById(reply_form);

        // Click on submit button of reply
        this_reply_form.addEventListener('submit', function(e){
            e.preventDefault();
            // Select text of reply
            reply_text = "text-" + comment_number;
            this_reply_text = document.getElementById(reply_text).value;

            // Prepare data for backend
            const fd = new FormData();
            fd.append('csrfmiddlewaretoken', csrf_meta);
            fd.append('new_reply', this_reply_text);
            fd.append('parent', comment_number);

            $.ajax({
                 type: "POST",
                 url: this_submit_reply.getAttribute('data-url'),
                 data: fd,
                 success: function(response) {
                        if(response.success==true){
                            this_reply_form.reset();
                            reply_text.value = ""
                            this_submit_reply_off.style.display = "inline";
                            this_submit_reply.style.display = "none";
                            if (response.author != response.user){
                                const SendNotifications = new WebSocket(
                                    ws_scheme +
                                    '://' +
                                    window.location.host +
                                    '/ws/notifications/' +
                                    response.author +
                                    '/'
                                );
                                SendNotifications.onopen = () => SendNotifications.send(JSON.stringify({
                                    'liked': response.user,
                                    'post-no': response.post_number,
                                    'comment-no': response.id
                                }));
                            }
                            new_added_reply = '<div class="comments replies comment-main-level"><div class="comment-avatar">' +
                                              '<a href="' + profile.href + '"><img class="rounded-circle avatar follow-avatars" src="' +
                                              avatar.src +
                                              '"></a></div><div class="comment-box"><div class="comment-head">' +
                                              '<h6 class="comment-name"><a href="' + profile.href + '">' +
                                              response.user +
                                              '</a></h6><span>Now</span>' +
                                              '<div class="arrows"><i class="new_reply_arrow_down fa fa-arrow-down" data-url="' +
                                              response.unlike_url +
                                              '"data-id="' + response.new_reply_id + '" id="down-' + response.new_reply_id +
                                              '"></i><i class="new_reply_arrow_up fa fa-arrow-up" data-url="' +
                                              response.like_url + '" data-id="' + response.new_reply_id +
                                              '" id="up-' + response.new_reply_id + '"></i>' +
                                              '<i id="clcounter-' + response.new_reply_id + '" data-ratio="0' +
                                              '">' + 0 + '</i></div>' +
                                              '<i class="fa fa-trash" data-bs-toggle="modal" data-bs-target="#delete_reply-' +
                                              response.new_reply_id + '"></i>' +
                                              '<div class="modal fade" id="delete_reply-' +
                                              response.new_reply_id + '" tabindex="-1" aria-labelledby="delete_reply_label-' +
                                              response.new_reply_id + '" aria-hidden="true"><div class="modal-dialog"><div class="modal-content">' +
                                              '<div class="modal-header"><h5 class="modal-title black" id="delete_reply_label-' +
                                              response.new_reply_id + '">Delete Comment</h5>' +
                                              '<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>' +
                                              '</div><div class="modal-body">Are you sure you want to delete your comment?</div>' +
                                              '<div class="modal-footer"><button type="button" class="btn btn-secondary" ' +
                                              'data-bs-dismiss="modal">Cancel</button><a class="btn btn-danger" href="' +
                                              response.delete_url + '">Delete Comment</a>' +
                                              '</div></div></div></div></div><div class="comment-content">' +
                                              this_reply_text + '</div></div></div>'

                            $(this_reply_box).after(new_added_reply);
                            // Click on arrow_up button
                            $('.arrows').on('click', '.new_reply_arrow_up', function(e){
                                e.preventDefault();
                                this_button = $(this);
                                url = $(this).attr('data-url');
                                likeArrowUp(this_button, url);
                            })

                            // Click on arrow_up button
                                $('.arrows').on('click', '.new_reply_arrow_down', function(e){
                                    e.preventDefault();
                                    this_button = $(this);
                                    url = $(this).attr('data-url');
                                    likeArrowDown(this_button, url);
                            })

                        }
                        else if(response.success==false){
                            console.log("Error")
                        }
                 },
                 contentType: false,
                 processData: false,

            });
        })

}

// LikeArrowUp
$('.arrows').on('click', '.like_arrow_up', function(e){
    e.preventDefault();
    this_button = $(this);
    url = $(this).attr('data-url');
    likeArrowUp(this_button, url)
})

function likeArrowUp(this_button, url) {
    image = this_button.find('.arrow_up');
    comment_id = this_button.attr('data-id');
    counter_name = "clcounter-" + comment_id;
    this_counter = document.getElementById(counter_name)
    down_arrow = "down-" + comment_id
    this_down_arrow = document.getElementById(down_arrow);
    down_image = $(this_down_arrow).find('.arrow_down');

    $.ajax({
        type: "POST",
        url: url,
        data: {'csrfmiddlewaretoken': csrftoken},
        dataType: "json",
        success: function(response) {
            if(response.liked==true){
                this_button[0].style.color = "#304c75";
                this_down_arrow.style.color = "";
                this_counter.innerHTML = response.count;
            }
            else if(response.liked==false){
                console.log("error")
            }
        }
    })
}

// LikeArrowDown
$('.arrows').on('click', '.like_arrow_down', function(e){
    e.preventDefault();
    this_button = $(this);
    url = $(this).attr('data-url')
    likeArrowDown(this_button, url)
})

function likeArrowDown(this_button, url) {
    image = this_button.find('.arrow_down');
    comment_id = this_button.attr('data-id');
    counter_name = "clcounter-" + comment_id;
    this_counter = document.getElementById(counter_name)
    up_arrow = "up-" + comment_id
    this_up_arrow = document.getElementById(up_arrow);
    up_image = $(this_up_arrow).find('.arrow_up');

    $.ajax({
        type: "POST",
        url: url,
        data: {'csrfmiddlewaretoken': csrftoken},
        dataType: "json",
        success: function(response) {
            if(response.liked==true){
                this_button[0].style.color = "tomato";
                this_up_arrow.style.color = "";
                this_counter.innerHTML = response.count;
            }
            else if(response.liked==false){
                console.log("error")
            }
        }
    })
}