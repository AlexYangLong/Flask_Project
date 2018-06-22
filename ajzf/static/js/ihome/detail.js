function hrefBack() {
    history.go(-1);
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function(){
    var hid = decodeQuery().hid;
    //alert(hid);

    $.getJSON('/house/house_info/' + hid +'/', function (data) {
        if(data.code == '200'){
            var house = data.data;
            if(house.images.length > 0) {
                for (var i = 0; i < house.images.length; i++) {
                    $('.swiper-wrapper').append('<li class=\"swiper-slide\"><img src=\"/static/upload/' + house.images[i] + '\"></li>');
                }
            }else{
                $('.swiper-wrapper').append('<li class=\"swiper-slide\"><img src=\"/static/images/no-house-img.png\"></li>');
            }
            $('.house-price span').html(house.price);
            $('.house-title').html(house.title);
            $('.landlord-pic img').attr({'src': '/static/upload/'+house.user_avatar});
            $('.landlord-name span').html(house.user_name);
            $('#address').html(house.address);
            $('#room_count').html(house.room_count);
            $('#acreage').html(house.acreage);
            $('#unit').html(house.unit);
            $('#capacity').html(house.capacity);
            $('#beds').html(house.beds);
            $('#deposit').html(house.deposit);
            $('#min_days').html(house.min_days);
            if(house.max_days == '0') {
                $('#max_days').html('无限制');
            } else {
                $('#max_days').html(house.max_days);
            }
            for(var i=0;i<house.facilities.length;i++){
                $('.house-facility-list').append('<li><span class=\"'+house.facilities[i].css+'\"></span>'+house.facilities[i].name+'</li>');
            }

            for(var i=0;i<data.comments.length;i++){
                $('.house-comment-list').append('<li><p>'+data.comments[i].user_name+'<span class=\"fr\">'+data.comments[i].create_date+'</span></p><p>'+data.comments[i].comment+'</p></li>');
            }

            var mySwiper = new Swiper ('.swiper-container', {
                loop: true,
                autoplay: 2000,
                autoplayDisableOnInteraction: false,
                pagination: '.swiper-pagination',
                paginationType: 'fraction'
            });

            $(".book-house").attr({'href': '/book/booking/?hid='+house.id})
            $(".book-house").show();
        }else {
            alert(data.msg);
        }
    });
});