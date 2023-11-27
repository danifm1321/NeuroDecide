var timeStamps = [];
var timeStampsFiltered = [];
var timeStampsLocalP = [];
var timeStampsLocalQ = [];

var timeStampsLocalFilteredP = [];
var timeStampsLocalFilteredQ = [];
//var timeStampsLocalAparicionLetra = [];

var timeStampsPulsaciones = [];
var timeStampsPulsacionesFiltered = [];

var timeStampsPulsacionesP = [];
var timeStampsPulsacionesQ = [];

var timeStampsComienzos = [];
var timeStampsComienzosFiltered = [];

var museData = {"raw" : {}, "delta" : {}, "theta" : {}, "gamma" : {}, "alpha" : {}, "beta" : {}}
var coloresTipoDeSensor = {"TP9" : "#6D78AD", "AF7" : "#52CDA0", "AF8" : "#DF7970", "TP10" : "#4C9C9F"}
var chartsLineas = {"raw" : null, "delta" : null, "theta" : null, "gamma" :null, "alpha" : null, "beta" : null};
var chartsCajas = {"raw" : null, "delta" : null, "theta" : null, "gamma" :null, "alpha" : null, "beta" : null};
var chartsCajasParticipantes = {"raw" : null, "delta" : null, "theta" : null, "gamma" :null, "alpha" : null, "beta" : null};
var chartsCajasSensores = {"raw" : null, "delta" : null, "theta" : null, "gamma" :null, "alpha" : null, "beta" : null};

var dataJsonParticipantes = {}
var dataJsonSensores = {}

const TIPOS_GRAFICOS = {
  LINEAS: "lineas",
  CAJAS: "cajas",
  CAJAS_PARTICIPANTES: "cajas_participantes",
  CAJAS_SENSORES: "cajas_sensores"
}

$(document).ready(function ()
{
  ajaxGetUsuarios();

  $("#select-participantes").change( function() {
    var data = $(this).val().toString();

    ajaxGetSesiones(+data);
    noData(TIPOS_GRAFICOS.LINEAS)
    noData(TIPOS_GRAFICOS.CAJAS)
  });
  
  $("#select-sesiones").change( function() {
    noData(TIPOS_GRAFICOS.LINEAS)
    noData(TIPOS_GRAFICOS.CAJAS)
    ajaxGetData();
  });

  $.each(museData, function(i, tipoDeOnda) {
    museData[i] = {"TP9":[],"AF7":[],"AF8":[],"TP10":[]}
  });

  $("#normalizar-checkbox-lines").change(function() {
    showLoading(TIPOS_GRAFICOS.LINEAS);

    setTimeout(function() {
      updateDataLineas();
      hideLoading(TIPOS_GRAFICOS.LINEAS);
    }, 1);

  });

  $("#normalizar-checkbox-boxes").change(function() {
    showLoading(TIPOS_GRAFICOS.CAJAS);

    setTimeout(function() {
      updateDataCajas();
      hideLoading(TIPOS_GRAFICOS.CAJAS);
    }, 1);
  });

  $("#normalizar-checkbox-boxes-participants").change(function() {
    ajaxGetDataCajasParticipantes();
  });

  $("#normalizar-checkbox-boxes-sensors").change(function() {
    ajaxGetDataCajasSensores();
  });

  $("#pre-decision-checkbox-boxes").change(function() {
    updateDataCajas();
  });

  $("#pre-decision-checkbox-boxes-participants").change(function() {
    updateDataCajasParticipantes();
  });

  $("#pre-decision-checkbox-boxes-sensors").change(function() {
    updateDataCajasSensores();
  });

  $("#post-decision-checkbox-boxes").change(function() {
    updateDataCajas();
  });

  $("#post-decision-checkbox-boxes-participants").change(function() {
    updateDataCajasParticipantes();
  });

  $("#post-decision-checkbox-boxes-sensors").change(function() {
    updateDataCajasSensores();
  });
  
  $("#select-intervalo").change(function () {
    showLoading(TIPOS_GRAFICOS.LINEAS);
    
    setTimeout(function() {
      updateDataLineas();
      hideLoading(TIPOS_GRAFICOS.LINEAS);
    }, 1);
  });

  $("#select-pre-decision").change(function () {
    showLoading(TIPOS_GRAFICOS.CAJAS);
  
    setTimeout(function() {
      updateDataCajas();
      hideLoading(TIPOS_GRAFICOS.CAJAS);
    }, 1);
  });

  $("#select-pre-decision-sensores").change(function () {
    ajaxGetDataCajasSensores();
  });

  $("#select-pre-decision-participantes").change(function () {
    ajaxGetDataCajasParticipantes();
  });

  $("#solo-aparicion-checkbox").change(function () {
    showLoading(TIPOS_GRAFICOS.LINEAS);

    setTimeout(function() {
      updateDataLineas();
      hideLoading(TIPOS_GRAFICOS.LINEAS);
    }, 1);
  });

  //MOSTRAR GRÁFICOS DE LÍNEAS
  $("#ver-lineas").click(function() {

    $(".boton-ver-graficas").removeClass("active");
    $("#ver-lineas").addClass("active");

    $(".boxes-related").addClass("d-none")
    $(".boxes-participants-related").addClass("d-none")
    $(".boxes-sensors-related").addClass("d-none")
    $(".lines-related").removeClass("d-none")

    $.each(chartsLineas, function(i, chart) {
      if(chart != null) {
        chart.render();
      }
    });
  })

  //MOSTRAR GRÁFICOS DE CAJA
  $("#ver-cajas").click(function() {

    $(".boton-ver-graficas").removeClass("active");
    $("#ver-cajas").addClass("active");

    $(".boxes-participants-related").addClass("d-none")
    $(".boxes-sensors-related").addClass("d-none")
    $(".lines-related").addClass("d-none")
    $(".boxes-related").removeClass("d-none")

    $.each(chartsCajas, function(i, chart) {
      if(chart != null) {
        chart.render();
      }
    });
  })
  
  $("#ver-cajas-participantes").click(function() {
    $(".boton-ver-graficas").removeClass("active");
    $("#ver-cajas-participantes").addClass("active");

    $(".boxes-sensors-related").addClass("d-none")
    $(".lines-related").addClass("d-none")
    $(".boxes-related").addClass("d-none")
    $(".boxes-participants-related").removeClass("d-none")

    $.each(chartsCajasParticipantes, function(i, chart) {
      if(chart != null) {
        chart.render();
      }
    });
  });

  $("#ver-cajas-sensores").click(function() {
    $(".boton-ver-graficas").removeClass("active");
    $("#ver-cajas-sensores").addClass("active");

    $(".lines-related").addClass("d-none")
    $(".boxes-related").addClass("d-none")
    $(".boxes-participants-related").addClass("d-none")
    $(".boxes-sensors-related").removeClass("d-none")

    $.each(chartsCajasSensores, function(i, chart) {
      if(chart != null) {
        chart.render();
      }
    });
  });

});


