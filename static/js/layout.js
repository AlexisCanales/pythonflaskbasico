
//alert("hola");
$(document).ready(function() {
    $("#btnMostrar").click(toggleimg);
});

function toggleimg() {
    $(".imagenTd").toggle();
}

//funcion toogle password escrita abreviada
$('[data-toggle="txtPassword"]').click(function () {//si le hace click al que tiene data-toggle
    const inputPassword = $("#txtPassword"); //recibe variable
    inputPassword.attr("type", inputPassword.attr("type") === "password" ? "text" : "password");//un if escondido
    //cambiar entre iconos
    const icon = inputPassword.attr("type") === "password" ? "fa-eye" : "fa-eye-slash";
    $(this).find("i").removeClass().addClass(`fa-solid ${icon}`);
});