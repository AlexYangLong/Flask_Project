function logout() {
    $.get("/api/logout", function(data){
        if (0 == data.errno) {
            location.href = "/";
        }
    })
}

$(document).ready(function(){
    $.getJSON('/user/get_name_img/', function (data) {
        if(data.code == '200'){
            $('#user-avatar').attr({'src': '/static/' + data.data.avatar});
            $('#user-name').text(data.data.name);
            $('#user-mobile').text(data.data.phone);
        }
    });
});