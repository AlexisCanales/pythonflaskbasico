
//alert("hola");
$(document).ready(function() {
    $("#btnMostrar").click(toggleimg);//va a la funcion
    var tipoUsuario = $("#tipoUsuario").text();//asigna el texto de la etiqueta
    //console.log(tipoUsuario);//se ve en la consola del navegador
    if (tipoUsuario === 'Administrador') {
        $("#divUsuario").show();
    }
});

function toggleimg() {
    $(".imagenTd").toggle();
}

//funcion boton toogle inicio sesion
$('[data-toggle="txtPassword"]').click(function () {//si le hace click al que tiene data-toggle
    const inputPassword = $("#txtPassword"); //recibe variable
    inputPassword.attr("type", inputPassword.attr("type") === "password" ? "text" : "password");//un if escondido
    //cambiar entre iconos
    const icon = inputPassword.attr("type") === "password" ? "fa-eye" : "fa-eye-slash";
    $(this).find("i").removeClass().addClass(`fa-solid ${icon}`);
});

//funcion export
function prepareData() {
    var table = document.getElementById('tabla');
    var rows = table.rows;
    var csv_data = [];
    for (var i = 0; i < rows.length; i++) {
        var cols = rows[i].cells;
        var row_data = [];
        //for (var j = 0; j < cols.length; j++) { //incluye todo hasta los th de update y eliminar
        //for (var j = 0; j < cols.length - 2; j++) {  // Excluir las dos últimas columnas eliminar y update
        for (var j = 1; j < cols.length - 2; j++) { //esta excluye la 1ra de # y las 2 ultimas de delete y update
            row_data.push(cols[j].innerText);
        }
        csv_data.push(row_data.join(','));
    }
    document.getElementById('table_data').value = csv_data.join('\n');
}