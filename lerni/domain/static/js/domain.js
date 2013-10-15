function delConfirm(id){
    $("#myModalDel h4").html("Deseja relamente excluir o tópico?");
    $("#myModalDel").modal("show");
    $("#yesBtn").click(function(){

        var url = "/domain/topic/delete/"+id;

        $(window.document.location).attr("href",url);
    });

}