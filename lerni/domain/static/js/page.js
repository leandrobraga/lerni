function delConfirm(page_id){
    $("#myModalDel h4").html("Deseja relamente excluir esta página?");
    $("#myModalDel").modal("show");
    $("#yesBtn").click(function(){

        var url = "/domain/topic/page/delete/"+page_id;

        $(window.document.location).attr("href",url);
    });

}