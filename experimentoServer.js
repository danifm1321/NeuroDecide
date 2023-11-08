const fs = require('fs');
const createCsvWriter = require('csv-writer').createObjectCsvWriter;

var csvWriter;

function registroUsuario(emailUsuario, generoUsuario) {
    var user;

    try {
      let rawdata = fs.readFileSync('secrets/users.json');
      let users = JSON.parse(rawdata);
      let higherID = 0;

      for (var i=0 ; i < users.length ; i++) {
        if(users[i]['id'] > higherID) {
          higherID = users[i]['id'];
        }

        if(users[i]['email'] == emailUsuario) 
          user = users[i];
      }

        
      if(user == undefined)
      {
        user = creaNuevoUsuario(emailUsuario, generoUsuario, higherID)
        users.push(user)

        let data = JSON.stringify(users);
        fs.writeFile('secrets/users.json', data, function(err, result) {
          if(err) console.log('error', err);
        });
      } else {

        creaCSVWriterConAppend(user.id);
        //Ya que si se añade append: true, csv writer no introduce la cabecera se ha de comprobar si el archivo en el que se van a introducir los datos
        //existe para introducir a mano la cabecera.
        creaCabecera(user.id)

      }
    } catch (err) {

      //SI NO EXISTE EL ARCHIVO, ES DECIR, NO SE HA REGISTRADO NINGUN USUARIO
      if (err.code === 'ENOENT') {
        user = creaPrimerUsuario(emailUsuario, generoUsuario)
      } else {
        throw err;
      }
    }

    return {
        userId: user['id']
      };
}

function creaCSVWriterSinAppend(id) {
    csvWriter = createCsvWriter({
        path: 'data/results' + id+ '.csv',
        header: [
        {id: 'id', title: 'ID del participante'},
        {id: 'trial', title: 'Trial'},
        {id: 'respuesta', title: 'Respuesta'},
        {id: 'tInicio', title: 'Tiempo de inicio'},
        {id: 'tApareceLetra', title: 'Tiempo de aparición de letras'},
        {id: 'tiempoPulsacion', title: 'Tiempo de la pulsación'},
        {id: 'tecla', title: 'Tecla elegida'},
        {id: 'tiempoAparicionLetraElegida', title: 'Tiempo de aparición de la letra observada'},
        {id: 'letraElegida', title: 'Letra observada'},
        ]
    });
}

function creaCSVWriterConAppend(id) {
    csvWriter = createCsvWriter({
        path: 'data/results' + id+ '.csv',
        header: [
          {id: 'id', title: 'ID del participante'},
          {id: 'trial', title: 'Trial'},
          {id: 'respuesta', title: 'Respuesta'},
          {id: 'tInicio', title: 'Tiempo de inicio'},
          {id: 'tApareceLetra', title: 'Tiempo de aparición de letras'},
          {id: 'tiempoPulsacion', title: 'Tiempo de la pulsación'},
          {id: 'tecla', title: 'Tecla elegida'},
          {id: 'tiempoAparicionLetraElegida', title: 'Tiempo de aparición de la letra observada'},
          {id: 'letraElegida', title: 'Letra observada'},
        ],
        append: true
      });
}

function creaNuevoUsuario(email, genero, higherID) {
    user = {
        email: email,
        genero: genero,
        id : higherID+1,
        session : -1
    }

    creaCSVWriterSinAppend(user.id);

    return user
}

function creaCabecera(id) {
    fs.readFile('data/results' + id+ '.csv', function(err, data) {
        if (data == undefined || data.length == 0) {

          let data = [{
            id : 'ID del participante',
            trial : 'Trial',
            respuesta : 'Respuesta',
            tInicio : 'Tiempo de inicio',
            tApareceLetra : 'Tiempo de aparición de letras',
            tiempoPulsacion : 'Tiempo de la pulsación',
            tecla : 'Tecla elegida',
            tiempoAparicionLetraElegida : 'Tiempo de aparición de la letra observada',
            letraElegida : 'Letra observada'
          }];

          csvWriter
          .writeRecords(data)
          .then(()=> console.log('Header was written successfully'));
        }
      })
}

function creaPrimerUsuario(emailUsuario, generoUsuario) {
    let users = [{
        email: emailUsuario,
        genero: generoUsuario,
        id : 0,
        session : -1
      }]


      creaCSVWriterSinAppend(users[0].id);


      let data = JSON.stringify(users);
      fs.writeFile('secrets/users.json', data, function(err, result) {
        if(err) console.log('error', err);
      });

      return users[0];
}

function grabarCSV(req, res) {
    const { id } = req.body
    const { trial } = req.body
    const { respuesta } = req.body
    const { tInicio } = req.body
    const { tApareceLetra } = req.body
    const { tPulsacion } = req.body
    const { eleccion } = req.body
    const { tAparicionLetraElegida } = req.body
    const { letraElegida } = req.body

    var data = [{
      id : id,
      trial : trial,
      respuesta : respuesta,
      tInicio : tInicio,
      tApareceLetra : tApareceLetra,
      tiempoPulsacion : tPulsacion,
      tecla : eleccion,
      tiempoAparicionLetraElegida : tAparicionLetraElegida,
      letraElegida : letraElegida
    }];
  
    console.log(data)

    csvWriter
        .writeRecords(data)
        .then(()=> console.log('The CSV file was written successfully'));

    return res.status(200).json({
      codigo : 200
    });
}

module.exports.registroUsuario = registroUsuario;
module.exports.grabarCSV = grabarCSV;