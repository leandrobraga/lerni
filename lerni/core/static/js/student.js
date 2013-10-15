function delConfirm(id,name){
    $("#myModalDel h4").html("Deseja relamente excluir o usuário "+name+"?");
    $("#myModalDel").modal("show");
    $("#yesBtn").click(function(){

        var url = "/managerStudent/delete/"+id;

        $(window.document.location).attr("href",url);
    });

}


function viewUser(id){
    $('#nameOnView').empty();
    $('#emailOnView').empty();
    $('#idOnView').empty();
    $('#userOnView').empty();
    $('#dateJoinOnView').empty();
    $('#lastLoginOnView').empty();

    var request = $.ajax({
        type:"GET",
        url:"/managerStudent/detail/"+id,
        datatype:"json",
    });

    request.done(function(studentJson){
        $('#nameOnView').html(studentJson.name);
        $('#emailOnView').html(studentJson.email);
        $('#idOnView').html(studentJson.id);
        $('#userOnView').html(studentJson.user);
        $('#dateJoinedOnView').html(studentJson.date_joined);
        $('#lastLoginOnView').html(studentJson.last_login);

    });

    request.fail(function(jqXHR, textStatus) {

        alert( "Request failed: " + textStatus );

    });

    $("#myModalView").modal("show");

}