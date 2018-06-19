function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function() {

    $.getJSON('/user/get_name_img/', function (data) {
        if(data.code == '200'){
            $('#user-avatar').attr({'src': '/static/' + data.data.avatar});
            $('#user-name').val(data.data.name);
        }
    });

    $('#avatar').focus(function () {
        $('#avatar-error').hide();
    });

    $('#form-avatar').submit(function (e) {
        e.preventDefault();

        var imageForm = new FormData();
        imageForm.append("avatar", $("avatar")[0]);

        $.ajax({
            url: '/user/avatar/',
            type: 'patch',
            data: new FormData($('#form-avatar')[0]),
            dataType: 'json',
            async: true,
            cashe: false,
            contentType:false,
            processData:false,
            success: function (data) {
                if(data.code == '200'){
                    alert('成功');
                    $('#user-avatar').attr({'src': '/static/' + data.img_url});
                }else{
                    alert(data.msg);
                }
            },
            error: function (error) {
                $('#avatar-error span').html('请求失败！');
                $('#avatar-error').show();
                console.log(error);
            }
        });
    });

    $('#user-name').focus(function () {
        $('#name-error').hide();
    });

    $('#form-name').submit(function (e) {
        e.preventDefault();

        var username = $('#user-name').val().trim();

        if (!username) {
            $("#name-error span").html("用户名不能为空！");
            $("#name-error").show();
            return;
        }

        $.ajax({
            url: '/user/username/',
            type: 'patch',
            data: {'username': username},
            dataType: 'json',
            success: function (data) {
                if(data.code == '200'){
                    alert('成功');
                    $('#user-name').val(username);
                }else{
                    $('#name-error span').html(data.msg);
                    $('#name-error').show();
                }
            },
            error: function (error) {
                $('#name-error span').html('请求失败！');
                $('#name-error').show();
                console.log(error);
            }
        });
    });
});

