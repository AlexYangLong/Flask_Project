function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1500)
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function() {

    $.getJSON('/user/get_name_img/', function (data) {
        if(data.code == '200'){
            if(data.data.avatar) {
                $('#user-avatar').attr({'src': '/static/upload/' + data.data.avatar});
            }
            $('#user-name').val(data.data.name);
        }
    });

    $('#avatar').focus(function () {
        $('#avatar-error').hide();
    });

    // 上传文件 方法1：
    $('#form-avatar').submit(function (e) {
        e.preventDefault();
        $(this).ajaxSubmit({
            url: '/user/avatar/',
            type: 'patch',
            dataType: 'json',
            success: function (data) {
                if(data.code == '200'){
                    $('.popup p').html(data.msg);
                    showSuccessMsg();
                    $('#user-avatar').src = '/static/upload/' + data.img_url;
                }else{
                    $('.popup p').html(data.msg);
                    showSuccessMsg();
                }
            },
            error: function (error) {
                $('.popup p').html('请求失败！');
                showSuccessMsg();
                console.log(error);
            }
        });
    });

    // 上传文件 方法2：
    // $('#form-avatar').submit(function (e) {
    //     e.preventDefault();
    //
    //     var imageForm = new FormData();
    //     imageForm.append("avatar", $("avatar")[0]);
    //
    //     $.ajax({
    //         url: '/user/avatar/',
    //         type: 'patch',
    //         data: new FormData($('#form-avatar')[0]),
    //         dataType: 'json',
    //         async: true,
    //         cashe: false,
    //         contentType:false,
    //         processData:false,
    //         success: function (data) {
    //             if(data.code == '200'){
    //                 alert('成功');
    //                 $('#user-avatar').attr({'src': '/static/' + data.img_url});
    //             }else{
    //                 alert(data.msg);
    //             }
    //         },
    //         error: function (error) {
    //             $('#avatar-error span').html('请求失败！');
    //             $('#avatar-error').show();
    //             console.log(error);
    //         }
    //     });
    // });

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
                    $('.popup p').html(data.msg);
                    showSuccessMsg();
                    $('#user-name').val(username);
                }else{
                    $('.popup p').html(data.msg);
                    showSuccessMsg();
                }
            },
            error: function (error) {
                $('.popup p').html(data.msg);
                showSuccessMsg();
                console.log(error);
            }
        });
    });
});

