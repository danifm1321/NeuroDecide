var index = 0;
var arrayLetras = ['s', 'r', 'n', 'd', 'l', 'c', 't', 'm'];
var arraySoluciones = [];
var arrayTiemposSoluciones = [];
var experimentoEmpezado = false;
var tiempoRespuestaAlto = 0
var tiemposRespuesta = 0
var necesitaParar = false
var cntP = 0;
var cntQ = 0;
var letrasAleatorias;
var comienzaExperimento;

var idUsuario;
var trialCnt;
var respuestaCnt;
var tInicio;
var tApareceLetra;
var tPulsacion;
var eleccion;
var tiempoAparicionLetraElegida;
var letraElegida;


$(document).ready(function ()
{    
    $("#modal-consentimiento").show()

    $(document).keypress(function(event){
        if(event.which == 32 && !experimentoEmpezado && $('#wrapper-4-imagenes').hasClass('d-none'))            //Pulsa la tecla espacio para comenzar el experimento
        {
            event.preventDefault();

            calibracion();
            setTimeout(finalizarExperimento, 120000);

        }
        else if(event.which == 113 && experimentoEmpezado && $('#wrapper-4-imagenes').hasClass('d-none'))       //Pulsa la tecla Q
        {
            cntQ++;
            eleccion = "q"
            tPulsacion = new Date()

            muestraSoluciones();

        }
        else if(event.which == 112 && experimentoEmpezado && $('#wrapper-4-imagenes').hasClass('d-none'))       //Pulsa la tecla P
        {
            cntP++;
            eleccion = "p"
            tPulsacion = new Date()

            muestraSoluciones();
        } else if(!$('#wrapper-4-imagenes').hasClass('d-none'))
        {
            if(event.which == 51)                                                       //Pulsa la tecla 3 asociada a #
                registraTiempoAparicionLetraElegida(3, '#');
            else
            {
                var indiceLetra = arraySoluciones.indexOf(String.fromCharCode(event.which));
                if(indiceLetra != -1)
                    registraTiempoAparicionLetraElegida(indiceLetra, String.fromCharCode(event.which));
                
            }
        }
    });

    $( "#btn-comenzar-experimento" ).click(function() {
            calibracion();
            setTimeout(finalizarExperimento, 120000); 
      });

    $('.enlace-imagen').on('click', function(e) {
        e.preventDefault();
    });

    $('.imagen-conjunto').click(function() {
        let letraAux = $(this).attr('src').split("images/letra-")[1].split(".png")[0]

        if(letraAux == "cardinal") {
            registraTiempoAparicionLetraElegida(3, '#')
        } else {
            let tiempoRes = arraySoluciones.indexOf(letraAux)
            registraTiempoAparicionLetraElegida(tiempoRes, letraAux)
        }
    })


    $("#form-usuario").submit(function(e) {
        e.preventDefault();
        iniciaUsuario();
    });
})

function calibracion()
{
    $("#checkbox-prueba").prop("disabled", true)
    necesitaParar = false;

    aniadirSesion()
    respuestaCnt = -1;

    tInicio = new Date()

    $("#btn-comenzar-experimento").addClass("d-none");
    $("#blank-image").removeClass("d-none");

    letrasAleatorias = setInterval(changeImage, 500);
    comienzaExperimento = setTimeout(comenzarExperimento, 5000);
}

function comenzarExperimento()
{
    experimentoEmpezado = true;

    respuestaCnt++;

    tApareceLetra = new Date()

    $("#btn-comenzar-experimento").addClass("d-none");

    $("#blank-image").addClass("d-none");

    $("#letra-experimento").removeClass("d-none");

}


