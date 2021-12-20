// noinspection SpellCheckingInspection,JSUnresolvedVariable,HtmlUnknownAttribute

$(document).ready(function () {

    $('.like_form').submit(function (e) {
        e.preventDefault()
        const post_id = $(this).attr('id');
        const type = $("input[name='type']", this).val();
        const url = $(this).attr('action');
        let res;

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
                        $(`#dislike-img${post_id}`).attr('src', 'static/src/icon/filled_like.svg');
                        $(`#like-img${post_id}`).attr('src', 'static/src/icon/like.svg');
                    } else {
                        $(`#dislike-img${post_id}`).attr('src', 'static/src/icon/like.svg');
                    }
                    res = parseInt(response.likes)
                } else if (type === 'like') {

                    if (response.is_liked === false) {
                        $(`#like-img${post_id}`).attr('src', 'static/src/icon/filled_like.svg');
                        $(`#dislike-img${post_id}`).attr('src', 'static/src/icon/like.svg');
                    } else {
                        $(`#like-img${post_id}`).attr('src', 'static/src/icon/like.svg');
                    }
                    res = parseInt(response.likes)
                }

                $(`#like-counter${post_id}`).text(res)
            },
            error: function (response) {
                console.error('error', response)
            }
        })
    })


    $('.comment_form').submit(function (e) {
        e.preventDefault();

        const post_id = $("input[name='id']", this).val();
        const url = $(this).attr('action');
        const parent_id = $("input[name='parent_id']", this).val();
        const body = $(e.target[1]).val();

        $.ajax({
            type: 'POST',
            url: url,
            data: {
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                'post_id': post_id,
                'parent_id': parent_id,
                'body': body
            },
            success: function (response) {

                let replies = '<div class="replies" id="replies' + response.comment_id + '"></div>';
                const comment_body = '<div class="comment-body"> <p>' + response.comment_body + '</p> <button class="reply-button" userName="' + response.author + '" type="button" id="comment-reply' + response.comment_id + ' " post_id="' + response.post_id + '">Reply </button> </div>'
                const comment_heading = '<div class="comment-heading"> <div class="comment-info"> <a href="#" class="comment-author">' + response.author + '</a> <p class="m-0"> ' + response.date + ' </p> </div> </div>'
                const comment = '<div class="col-xs-6" id="comment' + response.comment_id + '">' + comment_heading + comment_body + replies + '</div>'
                const comment_list = "#comment-list" + response.post_id

                if (response.parent_id !== null) {
                    replies = "#replies" + response.parent_id
                    $(replies).append(comment);
                } else {
                    $(comment_list).append(comment);
                }

                $(e.target[1]).val('').focus();

            },
            error: function (response) {
                console.error('error', response)
            }
        })
    })

});

$(document).on('click', '.btn-comment', function (event) {
    const comment = "comment-list" + event.currentTarget.id
    const post_id = $(this).attr('id')
    if (document.getElementById(comment).style.display === 'none') {
        document.getElementById(comment).style.display = 'block';
        document.getElementById('comment-form' + post_id).style.display = 'block';

    } else {
        document.getElementById(comment).style.display = 'none';
        document.getElementById('comment-form' + post_id).style.display = 'none';
    }
});

$(document).on('click', '.reply-button', function (event) {

    const post_id = $(this).attr('post_id');
    const comment_id = event.target.id.replace(/\D/g, '');

    let userName = $(this).attr('userName');

    $($('#comment-form' + post_id)[0][1]).val(userName + ', ').focus();

    document.getElementById('cancel-reply' + post_id).style.display = 'block';

    $('<input>').attr({
        type: 'hidden',
        name: 'parent_id',
        value: comment_id
    }).appendTo('.comment_form');

});


$(document).on('click', '.button-cancel', function (event) {

    const post_id = $(this).attr('post_id');
    document.getElementById('cancel-reply' + post_id).style.display = 'none';
    $("input[name='parent_id']").remove();

    $(event.target.form[1]).val('').focus();
});

