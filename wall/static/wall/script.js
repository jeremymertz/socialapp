function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

// Like/Unlike function
$('.like-buttons').on('click', '.like-button', function(e){
    e.preventDefault();
    this_button = $(this);
    post_number = $(this).attr('data-post')
    image = this_button.find('.foo');
    const like_counter = "counter-" + $(this).attr('data-post');
    this_counter = document.getElementById(like_counter);
    current_likes = parseInt($(this_counter).text());

    $.ajax({
             type: "POST",
             url: $(this).attr('data-url'),
             data: {'csrfmiddlewaretoken': csrftoken},
             dataType: "json",
             success: function(response) {
                    if(response.liked==true){
                        likes = (current_likes + 1)
                        image[0].src = "/static/wall/images/like.png";
                        this_counter.innerHTML = likes;
                        if (response.author != response.user){
                            var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
                            const SendNotifications = new WebSocket(
                            ws_scheme
                            + '://'
                            + window.location.host
                            + '/ws/notifications/'
                            + response.author
                            + '/'
                            );
                        SendNotifications.onopen = () => SendNotifications.send(JSON.stringify({
                            'liked': response.user,
                            'post-no': post_number,
                            }));
                        }

                    }
                    else if(response.liked==false){
                        likes = (current_likes - 1)
                        image[0].src = "/static/wall/images/nolike.png";
                        this_counter.innerHTML = likes;
                    }
              }
        });
  })

// Remove file upload
text_upload = document.getElementById("text-upload");
file_upload = document.getElementById("file_upload");
if (file_upload){
    file_upload.addEventListener("change", function(){
        file_upload.style.visibility="hidden";
        text_upload.style.visibility="hidden";
        file_upload.style.height= "20px";
        text_upload.style.height= "0px";
    });
}

// Crop image function
const image_box = document.getElementById('image_box');
const new_post_form = document.getElementById('new_post_form');
const submit_post = document.getElementById('submit_post');
const input = document.getElementById('id_picture');
const zoom = document.getElementById('btn-zoom');

if (input){
    input.addEventListener('change', ()=>{
        const img_data = input.files[0]
        const url = URL.createObjectURL(img_data)
        image_box.innerHTML = `<img src="${url}" id="image">`;
        zoom.style.visibility="visible";

        var $image = $('#image')
        $image.cropper({
            aspectRatio: 9 / 9,
            viewMode: 2,
            background: false,
            dragMode: 'move',
            cropBoxResizable: false,
            minCropBoxHeight: 400,
            minCropBoxWidth: 400,
            crop: function(event) {

            },
        });

        var cropper = $image.data('cropper');
        submit_post.addEventListener("click", function(e){
            e.preventDefault();
            cropper.getCroppedCanvas().toBlob(function (blob) {
                const fd = new FormData();
                fd.append('csrfmiddlewaretoken', csrftoken)
                fd.append('picture', blob, 'my-image.png');
                $.ajax({
                    method: "POST",
                    url: new_post_form.action,
                    enctype: 'multipart/form-data',
                    data: fd,
                    success: function(response){
                        window.location.href = response.next_new_post_link;
                    },
                    error: function(error){
                        console.log('error', error)
                    },
                    cache: false,
                    contentType: false,
                    processData: false,
                    })
                })
            })
            //Zoom_in
            zoom_in = document.getElementById("zoomin");
            zoom_in.addEventListener("click", function(){
                cropper.zoom(0.1);
            });

            //Zoom_out
            zoom_out = document.getElementById("zoomout");
            zoom_out.addEventListener("click", function(){
                    cropper.zoom(-0.1);
            });

            //Rotate_left
            rotate_left = document.getElementById("rotate-left");
            rotate_left.addEventListener("click", function(){
                cropper.rotate(-5);
            });

            //Rotate_right
            rotate_right = document.getElementById("rotate-right");
            rotate_right.addEventListener("click", function(){
                cropper.rotate(5);
            });

            // Right, Left, Up, Down
            move_left = document.getElementById("move-left");
            move_left.addEventListener("click", function(){
                cropper.move(-10, 0);
            });
            move_right = document.getElementById("move-right");
            move_right.addEventListener("click", function(){
                cropper.move(10, 0);
            });
            move_up = document.getElementById("move-up");
            move_up.addEventListener("click", function(){
                cropper.move(0, 10);
            });
            move_bottom = document.getElementById("move-down");
            move_bottom.addEventListener("click", function(){
                cropper.move(0, -10);
            });


            // Cancel image
            cancel_button = document.getElementById("cancel_post");

            cancel_button.addEventListener("click", function(){
                new_image = document.getElementById("image");
                cropper.destroy();
                file_upload.style.visibility="visible";
                zoom.style.visibility="hidden";
                file_upload.style.height= "auto";
                new_post_form.reset();
                new_image.remove();
            });

    })
}
// notification as read
$('#read_notification').on('click', function(e){
    e.preventDefault();
    $.ajax({
        type: "POST",
        url: $(this).attr('data-url'),
        data: {'csrfmiddlewaretoken': csrftoken},
        dataType: "json",
        success: function(response) {
            if(response.success==true){
                document.getElementById('notification').classList.remove("red-dot")
            }
        }
    });
})

// next post
$('#submit_post').on('click', function(e){
    $('#submit-btn').html('<btn class="btn btn-dark"><i class="fa fa-spinner fa-spin"></i><btn>');
})
