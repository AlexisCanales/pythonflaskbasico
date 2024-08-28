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



function ocultarform(){
    //$("#form1").fadeOut("slow");
   $("#form1").hide;
    llenartabla();
}
