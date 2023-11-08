const fs = require('fs');
const csvReader = require('csv-parser');
const localDataObjectFile = require('./localDataObject');
const localMuseDataObjectFile = require('./museDataObject');
const { spawn } = require('child_process');

var fileUploadPath = ''

fs.readFile('config.json', 'utf8', (err, data) => {
  if (err) {
    console.error('Error al leer el archivo de configuración:', err);
    return;
  }

  const config = JSON.parse(data);
  fileUploadPath = config.museDataPath;
});

function getUsuarios() {

    let participantes = []

    const resultsFileRegex = /^results\d+\.csv$/;

    fs.readdirSync("data/").forEach(file => {
      if (resultsFileRegex.test(file)) {

        let participante = parseInt(file.split("results")[1].split('.csv')[0]);

        if(participante >= 0)
          participantes.push(participante);
      }   
    });

    participantes.sort((a, b) => a - b);


    return participantes;
}

function getSesiones(participanteEleccion) {

  let trials = [];

  return new Promise((resolve, reject) => {
    if (fs.existsSync('data/results' + participanteEleccion + '.csv')) {
      fs.createReadStream('data/results' + participanteEleccion + '.csv')
      .pipe(csvReader({columns : true}))
      .on('data', (row) => {
        if(!trials.includes(parseInt(row['Trial']))) {
          trials.push(parseInt(row['Trial']))
        }
      }).on('end', () => {
        resolve(trials);
      });
    } else {
      reject(ERR_INVALID_FILE_URL_PATH);
    }
  });

}

function getData(participante, sesion) {
    var CSVSession = []
    var dataMuse = []
    var dataLocal = []

    return new Promise((resolve, reject) => {
      if (fs.existsSync('data/results' + participante + '.csv')) {
        fs.createReadStream('data/results' + participante + '.csv')
        .pipe(csvReader({columns : true}))
        .on('data', (row) => {
          if(sesion == row["Trial"])
          {
            CSVSession.push(row)
          }
        })
        .on('end', () => {
          //console.log('CSV file successfully processed');
  
          if (CSVSession.length != 0)
          {
  
            /*
            dataLocal.push(CSVSession[0]["Tiempo de inicio"]);
            */
  
            CSVSession.forEach ( dataSession => {
              var localData = new localDataObjectFile.LocalDataObject(dataSession["Tiempo de aparición de la letra observada"], dataSession["Tecla elegida"], dataSession["Tiempo de la pulsación"], dataSession["Tiempo de aparición de letras"])
              dataLocal.push(localData);
            });
            
  
            var inicioSesion = new Date(CSVSession[0]["Tiempo de inicio"]);
            var finalSesion = new Date(CSVSession[CSVSession.length-1]["Tiempo de la pulsación"]);
  
            if (fs.existsSync(fileUploadPath + '/museData' + participante + '.csv')) {
              fs.createReadStream(fileUploadPath + '/museData' + participante + '.csv')
              .pipe(csvReader({columns : true}))
              .on('data', (row2) => {
  
                if(row2["Elements"] == undefined || row2["Elements"] == "") {
                  var tiempoMuse = new Date(row2["TimeStamp"]);
  
                  if(tiempoMuse > inicioSesion && tiempoMuse < finalSesion) {
                    var dataObject = new localMuseDataObjectFile.MuseDataObject(row2["TimeStamp"], row2["Delta_TP9"], row2["Delta_AF7"], row2["Delta_AF8"], row2["Delta_TP10"], row2["Theta_TP9"], row2["Theta_AF7"], row2["Theta_AF8"], row2["Theta_TP10"], row2["Alpha_TP9"], row2["Alpha_AF7"], row2["Alpha_AF8"], row2["Alpha_TP10"], row2["Beta_TP9"], row2["Beta_AF7"], row2["Beta_AF8"], row2["Beta_TP10"], row2["Gamma_TP9"], row2["Gamma_AF7"], row2["Gamma_AF8"], row2["Gamma_TP10"], row2["RAW_TP9"], row2["RAW_AF7"], row2["RAW_AF8"], row2["RAW_TP10"])
    
                    dataMuse.push(dataObject);
                  }
                }
              }).on('end', () => {
  
                var finalData = [dataLocal, dataMuse]
  
               resolve(finalData);
              });
            } else {
              reject(ERR_INVALID_FILE_URL_PATH);
            }
          }
        });
      }
    });
}

function getMedidasCalculadasParticipantes(participantes, milisegundos, normalizar) {

  const pythonScript = spawn('python3', ['pythonScripts/medidas_calculadas_participantes.py', participantes, milisegundos, normalizar, fileUploadPath]);

  pythonScript.stderr.on('data', (data) => {
    console.error(`Error: ${data}`);
  });

  pythonScript.on('close', (code) => {
    console.log(`child process exited with code ${code}`);
  });

  return new Promise((resolve) => {
    pythonScript.stdout.on('data', (data) => {
      resolve(data.toString())
    });
  });
}

function getMedidasCalculadasSensores(sesiones, milisegundos, normalizar) {

  const pythonScript = spawn('python3', ['pythonScripts/medidas_calculadas_sensores.py', sesiones, milisegundos, normalizar, fileUploadPath]);

  pythonScript.stderr.on('data', (data) => {
    console.error(`Error: ${data}`);
  });

  pythonScript.on('close', (code) => {
    console.log(`child process exited with code ${code}`);
  });

  return new Promise((resolve) => {
    pythonScript.stdout.on('data', (data) => {
      resolve(data.toString())
    });
  });
}

module.exports.getUsuarios = getUsuarios;
module.exports.getSesiones = getSesiones;
module.exports.getData = getData;
module.exports.getMedidasCalculadasParticipantes = getMedidasCalculadasParticipantes;
module.exports.getMedidasCalculadasSensores = getMedidasCalculadasSensores;