function ajaxGetUsuarios() {

  $.ajax({
    type : "GET",
    url : "getUsuarios",
    context:this,
    contentType: 'application/json;charset=UTF-8', 
  }).done(function (data){

    $('#select-participantes option').remove();
    
    $.each(JSON.parse(data), function (i, item) {
      $('#select-participantes').append($('<option>', { 
            value: item,
            text : "Participante " + (item+1)
        }));
    });
    
    $('#select-participantes').selectpicker('refresh');

    $('#select-participantes-cajas option').remove();
    
    $.each(JSON.parse(data), function (i, item) {
      $('#select-participantes-cajas').append($('<option>', { 
            value: item,
            text : "Participante " + (item+1)
        }));
    });
    
    var newActionParticipantes = $('<button type="button" id="boton-enviar-participantes" onclick="ajaxGetDataCajasParticipantes()" class="btn btn-light btn-enviar-datos">Enviar</button>');
    var newActionSensores = $('<button type="button" id="boton-enviar-sensores" onclick="ajaxGetDataCajasSensores()" class="btn btn-light btn-enviar-datos">Enviar</button>');

    $('#select-participantes-cajas').siblings('.dropdown-menu').append(newActionParticipantes);
    $('#select-sensores-cajas').siblings('.dropdown-menu').append(newActionSensores);

    $('#select-participantes-cajas').selectpicker('refresh');
    $('#select-sensores-cajas').selectpicker('refresh');
  });
}

function ajaxGetSesiones(data) {

  $.ajax({
    type : "GET",
    url : "getSesiones/" + data,
    context:this,
    contentType: 'application/json;charset=UTF-8',
  })
  .done(function (data){

    $('#select-sesiones option').remove();

    $.each(JSON.parse(data), function (i, item) {
      $('#select-sesiones').append($('<option>', { 
            value: item,
            text : "Sesión " + (item+1)
        }));
    });

    $('#select-sesiones').selectpicker('refresh');
  });  
}

function ajaxGetData() {
  $.ajax({
    type : "GET",
    url : "getData/" + $("#select-participantes").val() + "/" + $("#select-sesiones").val(),
    contentType: 'application/json;charset=UTF-8',
    beforeSend: function() {
      showLoading(TIPOS_GRAFICOS.LINEAS)
      showLoading(TIPOS_GRAFICOS.CAJAS)
    },
    complete: function() {
      hideLoading(TIPOS_GRAFICOS.LINEAS)
      hideLoading(TIPOS_GRAFICOS.CAJAS)
    }
  }).done(function (data){
      setDataFromJSON(data)
  });  
}

