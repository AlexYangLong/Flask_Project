$(document).ready(function(){
    $(".auth-warn").show();
});

$(document).ready(function(){
     $.getJSON('/user/auth_info/', function (data) {
         if (data.code == '200') {
             if (data.data.id_card) {
                 $('.auth-warn').hide();
                 $('#houses-list').show();

                 getHouseList();
             }else{
                 $('.auth-warn').show();
                 $('#houses-list').hide();
             }
         }
     });
});

function getHouseList() {
    $.getJSON('/house/house_list/', function (data) {
        if (data.code == '200') {
            var list = '';
            for (var i=0;i<data.data_list.length;i++){
                list += '<li>';
                list += '<a href=\"/house/house_detail/?hid='+data.data_list[i].id+'\">';
                list += '<div class=\"house-title\">';
                list += '<h3>房屋ID:'+data.data_list[i].id+' —— '+data.data_list[i].title+'</h3>';
                list += '</div><div class=\"house-content\">';
                if (data.data_list[i].image != '') {
                    list += '<img src=\"/static/upload/' + data.data_list[i].image + '\">';
                }else{
                    list += '<img src=\"/static/images/no-house-img.png\">';
                }
                list += '<div class=\"house-text\"><ul>';
                list += '<li>位于：'+data.data_list[i].area+'</li>';
                list += '<li>价格：￥'+data.data_list[i].price+'/晚</li>';
                list += '<li>发布时间：'+data.data_list[i].create_time+'</li>';
                list += '</ul></div></div></a></li>';
            }
            $('#houses-list').append(list);
        }else {
            alert(data.msg);
        }
    });
}