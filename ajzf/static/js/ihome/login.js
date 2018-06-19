function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function() {
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
    });
    $("#btn-login").on('click', function(e){
        e.preventDefault();
        mobile = $("#mobile").val();
        passwd = $("#password").val();
        if (!mobile) {
            $("#mobile-err span").html("用户名或手机号不能为空！");
            $("#mobile-err").show();
            return;
        } 
        if (!passwd) {
            $("#password-err span").html("密码不能为空！");
            $("#password-err").show();
            return;
        }

        $.ajax({
            url: '/user/login/',
            type: 'post',
            data: {'mobile': mobile, 'password': passwd},
            dataType: 'json',
            success: function (data) {
                if(data.code == '200'){
                    window.parent.location.href = '/user/mine/';
                }
                else{
                    $('#result span').html('用户名或密码错误！');
                    $('#result').show();
                }
            },
            error: function (error) {
                $('#result span').html('请求失败！');
                $('#result').show();
                console.log(error);
            }
        });
    });
})