function ajaxGetDataCajasParticipantes() {

  if($("#select-participantes-cajas").val().length != 0) {
    $.ajax({
      type : "POST",
      url : "getDataCajasParticipantes",
      data : '{"participantes" : ' + JSON.stringify($("#select-participantes-cajas").val()) + ', '
      + '"milisegundos" : "' + $("#select-pre-decision-participantes").val() +'", '
      + '"normalizar" : "' + $("#normalizar-checkbox-boxes-participants").is(':checked') + '"}',
      contentType: 'application/json;charset=UTF-8',
      beforeSend: function() {
        showLoading(TIPOS_GRAFICOS.CAJAS_PARTICIPANTES)
      },
      complete: function() {
        hideLoading(TIPOS_GRAFICOS.CAJAS_PARTICIPANTES)
      }
    }).done(function(data) {


      if(JSON.parse(data)["Error"] != undefined)
      {
      } else {

        const dataJsonParticipantesDesordenado = JSON.parse(data)

        const orden = [
          "Pre-decisión de AF7 para p",
          "Pre-decisión de AF7 para q",
          "Post-decisión de AF7 para p",
          "Post-decisión de AF7 para q",
          "Pre-decisión de AF8 para p",
          "Pre-decisión de AF8 para q",
          "Post-decisión de AF8 para p",
          "Post-decisión de AF8 para q",
          "Pre-decisión de TP9 para p",
          "Pre-decisión de TP9 para q",
          "Post-decisión de TP9 para p",
          "Post-decisión de TP9 para q",
          "Pre-decisión de TP10 para p",
          "Pre-decisión de TP10 para q",
          "Post-decisión de TP10 para p",
          "Post-decisión de TP10 para q",
        ];
  
        dataJsonParticipantes = {}
  
        $.each(dataJsonParticipantesDesordenado, function(participante){
          dataJsonParticipantes[participante] = {}
          
          $.each(dataJsonParticipantesDesordenado[participante], function(tipoDeOnda){
            dataJsonParticipantes[participante][tipoDeOnda] = {}
  
            orden.forEach((clave) => {
              dataJsonParticipantes[participante][tipoDeOnda][clave] = dataJsonParticipantesDesordenado[participante][tipoDeOnda][clave]
            });
          });
        });
  
        updateDataCajasParticipantes();
      }
    });
  }
}


function ajaxGetDataCajasSensores() {

  if($("#select-pre-decision-sensores").val().length != 0)
   {
    $.ajax({
      type : "POST",
      url : "getDataCajasSensores",
      data : '{"sensores" : ' + JSON.stringify($("#select-sensores-cajas").val()) + ', '
      + '"milisegundos" : "' + $("#select-pre-decision-sensores").val() +'", '
      + '"normalizar" : "' + $("#normalizar-checkbox-boxes-sensors").is(':checked') + '"}',
      contentType: 'application/json;charset=UTF-8', 
      beforeSend: function() {
        showLoading(TIPOS_GRAFICOS.CAJAS_SENSORES)
      },
      complete: function() {
        hideLoading(TIPOS_GRAFICOS.CAJAS_SENSORES)
      }
    }).done(function(data) {

      if(JSON.parse(data)["Error"] != undefined)
      {
        console.log("error")
      } else {
        const dataJsonSensoresDesordenado = JSON.parse(data)

        const orden = [
          "Pre-decisión para p",
          "Pre-decisión para q",
          "Post-decisión para p",
          "Post-decisión para q",
        ];
  
        dataJsonSensores = {}
  
        $.each(dataJsonSensoresDesordenado, function(sensor){
          dataJsonSensores[sensor] = {}
          
          $.each(dataJsonSensoresDesordenado[sensor], function(tipoDeOnda){
            dataJsonSensores[sensor][tipoDeOnda] = {}
  
            orden.forEach((clave) => {
              dataJsonSensores[sensor][tipoDeOnda][clave] = dataJsonSensoresDesordenado[sensor][tipoDeOnda][clave]
            });
          });
        });
  
        updateDataCajasSensores();
      }


    });
  }

}

function setDataFromJSON(data) {
  var parsedData = JSON.parse(data)

  timeStamps = [];
  timeStampsLocalP = [];
  timeStampsLocalQ = [];
  timeStampsComienzos = [];


  $.each(parsedData[0], function(i, parsedLocalData){
    $.each(parsedLocalData, function(j, val) {

      if(j == "eleccion")
      {
        if(val == "p") {
          timeStampsLocalP.push(parsedLocalData["tiempoAparicion"]);
        } else {
          timeStampsLocalQ.push(parsedLocalData["tiempoAparicion"]);
        }
        //timeStampsLocalAparicionLetra.push(parsedLocalData["tiempoAparicion"]);
      } else if(j == "tiempoPulsacion") {
        timeStampsPulsaciones.push(val);

        if(parsedLocalData["eleccion"] == "p")
          timeStampsPulsacionesP.push(val)
        else
          timeStampsPulsacionesQ.push(val)

      }
      else if(j == "tiempoComienzo") {
        timeStampsComienzos.push(val);
      }
    });
  });

  $.each(parsedData[1], function(i, parsedMuseData) {      
    $.each(parsedMuseData, function(j, val) {
      if(j == "timeStamp")
        timeStamps.push(val)
      else {
        var splittedIndex = j.split(/(?=[A-Z])(.*)/);

        if(parseFloat(val)) {
          museData[splittedIndex[0]][splittedIndex[1]].push(parseFloat(val))
        } else {
          museData[splittedIndex[0]][splittedIndex[1]].push(null)
        }
      }
    })
  });

  updateDataLineas();
  updateDataCajas();
}

