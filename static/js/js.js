// JavaScript Document

var a;
a= $(document);
a.ready(iniciar);

function iniciar(){
   alert("funciona"); 
  //$("#mensaje").hide(); //si se pone al principio funciona
    //llenarcomboveh();
  //llenarcombofor();
  //llenartabla();


}

//foco rapido

function hola(){
    alert("llego al focus");

}




$(function(){
/*original
  $('a[href*=#menu]').click(function() {
se cambio a menu para que solo hiciera esa funcion con los id que tuvieras
menu en su id y asi no tendria el error con el carousel
  */
     $('a[href*=#menu]').click(function() {

     if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'')
         && location.hostname == this.hostname) {

             var $target = $(this.hash);

             $target = $target.length && $target || $('[name=' + this.hash.slice(1) +']');

             if ($target.length) {

                 var targetOffset = $target.offset().top;

                 $('html,body').animate({scrollTop: targetOffset}, 1000);

                 return false;

            }

       }

   });

});




function sesion(){
  //alert("llego a la funcion sesion js"); 
window.location="inicio.php";

}


function llenarcomboveh(){
      $.get('intermediario.php','combo=1',
    function(data){
       $("#cboveh").html(data);
    });
}

function llenarcombofor(){
      $.get('intermediario.php','combofor=1',
    function(data){
       $("#cbofor").html(data);
    });
}

function llenartabla(){
  $("#pdf").hide();
  $("#excel").show();
  $("#txtrut2").attr("value",""); //para limpiar casilla
  $.get('intermediario.php','tabla=1',
    function(data){
       $("#tably").html(data);
    });
}


function guardar(){
  var btnenv,txtrut,txtnom,cboveh,txtcos,cbonum,txtobs,cbofor,txtfec;
    btnenv=$("#btnenv").val();
    txtrut=$("#txtrut").val();
    txtnom=$("#txtnom").val();
    cboveh=$("#cboveh").val();
    txtcos=$("#txtcos").val(); //int
  cbonum=$("#cbonum").val(); //int
    txtobs=$("#txtobs").val();
    cbofor=$("#cbofor").val(); //int
    txtfec=$("#txtfec").val();
  
    if(txtrut != '' && txtnom != '' && txtcos != '' && txtobs != '' && txtfec != ''){ //ver con los cbo
        if(!isNaN(txtcos)){
            $.post('intermediario.php', {btnenv:btnenv, txtrut:txtrut, txtnom:txtnom, cboveh:cboveh, txtcos:txtcos, cbonum:cbonum, txtobs:txtobs, cbofor:cbofor, txtfec:txtfec},
            function(data){
               $("#mensaje").html(data);
               $("#mensaje").fadeIn(500);
            });
            $("#txtrut").attr("value","");
            $("#txtnom").attr("value","");
            $("#cboveh").attr("value","");
      $("#txtcos").attr("value","");
            $("#cbonum").attr("value","");
            $("#txtobs").attr("value","");
      $("#cbofor").attr("value","");
            $("#txtfec").attr("value","");
        }else{
            $("#mensaje").html('El precio y Stock debe ser Numericos!');
            $("#mensaje").fadeIn(500);
        }
    }else{
        $("#mensaje").html('Debe llenar todos los Campos!');
        $("#mensaje").fadeIn(500);
    }
}




function buscar(){
  var btnbus,txtrut2;
    btnbus=$("#btnbus").val();
    txtrut2=$("#txtrut2").val();
  //$("#txtrut3").val(txtrut2); //pasar variable de un textbox a otro
  $("#excel").hide();
    if(txtrut2 != ''){ //ver con los cbo
         $.post('intermediario.php', {btnbus:btnbus, txtrut2:txtrut2},
            function(data){
                 $("#tably").html(data);
            });
    }else{
        $("#mensaje").html('Debe llenar todos los Campos!');
        $("#mensaje").fadeIn(500);
    }
}



//lleva a intermediario y luego a la funcion eliminar
function borrarelemento(cod){
    $.get('intermediario.php', {cod:cod},
    function(data){
        $("#mensaje").html(data);
        $("#mensaje").fadeIn(500);
    });
}

function mostrarform(codmod){
    $.get('intermediario.php', {codmod:codmod},
    function(data){
    $("#form1").hide(); //paq salga el msj oculto al inicio
        $("#mensaje2").html(data);
        $("#mensaje2").fadeIn(500);
    });
}


function quitarmensaje(){
    $("#mensaje").fadeOut("slow");
    llenartabla();
}

function ocultarform(){
    //$("#form1").fadeOut("slow");
   $("#form1").hide;
    llenartabla();
}
