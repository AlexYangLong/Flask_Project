function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1500);
    });
}

$(document).ready(function () {

    $.getJSON('/user/auth_info/', function (data) {
        if(data.code == '200'){
            if(data.data.id_card){
                $('#real_name').val(data.data.id_name);
                $('#real_name').attr({'readonly': 'readonly'});
                $('#id_card').val(data.data.id_card);
                $('#id_card').attr({'readonly': 'readonly'});
                $('.btn-success').hide();

                $('.popup p').html('已实名认证，如需修改请联系客服！');
                showSuccessMsg();
            }
        }else {
            $('.popup p').html(data.msg);
            showSuccessMsg();
        }
    });

    $("#real_name").focus(function(){
        $("#error-msg").hide();
    });
    $("#id_card").focus(function(){
        $("#error-msg").hide();
    });

    $('#form-auth').submit(function (e) {
        e.preventDefault();

        var real_name = $("#real_name").val().trim();
        var id_card = $("#id_card").val().trim();

        if (!real_name) {
            $("#error-msg span").html("真实姓名不能为空！");
            $("#error-msg").show();
            return;
        }
        if (!id_card) {
            $("#error-msg span").html("身份证号不能为空！");
            $("#error-msg").show();
            return;
        }

        $.ajax({
            url: '/user/authenticate/',
            type: 'patch',
            data: {'real_name': real_name, 'id_card': id_card},
            dataType: 'json',
            success: function (data) {
                if(data.code == '200'){
                    $('.btn-success').hide()
                    $('.popup p').html(data.msg);
                    showSuccessMsg();
                    $('#real_name').attr({'readonly': 'readonly'});
                    $('#id_card').attr({'readonly': 'readonly'});
                }
                else{
                    $('.popup p').html(data.msg);
                    showSuccessMsg();
                }
                //(data.code == '1001')
                // else if(data.code == '1002'){
                //     $('#result span').html('手机号码格式错误');
                //     $('#result').show();
                // }
                // else if(data.code == '1003'){
                //     $('#result span').html('两次密码不一致');
                //     $('#result').show();
                // }
                // else if(data.code == '1004'){
                //     $('#result span').html('手机号已被注册！');
                //     $('#result').show();
                // }
                // else if(data.code == '1005'){
                //     $('#result span').html('用户名已存在！');
                //     $('#result').show();
                // }
            },
            error: function (error) {
                $('.popup p').html('请求失败！');
                showSuccessMsg();
                console.log(error);
            }
        });
    });
});