function updateDataLineas(){

  timeStampsLocalFilteredP = [];
  timeStampsLocalFilteredQ = [];
  timeStampsPulsacionesFiltered = [];
  timeStampsComienzosFiltered = [];

  timeStampsFiltered = [];
  
  if(timeStamps.length != 0) {
    let indice = 0;
    let incremento = parseInt($("#select-intervalo").val());

    let indexComienzoFin = 0;

    let closestComienzo = getClosestTime(new Date(timeStampsComienzos[indexComienzoFin]));
    let closestFinal = getClosestTime(new Date(timeStampsPulsaciones[indexComienzoFin]));

    while (indice < timeStamps.length-1){

      //timeStampsFiltered.push(indice)
      
      if(!$("#solo-aparicion-checkbox").is(':checked')) {
        timeStampsFiltered.push(indice)
      } else {
        //Si estamos en el final y no hay una pulsacion final o si el tiempo entra dentro de las apariciones de letras
        if((indexComienzoFin == timeStampsComienzos.length-1 && timeStampsPulsaciones.length < timeStampsComienzos.length) || (indice > closestComienzo && indice < closestFinal)) 
          timeStampsFiltered.push(indice)
        //Si no estamos en el indice final y es mayor que el ultimo final pero no mayor que el proximo comienzo, aumentamos el indice
        else if(indexComienzoFin < timeStampsComienzos.length-1 && indice > closestFinal)
        {
          indexComienzoFin++;
          closestComienzo = getClosestTime(new Date(timeStampsComienzos[indexComienzoFin]));
          closestFinal = getClosestTime(new Date(timeStampsPulsaciones[indexComienzoFin]));
        }
      }

      if(incremento == 0)
      {
        indice++;
      } else {

        let time = new Date(timeStamps[indice]);
        let timeInMilliseconds = time.getTime();
        timeInMilliseconds += incremento;
        time = new Date(timeInMilliseconds)
        
        indice = getClosestTime(time)
      }
    }
  }

  if (timeStampsLocalP.length != 0) {
    $.each(timeStampsLocalP, function(i, tiempo) {
      let fecha = new Date(tiempo)
      timeStampsLocalFilteredP.push(getClosestTimeLocal(fecha));
    });
  }

  if (timeStampsLocalQ.length != 0) {
    $.each(timeStampsLocalQ, function(i, tiempo) {
      let fecha = new Date(tiempo)
      timeStampsLocalFilteredQ.push(getClosestTimeLocal(fecha));
    });
  }

  if (timeStampsPulsaciones.length != 0) {
    $.each(timeStampsPulsaciones, function(i, tiempo) {
      let fecha = new Date(tiempo)
      timeStampsPulsacionesFiltered.push(getClosestTimeLocal(fecha));
    });
  }

  if(timeStampsComienzos.length != 0) {
    $.each(timeStampsComienzos, function(i, tiempo) {
      let fecha = new Date(tiempo)
      timeStampsComienzosFiltered.push(getClosestTimeLocal(fecha));
    });
  }

  if (timeStampsFiltered.length != 0)
  {

    var firstTime = new Date(timeStamps[0])

    $.each(museData, function(i, tipoDeOnda) {
      var data = [];

      var max = getMax(tipoDeOnda['TP9'])
      var min = getMin(tipoDeOnda['TP9'])

      $.each(tipoDeOnda, function(j, array) {

        var newMax = getMax(array)
        var newMin = getMin(array)

        if (max < newMax)
          max = newMax;
        
        if(min > newMin)
          min = newMin;
      });
      

      $.each(tipoDeOnda, function(j, array) {

        let dataPoints = []

        $.each(timeStampsFiltered, function(k, index) {
          
          let value = array[index]

          if($("#normalizar-checkbox-lines").is(':checked'))
            value = normalize(value, max, min);

          let myTime = new Date(timeStamps[index]);
    
          dataPoints.push({
            x: (myTime.getTime() - firstTime.getTime()),
            y: value
          });
          
        });

        data.push(    
          {        
          type: "line",
          showInLegend: true,
          connectNullData: true,
          name: j,
          dataPoints: dataPoints
        })
      });

      let dataPoints = []

      if($("#normalizar-checkbox-lines").is(':checked'))
      {
        min = -1;
        max = 1;
      }

      if(!$("#solo-aparicion-checkbox").is(':checked')) {
        $.each(timeStampsComienzosFiltered, function(k, value) {

          let myTime = new Date(timeStamps[value]);
  
          dataPoints.push({
            x: (myTime.getTime() - firstTime.getTime()),
            y: (min+max)/2,
            markerType: "circle",
            markerColor: "#F0D81A",
            markerSize: 10
          })
        });
  
        data.push(    
          {        
          type: "line",
          color: "#00F0D81A",
          legendMarkerColor: "#F0D81A",
          showInLegend: true,
          connectNullData: true,
          name: "Aparición de letras",
          dataPoints: dataPoints
        })
  
        dataPoints = [];
      }


      $.each(timeStampsPulsacionesFiltered, function(k, value) {

        let myTime = new Date(timeStamps[value]);

        dataPoints.push({
          x: (myTime.getTime() - firstTime.getTime()),
          y: (min+max)/2,
          markerType: "circle",
          markerColor: "#000000",
          markerSize: 10
        })
      });

      data.push(    
        {        
        type: "line",
        color: "#00000000",
        legendMarkerColor: "#000000",
        showInLegend: true,
        connectNullData: true,
        name: "Pulsaciones",
        dataPoints: dataPoints
      })

      dataPoints = [];

      $.each(timeStampsLocalFilteredP, function(k, value) {

        let myTime = new Date(timeStamps[value]);


        dataPoints.push({
          x: (myTime.getTime() - firstTime.getTime()),
          y: (min+max)/2,
          markerType: "circle",
          markerColor: "#9A0000",
          markerSize: 10
        })
      });

      data.push(    
        {        
        type: "line",
        color: "#009A0000",
        legendMarkerColor: "#9A0000",
        showInLegend: true,
        connectNullData: true,
        name: "Impulsos de P",
        dataPoints: dataPoints
      })

      dataPoints = [];
      
      $.each(timeStampsLocalFilteredQ, function(k, value) {
        let myTime = new Date(timeStamps[value]);

        dataPoints.push({
          x: (myTime.getTime() - firstTime.getTime()),
          y: (min+max)/2,
          markerType: "circle",
          markerColor: "#0003C1",
          markerSize: 10
        })
      });

      data.push(    
        {        
        type: "line",
        color: "#0003C100",
        legendMarkerColor: "#0003C1",
        showInLegend: true,
        connectNullData: true,
        name: "Impulsos de Q",
        dataPoints: dataPoints
      })

      chartsLineas[i] = createChartLineas(i + '-line-chart', data);

    });
  }  
}

