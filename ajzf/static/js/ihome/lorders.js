//模态框居中的控制
function centerModals(){
    $('.modal').each(function(i){   //遍历每一个模态框
        var $clone = $(this).clone().css('display', 'block').appendTo('body');    
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 0 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", top-30);  //修正原先已经有的30个像素
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){});
        },1500)
    });
}

$(document).ready(function(){
    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);

    $.getJSON('/book/custom_orders_list/', function (data) {
        console.log(data)
        if(data.code == '200') {
            var orders = {
                'orders': data.data_list
            }
            var html = template("orders-list-tmpl", orders);
            $('.orders-list').html(html);
        }else{
            var orders = {
                'orders': ''
            }
            var html = template("orders-list-tmpl", orders);
            $('.orders-list').html(html);
        }
        $(".order-accept").on("click", function(e){
            var orderId = $(this).parents("li").attr("order-id");
            $(".modal-accept").attr("order-id", orderId);
            $('#accept-modal').modal("show");
        });

        $(".order-reject").on("click", function(){
            var orderId = $(this).parents("li").attr("order-id");
            $(".modal-reject").attr("order-id", orderId);
            $('#reject-modal').modal("show");
        });
    });

    $('.modal-accept').on('click', function (e) {
        e.preventDefault();
        var oid = $(".modal-accept").attr("order-id");
        var status = '待支付';
        change_order_status(oid, status, '', $('#accept-modal'));
    });

    $('.modal-reject').on('click', function (e) {
        e.preventDefault();
        var oid = $(".modal-reject").attr("order-id");
        var status = '已拒单';
        var comment = $('#reject-reason').val().trim();
        change_order_status(oid, status, comment, $('#reject-modal'));
    });
});

function change_order_status(oid, status, comment, element) {
    $.ajax({
        url: '/book/change_order_status/',
        type: 'patch',
        data: {'oid': oid, 'status': status, 'comment': comment},
        dataType: 'json',
        success: function (data) {
            //隐藏模态框
            element.modal("hide");
            $('.popup p').html(data.msg);
            showSuccessMsg();
            if(data.code == '200'){
                $('li[order-id=\"'+oid+'\"] .order-title div').hide();
                $('li[order-id=\"'+oid+'\"] .order-text ul li:eq(4) span').html(status);
                if(status == '已拒单'){
                    $('li[order-id=\"'+oid+'\"] .order-text ul').append('<li>拒单原因： '+comment+'</li>');
                }
            }
        },
        error: function (error) {
            $('.popup p').html('请求失败！');
            showSuccessMsg();
            console.log(error);
        }
    });
}