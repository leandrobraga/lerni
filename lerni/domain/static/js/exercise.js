function viewDetail(id){
    $('#topicOnView').empty();
    $('#questionOnView').empty();
    $('#answer1OnView').empty();
    $('#answer2OnView').empty();
    $('#answer3OnView').empty();
    $('#answer4OnView').empty();
    $('#correctAnswerOnView').empty();
    $('#levelOnView').empty();
    $('#kindOnView').empty();
    $('#timeOnView').empty();

    var request = $.ajax({
        type:"GET",
        url:"/domain/exercise/detail/"+id,
        datatype:"json",
    });

    request.done(function(exercise){

        $('#topicOnView').html(exercise.topic);
        $('#questionOnView').html(exercise.question);
        $('#answer1OnView').html(exercise.answer1);
        $('#answer2OnView').html(exercise.answer2);
        $('#answer3OnView').html(exercise.answer3);
        $('#answer4OnView').html(exercise.answer4);
        $('#correctAnswerOnView').html(exercise.correctAnswer);
        if(exercise.level == 1){
            var level = 'Fácil';
        }
        else if(exercise.level == 2){
            var level = 'Médio';
        }
        else if(exercise.level == 3){
            var level = 'Difícil';
        }
        $('#levelOnView').html(level);
        $('#kindOnView').html(exercise.kind);
        $('#timeOnView').html(exercise.time);

    });

    request.fail(function(jqXHR, textStatus) {

        alert( "Request failed: " + textStatus );

    });

    $("#myModalView").modal("show");

}

function delConfirm(theoretical_id){
    $("#myModalDel h4").html("Deseja relamente excluir este exercício?");
    $("#myModalDel").modal("show");
    $("#yesBtn").click(function(){

        var url = "/domain/exercise/delete/"+theoretical_id;

        $(window.document.location).attr("href",url);
    });

}