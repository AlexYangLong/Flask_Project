$(document).ready(function(){
    $(".auth-warn").show();
});

$(document).ready(function(){
     $.getJSON('/user/auth_info/', function (data) {
         if (data.code == '200') {
             if (data.data.id_card != '') {
                 $('.auth-warn').hide();
                 $('#houses-list').show();
             }else{
                 $('.auth-warn').show();
                 $('#houses-list').hide();
             }
         }
     });
});