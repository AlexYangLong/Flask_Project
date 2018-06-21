function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){});
        },1500);
    });
}

$(document).ready(function(){
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');

    $.getJSON('/house/area_facility/', function (data) {
        if (data.code == '200'){
            areas = data.area_list;
            for(var i=0;i<areas.length;i++){
                $('#area_id').append('<option value=\"'+ areas[i].id +'\">'+ areas[i].name +'</option>')
            }
            facilities = data.facility_list;
            f_list = '';
            for(var i=0;i<facilities.length;i++){
                f_list += '<li><div class=\"checkbox\"><label><input type=\"checkbox\" name=\"facility\" value=\"'+facilities[i].id+'\">'+facilities[i].name+'</label></div></li>';
            }
            $('.house-facility-list').append(f_list);
        }
    });

    $('#form-house-info').submit(function (e) {
        e.preventDefault();

        var title = $('#house-title').val().trim();
        var price = $('#house-price').val().trim();
        var area_id = $('#area_id').val().trim();
        var address = $('#house-address').val().trim();
        var room_count = $('#house-room-count').val().trim();
        var acreage = $('#house-acreage').val().trim();
        var unit = $('#house-unit').val().trim();
        var capacity = $('#house-capacity').val().trim();
        var beds = $('#house-beds').val().trim();
        var deposit = $('#house-deposit').val().trim();
        var min_days = $('#house-min-days').val().trim();
        var max_days = $('#house-max-days').val().trim();
        obj = $('input[type=checkbox]');
        var check_val = '';
        for(k in obj){
            if(obj[k].checked)
                check_val += obj[k].value + ',';
        }

        var info = {
            'title': title,
            'price': price,
            'area_id': area_id,
            'address': address,
            'room_count': room_count,
            'acreage': acreage,
            'unit': unit,
            'capacity': capacity,
            'beds': beds,
            'deposit': deposit,
            'min_days': min_days,
            'max_days': max_days,
            'check_val': check_val
        }

        $.ajax({
            url: '/house/publish_house/',
            type: 'post',
            data: info,
            dataType: 'json',
            success: function (data) {
                if(data.code == '200'){
                    $('#house-id').val(data.data.id);
                    $('.popup p').html(data.msg);
                    showSuccessMsg();
                    $('#form-house-info').hide();
                    $('#form-house-image').show();
                }else {
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

    $('#form-house-image').submit(function (e) {
        e.preventDefault();

        $(this).ajaxSubmit({
            url: '/house/upload_image/',
            type: 'post',
            dataType: 'json',
            success: function (data) {
                $('.popup p').html(data.msg);
                showSuccessMsg();
                if(data.code == '200'){
                    window.parent.location.href = '/house/my_house/';
                }
            },
            error: function (error) {
                $('.popup p').html('请求失败！');
                showSuccessMsg();
                console.log(error);
            }
        });
    });
})