function changeImage()
{
    if($('#wrapper-4-imagenes').hasClass('d-none'))
    {
        if(index == arrayLetras.length)
        {
            var ultimaLetra = arrayLetras[arrayLetras.length-1];
            var penultimaLetra = arrayLetras[arrayLetras.length-2];
            var antePenultimaLetra = arrayLetras[arrayLetras.length-3];
            shuffle(arrayLetras);
            var primerosElementos = arrayLetras.slice(0, 3);

            //Mezclamos el array hasta que sus 3 primeros elementos sean distintos a los 3 últimos del anterior array
            //Esto se hace para que no aparezcan en la vista de las 4 letras 2 letras que sean iguales
            while(primerosElementos.includes(ultimaLetra) || primerosElementos.includes(penultimaLetra) || primerosElementos.includes(antePenultimaLetra))
            {
                shuffle(arrayLetras);
                primerosElementos = arrayLetras.slice(0, 3);
            }
            
            index = 0;
        }

        $("#letra-experimento").attr("src", "images/letra-" + arrayLetras[index] + ".png");

        arraySoluciones.unshift(arrayLetras[index])
        arrayTiemposSoluciones.unshift(new Date())
        if(arraySoluciones.length > 3) {
            arraySoluciones.pop();
            arrayTiemposSoluciones.pop();
        }

        index++;
    }
}

function shuffle(array)
{
    array.sort(function() { return 0.5 - Math.random() });
}

function muestraSoluciones()
{
    clearInterval(letrasAleatorias)

    $("#letra-experimento").addClass("d-none");
    $("#wrapper-4-imagenes").removeClass("d-none");

    let arrayShuffle = []

    $.each(arraySoluciones, function(i, val) {
        arrayShuffle.push(val)
    });

    arrayShuffle.push("cardinal")
    shuffle(arrayShuffle)

    $("#conjunto-letra-1").attr("src", "images/letra-" + arrayShuffle[0] + ".png");
    $("#conjunto-letra-2").attr("src", "images/letra-" + arrayShuffle[1] + ".png");
    $("#conjunto-letra-3").attr("src", "images/letra-" + arrayShuffle[2] + ".png");
    $("#conjunto-letra-4").attr("src", "images/letra-" + arrayShuffle[3] + ".png");
}

function resetExperimento()
{
    tInicio = new Date()

    experimentoEmpezado = false

    $("#wrapper-4-imagenes").addClass("d-none");
    $("#blank-image").removeClass("d-none");

    
    comienzaExperimento = setTimeout(comenzarExperimento, 2000);
    letrasAleatorias = setInterval(changeImage, 500);
}

function registraTiempoAparicionLetraElegida(indiceLetra, letra)
{
    if(indiceLetra != 3) 
        tiempoAparicionLetraElegida = arrayTiemposSoluciones[indiceLetra];
    else {
        tiempoAparicionLetraElegida = new Date(tPulsacion)
        tiempoAparicionLetraElegida.setMilliseconds(tiempoAparicionLetraElegida.getMilliseconds() - 1750);
    }
 
    letraElegida = letra

    if(indiceLetra == 3)
        tiempoRespuestaAlto++;

    tiemposRespuesta++;

    ajaxEleccion()   

    if(!necesitaParar)
        resetExperimento();
    else
    {
        $("#wrapper-4-imagenes").addClass("d-none");
        finalizarExperimento();
    }
}

function finalizarExperimento()
{
    necesitaParar = true;

    if($('#wrapper-4-imagenes').hasClass('d-none'))
    {
        experimentoEmpezado = false;
        $("#wrapper-4-imagenes").addClass("d-none");
        $("#letra-experimento").addClass("d-none");
        clearInterval(letrasAleatorias)
        clearInterval(comienzaExperimento)

        $("#blank-image").addClass("d-none");
        $("#btn-comenzar-experimento").removeClass("d-none");
        $("#checkbox-prueba").prop("disabled", false)
    }
}