function updateDataCajas() {

  timeStampsFiltered = [];
  timeStampsLocalFilteredP = [];
  timeStampsLocalFilteredQ = [];

  if(timeStamps.length != 0) {
    let indice = 0;
    
    while (indice < timeStamps.length-1){
      timeStampsFiltered.push(indice)
      indice++;
    }
  }

  if (timeStampsLocalP.length != 0) {
    $.each(timeStampsLocalP, function(i, tiempo) {
      let fecha = new Date(tiempo)
      timeStampsLocalFilteredP.push(getClosestTimeLocal(fecha));
    });
  }

  if (timeStampsLocalQ.length != 0) {
    $.each(timeStampsLocalQ, function(i, tiempo) {
      let fecha = new Date(tiempo)
      timeStampsLocalFilteredQ.push(getClosestTimeLocal(fecha));
    });
  }

  let tiemposPredecisionP = [];
  let tiemposPredecisionQ = [];

  let tiemposAparicionP = [];
  let tiemposAparicionQ = [];

  let tiemposPostdecisionP = [];
  let tiemposPostdecisionQ = [];

  //PREPARAMOS EN UN ARRAY LOS LIMITES POR ARRIBA Y POR ABAJO DEL INTEVALO DE TIEMPOS A MEDIR. USAMOS ARRAYS YA QUE SERÁ EL MISMO INTERVALO PARA TODOS LOS TIPOS DE ONDA
  //Para cada tiempo de pulsacion
  $.each(timeStampsLocalFilteredP, function(i, tiempo) {
    let fecha = new Date(timeStamps[tiempo]);
    let fechaPulsacion = new Date(timeStampsPulsacionesP[i])
    //Calculamos el momento x segundos antes
    let fechaAnterior = new Date(fecha.getTime() - $("#select-pre-decision").val());
    let fechaSiguiente = new Date(fechaPulsacion.getTime() + 500)

    //Obtenemos el tiempo medido por Muse más cercano a la pulsación
    tiemposPredecisionP.push(getClosestTime(fechaAnterior));
    tiemposAparicionP.push(getClosestTime(fecha));
    tiemposPostdecisionP.push(getClosestTime(fechaSiguiente))
  });

  $.each(timeStampsLocalFilteredQ, function(i, tiempo) {
    let fecha = new Date(timeStamps[tiempo]);
    let fechaPulsacion = new Date(timeStampsPulsacionesQ[i])
    //Calculamos el momento x segundos antes
    let fechaAnterior = new Date(fecha.getTime() - $("#select-pre-decision").val());
    let fechaSiguiente = new Date(fechaPulsacion.getTime() + 500)

    //Obtenemos el tiempo medido por Muse más cercano a la pulsación
    tiemposPredecisionQ.push(getClosestTime(fechaAnterior));
    tiemposAparicionQ.push(getClosestTime(fecha));
    tiemposPostdecisionQ.push(getClosestTime(fechaSiguiente))
  });

  //Para cada tipo de onda
  if(tiemposAparicionP.length != 0 || tiemposAparicionQ.length != 0) {

    let preDecisionChecked = $("#pre-decision-checkbox-boxes").is(':checked');
    let postDecisionChecked = $("#post-decision-checkbox-boxes").is(':checked');

    $.each(museData, function(i, tipoDeSensor) {    
      let dataPoints = [];
      let data = [];

      var max = getMax(tipoDeSensor['TP9'])
      var min = getMin(tipoDeSensor['TP9'])
  
      $.each(tipoDeSensor, function(j, array) {
  
        var newMax = getMax(array)
        var newMin = getMin(array)
  
        if (max < newMax)
          max = newMax;
        
        if(min > newMin)
          min = newMin;
      });
      
      //Para cada tipo de sensor
      $.each(tipoDeSensor, function(j, valores) {
  
        let valoresDatapointsPredecisionP = [];
        let valoresDatapointsPredecisionQ = [];
        let valoresDatapointsPostdecisionP = [];
        let valoresDatapointsPostdecisionQ = [];
  
        //AGRUPAMOS TODOS LOS TIEMPOS DE TODOS LOS TRIALS
        //Para cada tiempoPulsacion-x


        $.each(tiemposAparicionP, function(k, momentoAparicion){


          //RECORREMOS TODOS LOS TIEMPOS ENTRE tiempoPulsacion-x y tiempoPulsacion
          for(var tiempo = tiemposPredecisionP[k]; tiempo <= momentoAparicion; tiempo++)
          {
            if (valores[tiempo] != undefined && valores[tiempo] != null)
              if($("#normalizar-checkbox-boxes").is(':checked'))
                valoresDatapointsPredecisionP.push(parseFloat(normalize(valores[tiempo], max, min)));
              else
                valoresDatapointsPredecisionP.push(parseFloat(valores[tiempo]))
          }

          for(var tiempo = momentoAparicion; tiempo <= tiemposPostdecisionP[k]; tiempo++)
          {
            if (valores[tiempo] != undefined && valores[tiempo] != null)
              if($("#normalizar-checkbox-boxes").is(':checked'))
                valoresDatapointsPostdecisionP.push(parseFloat(normalize(valores[tiempo], max, min)))
              else
                valoresDatapointsPostdecisionP.push(parseFloat(valores[tiempo]))
          }
        });


        $.each(tiemposAparicionQ, function(k, momentoAparicion){
          //RECORREMOS TODOS LOS TIEMPOS ENTRE tiempoPulsacion-x y tiempoPulsacion
          for(var tiempo = tiemposPredecisionQ[k]; tiempo <= momentoAparicion; tiempo++)
          {
            if (valores[tiempo] != undefined && valores[tiempo] != null)
              if($("#normalizar-checkbox-boxes").is(':checked'))
                valoresDatapointsPredecisionQ.push(parseFloat(normalize(valores[tiempo], max, min)));
              else
                valoresDatapointsPredecisionQ.push(parseFloat(valores[tiempo]))
          }
  
          for(var tiempo = momentoAparicion; tiempo <= tiemposPostdecisionQ[k]; tiempo++)
          {
            if (valores[tiempo] != undefined && valores[tiempo] != null)
              if($("#normalizar-checkbox-boxes").is(':checked'))
                valoresDatapointsPostdecisionQ.push(parseFloat(normalize(valores[tiempo], max, min)))
              else
                valoresDatapointsPostdecisionQ.push(parseFloat(valores[tiempo]))
          }
        });

        if(preDecisionChecked)
        {
          let valoresCalculadosPredecisionP = getValoresBoxPlot(valoresDatapointsPredecisionP);
  
          dataPoints.push({
            label: "Pre-decisión de " + j + " para p",
            y: valoresCalculadosPredecisionP,
            color: coloresTipoDeSensor[j]
          });
  
          let valoresCalculadosPredecisionQ = getValoresBoxPlot(valoresDatapointsPredecisionQ);
    
          dataPoints.push({
            label: "Pre-decisión de " + j + " para q",
            y: valoresCalculadosPredecisionQ,
            color: coloresTipoDeSensor[j]
          });
        }

        if(postDecisionChecked)
        {
          let valoresCalculadosPostdecisionP = getValoresBoxPlot(valoresDatapointsPostdecisionP);
  
          dataPoints.push({
            label: "Post-decisión de " + j + " para p",
            y: valoresCalculadosPostdecisionP,
            color: coloresTipoDeSensor[j]
          });
  
          let valoresCalculadosPostdecisionQ = getValoresBoxPlot(valoresDatapointsPostdecisionQ);
    
          dataPoints.push({
            label: "Post-decisión de " + j + " para q",
            y: valoresCalculadosPostdecisionQ,
            color: coloresTipoDeSensor[j]
          });
        }
      });
  
      data.push({
        type: "boxAndWhisker",
        dataPoints: dataPoints,
        upperBoxColor: "#F0E081",
        lowerBoxColor: "#F0E081",
      });
  
      chartsCajas[i] = createChartCajas(i + '-box-chart', data, TIPOS_GRAFICOS.CAJAS)
    });
  }
}

