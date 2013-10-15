function get_page(student_id){

    $('#content_page').empty();

    var request = $.ajax({
        type:"GET",
        url:"/classRoom/getPage/"+student_id,
        datatype:"json",
    });

    request.done(function(page){
        $('h2').html(page.topic);
        $('#content_page').html(page.content_page);

    });

    request.fail(function(jqXHR, textStatus) {

        alert( "Request failed: " + textStatus );

    });

};

function next_page(student_id){

    var request = $.ajax({
        type:"GET",
        url:"/classRoom/"+student_id+"/nextPage/",
        datatype:"json",
    });

    request.done(function(resp){

        if(resp.sucess == 1){

            $(window.document.location).attr("href","/classRoom/");
        }
        if(resp.sucess == 2){

            $(window.document.location).attr("href","/classRoom/exercise/");

        }

    });

};

function get_exercise(){

    $('#content_page').empty();

    var request = $.ajax({
        type:"POST",
        url:"/classRoom/getExercise/",
        datatype:"json",
    });

    request.done(function(page){
       alert('ok');
    });

    request.fail(function(jqXHR, textStatus) {

        alert( "Request failed: " + textStatus );

    });


};