function ajaxEleccion()
{
    if(!$("#checkbox-prueba").is(':checked')) {
        $.ajax({
            type : "POST",
            url : "grabarCSV",
            data : '{"id" : ' + idUsuario + ','
                + '"trial": ' + trialCnt + ',' 
                + '"respuesta": ' + respuestaCnt + ','
                + '"tInicio": "' + tInicio.getFullYear().toString() + "-" + parseInt(parseInt(tInicio.getMonth())+1) + "-" + tInicio.getDate() + " " + tInicio.getHours() + ":" + tInicio.getMinutes() + ":" + tInicio.getSeconds() + "." + tInicio.getMilliseconds() + '",'
                + '"tApareceLetra": "' + tApareceLetra.getFullYear().toString() + "-" + parseInt(parseInt(tApareceLetra.getMonth())+1) + "-" + tApareceLetra.getDate() + " " + tApareceLetra.getHours() + ":" + tApareceLetra.getMinutes() + ":" + tApareceLetra.getSeconds() + "." + tApareceLetra.getMilliseconds() + '",'
                + '"tPulsacion": "' + tPulsacion.getFullYear().toString() + "-" + parseInt(parseInt(tPulsacion.getMonth())+1) + "-" + tPulsacion.getDate() + " " + tPulsacion.getHours() + ":" + tPulsacion.getMinutes() + ":" + tPulsacion.getSeconds() + "." + tPulsacion.getMilliseconds() + '",'
                + '"eleccion": "' + eleccion + '",'
                + '"tAparicionLetraElegida": "' + tiempoAparicionLetraElegida.getFullYear().toString() + "-" + parseInt(parseInt(tiempoAparicionLetraElegida.getMonth())+1) + "-" + tiempoAparicionLetraElegida.getDate() + " " + tiempoAparicionLetraElegida.getHours() + ":" + tiempoAparicionLetraElegida.getMinutes() + ":" + tiempoAparicionLetraElegida.getSeconds() + "." + tiempoAparicionLetraElegida.getMilliseconds() + '",'
                + '"letraElegida": "' + letraElegida + '"'
                +'}',
            contentType: 'application/json;charset=UTF-8', 
        }).done(function (data){
            if(data.codigo == 200)
            {
                console.log("Datos enviados con exito")
            }
        });
    }
}

function validarExperimento()
{
    $("#experimento-valido").addClass("d-none")
    $("#tiempo-de-respuesta-alto").addClass("d-none")
    $("#predileccion").addClass("d-none")

    var valido = true

    if (tiemposRespuesta > 0 && tiempoRespuestaAlto/tiemposRespuesta >= 0.1)
    {
        $("#tiempo-de-respuesta-alto").removeClass("d-none")
        valido = false
    }
    if((cntQ+cntP != 0) && ((cntQ-cntP)/(cntQ+cntP) > 0.3))
    {
        $("#predileccion").removeClass("d-none")
        valido = false
    }
    if(valido){
        $("#experimento-valido").removeClass("d-none")
    }
}

function iniciaUsuario()
{
    if($("#input-correo").val() != "" && $('input[name=genero-usuario]:checked', '#form-usuario').val() != undefined)
    {
        $("#form-usuario").prop("disabled", true)        
        $("#correo-introducido").removeClass("d-none")
        identificarUsuario()

    }
}

function marcarConsentimiento(){
    if($("#checkbox-consentimiento").is(':checked'))
        $("#dar-consentimiento").prop("disabled", false)
    else 
        $("#dar-consentimiento").prop("disabled", true)
}

function identificarUsuario() {

    $.ajax({
        type : "POST",
        url : "registrarUsuario",
        data : '{"emailUsuario": "' + $("#input-correo").val() + '", ' +
        '"generoUsuario": "' + $('input[name=genero-usuario]:checked', '#form-usuario').val() + '"}',
        contentType: 'application/json;charset=UTF-8', 
      }).done (function (data) {
        idUsuario = data.userId;
    });
}

function aniadirSesion() {
    if(!$("#checkbox-prueba").is(':checked')) {
        $.ajax({
            type : "PUT",
            url : "aniadirSesion/" + idUsuario,
            contentType: 'application/json;charset=UTF-8', 
          }).done (function(data) {
            trialCnt = data.session;
            $("#numero-trial").removeClass("d-none");
            $("#numero-trial h4").text("Trial nº " + (trialCnt + 1));
          });
    } 
}