function updateDataCajasParticipantes() {

  let participantes = Object.keys(dataJsonParticipantes)
  let preDecisionChecked = $("#pre-decision-checkbox-boxes-participants").is(':checked');
  let postDecisionChecked = $("#post-decision-checkbox-boxes-participants").is(':checked');

  $.each(chartsCajasParticipantes, function(i, chart) {

    let data = []
    let datapoints = []

    $.each(dataJsonParticipantes[participantes[0]][i], function(j){
      $.each(participantes, function(k, participante) {
        if((j.includes("Pre-decisión") && preDecisionChecked) || (j.includes("Post-decisión") && postDecisionChecked))
          datapoints.push({
            label: j + " del participante " + (parseInt(participante) + 1),
            y: [dataJsonParticipantes[participante][i][j]["minimo"], dataJsonParticipantes[participante][i][j]["cuartil1"], dataJsonParticipantes[participante][i][j]["cuartil3"], dataJsonParticipantes[participante][i][j]["maximo"], dataJsonParticipantes[participante][i][j]["cuartil2"]],
            color: coloresTipoDeSensor[j.split("decisión de ")[1]]
          });
      });
    });

    data.push({
      type: "boxAndWhisker",
      dataPoints: datapoints,
      upperBoxColor: "#F0E081",
      lowerBoxColor: "#F0E081",
    });

    chart = createChartCajas(i + '-box-participants-chart', data, TIPOS_GRAFICOS.CAJAS_PARTICIPANTES)
  });
  
}

