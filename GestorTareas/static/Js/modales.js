$(document).ready(function(){
    $("#btnActualizar").click(function(){  //Se llama el boton
        cargamodal.load("Templates/Modaltareas.html"); //Aqui se esta llamando el modal para que cargue la ruta y luego la ventana
    });

    function cargamodal(){
        $("#Mtareas").load(ruta,function(){
            $("#Mtareas").modal("show");
        });
    }
});

