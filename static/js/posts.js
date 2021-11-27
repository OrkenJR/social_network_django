var isRotated = false;

function rotate(event) {



    console.log('afafadfafasf')
    if (!isRotated) {
        document.getElementById('down-icon').classList.add('rotated');
        document.getElementById('header-popover').classList.add('popover-opened');
        event.stopPropagation();

        document.addEventListener('click', function ($event) {

            let isClickedOutside = true;
            let isClickedPersonInfoWrapper = false;

            for (const path of $event.composedPath()) {
                if (path.id === 'header-popover') {
                    isClickedOutside = false;
                }
                if (path.id === 'person-info-wrapper-id') {
                    isClickedPersonInfoWrapper = true;
                }
            }

            if (isClickedOutside) {
                document.removeEventListener('click', arguments.callee, false);

                if (!isClickedPersonInfoWrapper) {
                    document.getElementById('person-info-wrapper-id').click();
                }
            }

        });
    } else {
        document.getElementById('down-icon').classList.remove('rotated');
        document.getElementById('header-popover').classList.remove('popover-opened');
    }

    isRotated = !isRotated;

}


function makePostCall(body, parent_id, token) {

}

$(document).ready(function () {
    let display = false

    $('.like_form').submit(function (e) {
        e.preventDefault()
        const post_id = $(this).attr('id')
        const type = $("input[name='type']", this).val();
        const url = $(this).attr('action')
        const likes = parseInt($(`#like-counter${post_id}`).text())
        // const user_id = {{ user.id }}
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                'post_id': post_id,
                'type': type
            },
            success: function (response) {
                if (type === 'dislike') {


                    if (response.is_liked === false) {
                        $(`#dislike-img${post_id}`).attr('src', 'static/src/icon/filled_like.png');
                        $(`#like-img${post_id}`).attr('src', 'static/src/icon/like.svg');
                    } else {
                        $(`#dislike-img${post_id}`).attr('src', 'static/src/icon/like.svg');
                    }
                    res = parseInt(response.likes)
                } else if (type === 'like') {

                    if (response.is_liked === false) {
                        $(`#like-img${post_id}`).attr('src', 'static/src/icon/filled_like.png');
                        $(`#dislike-img${post_id}`).attr('src', 'static/src/icon/like.svg');
                    } else {
                        $(`#like-img${post_id}`).attr('src', 'static/src/icon/like.svg');
                    }
                    res = parseInt(response.likes)
                }

                $(`#like-counter${post_id}`).text(res)
            },
            error: function (response) {
                console.log('error', response)
            }
        })
    })


    $('.comment_form').submit(function (e) {


        // {#const post_id = $(this).attr('id');#}
        const post_id = $("input[name='id']", this).val();
        const url = $(this).attr('action');
        // const user_id = {{ user.id }};
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                'post_id': post_id,
                'body': body
            },
            success: function (response) {

                console.log(response.comments)
            },
            error: function (response) {
                console.log('error', response)
            }
        })
    })

});
$(document).on('click', '.btn-comment', function (event) {
    const comment = "comment-list" + event.currentTarget.id

    if (document.getElementById(comment).style.display === 'none') {
        document.getElementById(comment).style.display = 'block';
    } else {
        document.getElementById(comment).style.display = 'none';
    }
});

$(document).on('click', '.reply-button', function (event) {

    const post_id = $(this).attr('post_id')
    comment_id = event.target.id.replace(/\D/g, '');


    document.getElementById('cancel-reply' + post_id).style.display = 'block';


    console.log(post_id)
    // {#$(`#form-id${post_id}`)#}


});


$(document).on('click', '.button-cancel', function (event) {

    const post_id = $(this).attr('post_id')

    // {#const post_id = $("input[name='id']",this).val();#}
    comment_id = event.target.id.replace(/\D/g, '');


    document.getElementById('cancel-reply' + post_id).style.display = 'none';


    // {#$(`#form-id${post_id}`)#}


});
