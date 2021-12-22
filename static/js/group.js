// noinspection SpellCheckingInspection

$(document).ready(function () {

    $('.unfollow_group').submit(function (e) {
        e.preventDefault();
        const url = $(this).attr('action');
        const group_id = $(this).attr('id');
        const follower_count = document.getElementById("follower-count");



        $.ajax({
            type: 'POST',
            url: url,
            data: {
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                'group_id': group_id
            },
            success: function (response) {
                if (response['response'] === "success") {
                    $('.unfollow_group')[0].style.display = 'none'
                    $('.follow_group')[0].style.display = 'block'


                    follower_count.innerText=response['count'] + " subscribers"

                } else {
                    alert('Error 404');
                }

            },
            error: function (response) {
                console.error('error', response)
            }
        })
    });

    $('.follow_group').submit(function (e) {
        e.preventDefault();
        const url = $(this).attr('action');
        const group_id = $(this).attr('id');
        const follower_count = document.getElementById("follower-count");


        $.ajax({
            type: 'POST',
            url: url,
            data: {
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                'group_id': group_id
            },
            success: function (response) {
                if (response['response'] === "success") {

                    $('.follow_group')[0].style.display = 'none'
                    $('.unfollow_group')[0].style.display = 'block'

                    follower_count.innerText=response['count'] + " subscribers"
                } else {
                    alert('Error 404');
                }
                console.error(response)

            },
            error: function (response) {
                console.error('error', response)
            }
        })
    });

});
