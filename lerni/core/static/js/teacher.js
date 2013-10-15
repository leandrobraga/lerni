function delConfirm(id,name){
                $("#myModalDel h4").html("Deseja relamente excluir o usuário "+name+"?");
                $("#myModalDel").modal("show");
                $("#yesBtn").click(function(){

                    var url = "/managerTeacher/delete/"+id;

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
                    url:"/managerTeacher/detail/"+id,
                    datatype:"json",
                });
                request.done(function(teacherJson){
                    $('#nameOnView').html(teacherJson.name);
                    $('#emailOnView').html(teacherJson.email);
                    $('#idOnView').html(teacherJson.id);
                    $('#userOnView').html(teacherJson.user);
                    $('#dateJoinedOnView').html(teacherJson.date_joined);
                    $('#lastLoginOnView').html(teacherJson.last_login);


                });
                request.fail(function(jqXHR, textStatus) {
                    alert( "Request failed: " + textStatus );

                });

                $("#myModalView").modal("show");

            }