function updateDataCajasSensores() {
  
  let sensores = Object.keys(dataJsonSensores)
  let preDecisionChecked = $("#pre-decision-checkbox-boxes-sensors").is(':checked');
  let postDecisionChecked = $("#post-decision-checkbox-boxes-sensors").is(':checked');

  $.each(chartsCajasSensores, function(i, chart) {

    let data = []
    let datapoints = []

    $.each(dataJsonSensores[sensores[0]][i], function(j){
      $.each(sensores, function(k, sensor) {

        if((j.includes("Pre-decisión") && preDecisionChecked) || (j.includes("Post-decisión") && postDecisionChecked))
          datapoints.push({
            label: j + " del sensor " + sensor,
            y: [dataJsonSensores[sensor][i][j]["minimo"], dataJsonSensores[sensor][i][j]["cuartil1"], dataJsonSensores[sensor][i][j]["cuartil3"], dataJsonSensores[sensor][i][j]["maximo"], dataJsonSensores[sensor][i][j]["cuartil2"]],
            color: coloresTipoDeSensor[sensor]
          });
      })
    });

    data.push({
      type: "boxAndWhisker",
      dataPoints: datapoints,
      upperBoxColor: "#F0E081",
      lowerBoxColor: "#F0E081",
    });

    chart = createChartCajas(i + '-box-sensors-chart', data, TIPOS_GRAFICOS.CAJAS_SENSORES)
  });
  
}


function getValoresBoxPlot(valores) {

  //Minimo, cuartil 1, cuartil3,  maximo, mediana
  var valoresCalculados = [0.0, 0.0, 0.0, 0.0, 0.0]

  valoresCalculados[0] = getMin(valores);
  valoresCalculados[1] = quartile(valores, 0.25);
  valoresCalculados[2] = quartile(valores, 0.75);
  valoresCalculados[3] = getMax(valores);
  valoresCalculados[4] = quartile(valores, 0.5);

  return valoresCalculados;
}

function quartile(vector, q) {
  const sortedVector = vector.sort((a, b) => a - b);
  const position = q * (sortedVector.length - 1);
  const base = Math.floor(position);
  const rest = position - base;
  if (sortedVector[base + 1] !== undefined) {
    return sortedVector[base] + rest * (sortedVector[base + 1] - sortedVector[base]);
  } else {
    return sortedVector[base];
  }
}




function noData(tipo_grafico) {
  hideLoading(tipo_grafico);

  if(tipo_grafico == TIPOS_GRAFICOS.LINEAS || tipo_grafico == TIPOS_GRAFICOS.CAJAS) {
    timeStamps = [];
    timeStampsFiltered = [];
    timeStampsLocalP = [];
    timeStampsLocalQ = [];
    timeStampsLocalFilteredP = [];
    timeStampsLocalFilteredQ = [];
    //timeStampsLocalAparicionLetra = [];
    timeStampsPulsaciones = [];
    timeStampsPulsacionesFiltered = [];
    timeStampsPulsacionesP = [];
    timeStampsPulsacionesQ = [];
    timeStampsComienzos = [];
    timeStampsComienzosFiltered = [];

    $.each(museData, function(i, tipoDeOnda) {
      museData[i] = {"TP9":[],"AF7":[],"AF8":[],"TP10":[]}
    });
  }
  
  hideCharts(tipo_grafico);
  if(tipo_grafico == TIPOS_GRAFICOS.LINEAS)
    updateDataLineas();
  else if(tipo_grafico == TIPOS_GRAFICOS.CAJAS)
    updateDataCajas();

}

function hideCharts(tipo_grafico) {

  switch(tipo_grafico) {
    case TIPOS_GRAFICOS.LINEAS:
      $(".chart-line-wrapper").addClass("d-none")

      $.each(chartsLineas, function(i, chart) {
        if (chart != null) {
          chart.destroy();
          chart = null
        }
      });
      break;
    case TIPOS_GRAFICOS.CAJAS:
      $(".chart-box-wrapper").addClass("d-none")

      $.each(chartsCajas, function(i, chart) {
        if (chart != null) {
          chart.destroy();
          chart = null
        }
      });
      break;
    case TIPOS_GRAFICOS.CAJAS_PARTICIPANTES:
      $(".chart-box-participants-wrapper").addClass("d-none")

      $.each(chartsCajasParticipantes, function(i, chart) {
        if (chart != null) {
          chart.destroy();
          chart = null
        }
      });
      break;
    case TIPOS_GRAFICOS.CAJAS_SENSORES:
      $(".chart-box-sensors-wrapper").addClass("d-none")

      $.each(chartsCajasSensores, function(i, chart) {
        if (chart != null) {
          chart.destroy();
          chart = null
        }
      });
      break;
  }
}


function getClosestTime(tiempo) {

  let diferencia = 0;
  let posicion = 0;
  let fecha = new Date(timeStamps[0]);

  diferencia = Math.abs(fecha.getTime() - tiempo.getTime());

  for (let i = 1; i < timeStamps.length; i++)
  {
    fecha = new Date(timeStamps[i]);
    let posibleDiferencia = Math.abs(fecha.getTime() - tiempo.getTime());

    if(posibleDiferencia <= diferencia) 
    {
      diferencia = posibleDiferencia;
      posicion = i;
    } else {
      //Como el vector timeStamps está ordenado de menor a mayor en el tiempo, en el momento en el que no se encuentre una diferencia menor, no se va a encontrar
        break;
    }
  }
  
  return posicion
}

