/*Funcion de cargar*/
$(document).ready(function(){
    $(".button-collapse").sideNav(); //Menu del Header

    $('ul.tabs').tabs(); //Menu

    $('.parallax').parallax(); //Efecto Parallax

    $('.scrollspy').scrollSpy(); //Transicion a los elementos de forma fluida

    $('.modal-trigger').leanModal({ //Ventanas Modales (Las que aparecen derrepente :v)
          dismissible: true, // Afecto
          opacity: .7, // Opacidad de fondo
          in_duration: 300, // Duracion de la transicion al abrir
          out_duration: 250, // Duracion de la transicion al cerrar
        }
    );    

    Materialize.updateTextFields(); //Habilitar TextFields

    $('select').material_select(); //Habilitar los Select

    $('input#input_text, textarea#textarea1').characterCounter(); //Habilitar que Pueda Contar los Caracteres

    $('.datepicker').pickadate({ //Calendario
                selectMonths: true, // Habilitar la Seleccion de Meses
                selectYears: 15, // Numero de Años Posibles
                firstDay: true //Que el calendario empieze en lunes
            });

    $('.tooltipped').tooltip({delay: 50});//Mensajito en hover del boton

    $('.materialboxed').materialbox();//Efecto zoom de imagenes

    $('.NavLateral-DropDown').on('click', function(e){
        e.preventDefault();
        var DropMenu=$(this).next('ul');
        var CaretDown=$(this).children('i.NavLateral-CaretDown');
        DropMenu.slideToggle('fast');
        if(CaretDown.hasClass('NavLateral-CaretDownRotate')){
            CaretDown.removeClass('NavLateral-CaretDownRotate');    
        }else{
            CaretDown.addClass('NavLateral-CaretDownRotate');    
        }
         
    });
    
    $('.ShowHideMenu').on('click', function(){
        var MobileMenu=$('.NavLateral');
        if(MobileMenu.css('opacity')==="0"){
            MobileMenu.addClass('Show-menu');   
        }else{
            MobileMenu.removeClass('Show-menu'); 
        }   
    });

    $('.btn-ExitSystem').on('click', function(e){
        e.preventDefault();
        swal({ 
            title: "Do you want to get out?",   
            text: "Your session will be closed",
            type: "warning",   
            showCancelButton: true,   
            confirmButtonColor: "#DD6B55",   
            confirmButtonText: "Yes, sure",
            animation: "slide-from-top",   
            closeOnConfirm: false,
            cancelButtonText: "Cancel"
        }, function(){
            setTimeout(function(){ window.location='/'; }, 200);
        });
    });

});

/*Funcion de scroll*/
(function($){
    $(window).load(function(){
        $(".NavLateral-content").mCustomScrollbar({
            theme:"light-thin",
            scrollbarPosition: "inside",
            autoHideScrollbar: true,
            scrollButtons:{ enable: true }
        });
        $(".ContentPage, .NotificationArea").mCustomScrollbar({
            theme:"dark-thin",
            scrollbarPosition: "inside",
            autoHideScrollbar: true,
            scrollButtons:{ enable: true }
        });
    });
})(jQuery);