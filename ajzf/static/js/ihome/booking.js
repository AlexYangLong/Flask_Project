function hrefBack() {
    history.go(-1);
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

function showErrorMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1500)
    });
}

$(document).ready(function(){
    var hid = decodeQuery().hid;
    $.getJSON('/house/house_info/' + hid +'/', function (data) {
        if(data.code == '200'){
            if(data.data.images.length > 0) {
                $('.house-info img').attr({'src': '/static/upload/' + data.data.images[0]});
            }else{
                $('.house-info img').attr({'src': '/static/images/no-house-img.png'});
            }
            $('.house-text h3').html(data.data.title);
            $('.house-text p:eq(0) span').html(data.data.price);
            $('.house-text p:last').html(data.data.address);
        }else {
            $('.popup p').html(data.msg);
            showErrorMsg();
        }
    });

    $(".input-daterange").datepicker({
        format: "yyyy-mm-dd",
        startDate: "today",
        language: "zh-CN",
        autoclose: true
    });
    $(".input-daterange").on("changeDate", function(){
        var startDate = $("#start-date").val();
        var endDate = $("#end-date").val();

        if (startDate == '' || endDate == '' || startDate > endDate) {
            $('.popup p').html('日期有误，请重新选择！');
            showErrorMsg();
        } else {
            var sd = new Date(startDate);
            var ed = new Date(endDate);
            days = (ed - sd)/(1000*3600*24) + 1;
            var price = $(".house-text>p>span").html();
            var amount = days * parseFloat(price);
            $(".order-amount>span").html(amount.toFixed(2) + "(共"+ days +"晚)");
        }
    });
    $('.submit-btn').on('click', function (e) {
        e.preventDefault();

        var startDate = $("#start-date").val();
        var endDate = $("#end-date").val();

        if (startDate == '' || endDate == '' || startDate > endDate) {
            $('.popup p').html('日期有误，请重新选择！');
            showErrorMsg();
            return;
        }
        days = (new Date(endDate) - new Date(startDate))/(1000*3600*24) + 1;
        var price = $(".house-text>p>span").html();
        var amount = days * parseFloat(price);

        $.ajax({
            url: '/book/check_in/',
            type: 'post',
            data: {'hid': hid, 'begin': startDate, 'end': endDate, 'days': days, 'price': price, 'amount': amount},
            dataType: '',
            success: function (data) {
                if(data.code == '200'){
                    $('.popup p').html('下单成功！');
                    showErrorMsg();
                    //跳转到订单页面
                    window.parent.location.href = '/book/my_orders/';
                }else {
                    $('.popup p').html(data.msg);
                    showErrorMsg();
                }
            },
            error: function (error) {
                $('.popup p').html('请求失败！');
                showErrorMsg();
                console.log(error);
            }
        });
    });
});