function getClosestTimeLocal(tiempo) {

  let diferencia = 0;
  let posicion = 0;

  let fecha = new Date(timeStamps[timeStampsFiltered[0]]);

  diferencia = Math.abs(fecha.getTime() - tiempo.getTime());


  for (let i = 1; i < timeStampsFiltered.length; i++)
  {
    fecha = new Date(timeStamps[timeStampsFiltered[i]]);
    let posibleDiferencia = Math.abs(fecha.getTime() - tiempo.getTime());

    if(posibleDiferencia <= diferencia) 
    {
      diferencia = posibleDiferencia;
      posicion = timeStampsFiltered[i];
    } else {
      break;
    }
  }
  
  return posicion
}


function createChartLineas(canvas, data) {

  $('#' + canvas).removeClass("d-none")
  
  let chart = new CanvasJS.Chart(canvas, {
    
    toolTip: {
      shared: true,
      contentFormatter: function(e){
        var str = "";
        for (var i = 0; i < e.entries.length; i++){
          if(e.entries[i].dataSeries.name != "Impulsos de P" && e.entries[i].dataSeries.name != "Impulsos de Q" && e.entries[i].dataSeries.name != "Pulsaciones" && e.entries[i].dataSeries.name != "Aparición de letras" )
            var temp = "<span style=color:" + e.entries[i].dataSeries.color + ";>" + e.entries[i].dataSeries.name + " <strong>"+  e.entries[i].dataPoint.y + "</strong> </span> <br/>" ; 
          else if(e.entries[i].dataSeries.name != "Pulsaciones")
            var temp = "<span> <strong>En este momento se sintió un impulso</strong> </span> <br/>" ; 
          else if(e.entries[i].dataSeries.name != "Aparición de letras")
            var temp = "<span> <strong>En este momento comenzaron a aparecer letras</strong> </span> <br/>" ; 
          else
            var temp = "<span> <strong>En este momento se realizó una pulsación</strong> </span> <br/>" ; 

          str = str.concat(temp);
        }
        return (str);
      }
    },
    animationEnabled: true,
    zoomEnabled: true,
    theme: "light2",
    legend:{
      cursor: "pointer",
      fontSize: 16,
      itemclick: (function toggleDataSeries(e){
        if (typeof(e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
          e.dataSeries.visible = false;
        }
        else{
          e.dataSeries.visible = true;
        }
        chart.render();
      })
    },
    axisX:{
      title: "Tiempo (ms)",
      titleFontSize : 20
     },
    data: data
  });


  if($("#ver-lineas").hasClass("active")) {
    chart.render();
  }

  return chart;
}

function createChartCajas(canvas, data, tipoChart) {

  $('#' + canvas).removeClass("d-none")

  var labelFontSize = 20;
  if(data[0].dataPoints.length == 8)
    labelFontSize = 14;
  else if(data[0].dataPoints.length > 8)
    labelFontSize = 10;
  

  let chart = new CanvasJS.Chart(canvas, {
    animationEnabled: true,
    axisX: {
      interval: 1,
      labelFontSize: labelFontSize
    },
    data: data
  });

  if(tipoChart == TIPOS_GRAFICOS.CAJAS && $("#ver-cajas").hasClass("active")) {
    chart.render();
  } else if(tipoChart == TIPOS_GRAFICOS.CAJAS_PARTICIPANTES && $("#ver-cajas-participantes").hasClass("active")) {
    chart.render();
  } else if(tipoChart == TIPOS_GRAFICOS.CAJAS_SENSORES && $("#ver-cajas-sensores").hasClass("active")) {
    chart.render();
  }

  return chart;
}


function showLoading(tipo_grafico){
  hideCharts(tipo_grafico);

  switch(tipo_grafico) {
    case TIPOS_GRAFICOS.LINEAS:
      $('.lines-spinner-wrapper').removeClass("d-none")
      break;
    case TIPOS_GRAFICOS.CAJAS:
      $('.box-spinner-wrapper').removeClass("d-none")
      break;
    case TIPOS_GRAFICOS.CAJAS_PARTICIPANTES:
      $('.box-participants-spinner-wrapper').removeClass("d-none")
      break;
    case TIPOS_GRAFICOS.CAJAS_SENSORES:
      $('.box-sensors-spinner-wrapper').removeClass("d-none")
      break;
  }
}

function hideLoading(tipo_grafico){
  switch(tipo_grafico) {
    case TIPOS_GRAFICOS.LINEAS:
      $('.lines-spinner-wrapper').addClass("d-none")
      break;
    case TIPOS_GRAFICOS.CAJAS:
      $('.box-spinner-wrapper').addClass("d-none")
      break;
    case TIPOS_GRAFICOS.CAJAS_PARTICIPANTES:
      $('.box-participants-spinner-wrapper').addClass("d-none")
      break;
    case TIPOS_GRAFICOS.CAJAS_SENSORES:
      $('.box-sensors-spinner-wrapper').addClass("d-none")
      break;
  }
}

function normalize(val, max, min) { return (val - min) / (max - min) * 2 - 1; }

function getMax(arr) {
  let len = arr.length;
  let max = -Infinity;

  while (len--) {
      max = arr[len] > max ? arr[len] : max;
  }
  return max;
}


function getMin(arr) {
  let len = arr.length;
  let min = Infinity;

  while (len--) {
      min = arr[len] < min ? arr[len] : min;
  }
  return min;
}
