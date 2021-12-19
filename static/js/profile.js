// noinspection SpellCheckingInspection

$(document).ready(function () {

    $('.delete_friend').submit(function (e) {
        e.preventDefault();
        const url = $(this).attr('action');
        const receiver_id = $(this).attr('id')
        const request_id = $("input[name='request_id']", this).val();

        $.ajax({
            type: 'POST',
            url: url,
            data: {
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                'receiver_id': receiver_id,
                'request_id': request_id
            },
            success: function (response) {
                if (response['response'] === "success") {
                    $('.delete_friend').attr("action", "send_friend_request").removeClass('delete_friend').addClass('send_request')
                    $('#delete_friend_button').removeClass('btn-primary').addClass('btn-danger').attr("id", "send_request_button").text("Отправить предложение дружбы")
                } else {
                    alert('Error 404');
                }

            },
            error: function (response) {
                console.error('error', response)
            }
        })
    });

    $('.accept_request').submit(function (e) {
        e.preventDefault();
        const url = $(this).attr('action');
        const receiver_id = $(this).attr('id')
        const request_id = $("input[name='request_id']", this).val();
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                'receiver_id': receiver_id,
                'request_id': request_id
            },
            success: function (response) {
                if (response['response'] === "success") {
                    $('.accept_request').attr("action", "delete_friend").removeClass('accept_request').addClass('delete_friend')
                    $('#accept_friend_button').removeClass('btn-primary').addClass('btn-danger').attr("id", "delete_friend_button").text("Удалить")

                } else {
                    alert('Error 404');
                }

            },
            error: function (response) {
                console.error('error', response)
            }
        })
    });

    $('.send_request').submit(function (e) {
        e.preventDefault();
        const url = $(this).attr('action');
        const receiver_id = $(this).attr('id')

        console.log(receiver_id)
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                'receiver_id': receiver_id,
            },
            success: function (response) {
                if (response['response'] === "success") {

                    $('.send_request')[0].style.display = 'none';
                    $('.cancel_request')[0].style.display = 'block';


                } else {
                    alert('Error 404');
                }

            },
            error: function (response) {
                console.error('error', response)
            }
        })
    });

    $('.cancel_request').submit(function (e) {
        e.preventDefault();
        const url = $(this).attr('action');
        const receiver_id = $(this).attr('id')
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                'receiver_id': receiver_id,
            },
            success: function (response) {
                if (response['response'] === "success") {

                    $('.cancel_request')[0].style.display = 'none'
                    $('.send_request')[0].style.display = 'block'

                } else {
                    alert('Error 404');
                }

            },
            error: function (response) {
                console.error('error', response)
            }
        })
    });

});
