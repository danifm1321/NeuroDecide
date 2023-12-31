const http = require('http');
const express = require('express');
const fs = require('fs');

const graficosServer = require('./graficosServer');
const experimentoServer = require('./experimentoServer');
const logger = require('./logger');

const app = express();
app.use(express.json());
app.use(express.static("express"));

app.set('view engine', 'ejs');

//serve index page
app.get('/', function(req, res) {

  var active = "inicio";

  res.render('pages/index', {
    active : active
  });
});

//serve experiment page 
app.get('/experimento', function(req, res) {

  var active = "experimento";

  res.render('pages/experimento', {
    active: active
  });
});

//serve graphs page 
app.get('/graficos', function(req, res) {

  var active = "graficos";

  res.render('pages/graficos', {
    active: active
  });
});

app.post('/identificarUsuario', function(req, res) {
  const { emailUsuario } = req.body;

  respuesta = experimentoServer.identificacionUsuario(emailUsuario);

  return res.status(200).json(respuesta);
});

app.post('/registrarUsuario', function(req, res) {
  const { emailUsuario, generoUsuario } = req.body

  respuesta = experimentoServer.registroUsuario(emailUsuario, generoUsuario);

  return res.status(200).json(respuesta);
});

app.put('/aniadirSesion/:id', function(req, res) {
  const idAAniadir = req.params.id;

  let rawdata = fs.readFileSync('secrets/users.json');
  let users = JSON.parse(rawdata);

  let newSession;

  for (var i=0 ; i < users.length ; i++)
    if(users[i]['id'] == idAAniadir)
    {
      users[i]['session']++;
      newSession = users[i]['session']
    }
    
  let data = JSON.stringify(users);
  fs.writeFile('secrets/users.json', data, function(err, result) {
    if(err) logger.error("Error creating the users file: " + err);
  });

  return res.status(200).json({
    session: newSession
  });
});

app.post('/grabarCSV', function(req, res) {
  return experimentoServer.grabarCSV(req, res);
});

app.get('/getUsuarios', function(req, res) {
  return res.status(200).json(JSON.stringify(graficosServer.getUsuarios()));    
});

app.get('/getSesiones/:user', function(req, res) {

  const user = req.params.user;

  graficosServer.getSesiones(user)
  .then(sesiones => {
    return res.status(200).json(JSON.stringify(sesiones));
  })
  .catch(err => {
    logger.error("Error getting the sessions: " + err)
    return res.status(500).json({ error: 'Error en el servidor' });
  });
});

app.get('/getData/:user/:sesion', function(req, res) {
  const user = req.params.user;
  const sesion = req.params.sesion;

  return graficosServer.getData(user, sesion)
  .then(data => {
    return res.status(200).json(JSON.stringify(data));
  })
  .catch(err => {
    logger.error("Error getting the data: " + err)
    return res.status(500).json({ error: 'Error en el servidor' });
  });
});

app.post('/getDataCajasParticipantes', function(req, res) {
  const{ participantes, milisegundos, normalizar } = req.body;

  graficosServer.getMedidasCalculadasParticipantes(JSON.stringify(participantes), milisegundos, normalizar)
  .then(data => {
    return res.status(200).json(data);
  })
  .catch(err => {
    logger.error("Error getting the participants data: " + err)
    return res.status(500).json({ error: 'Error en el servidor' });
  });
});

app.post('/getDataCajasSensores', function(req, res) {
  const { sensores, milisegundos, normalizar } = req.body;

  graficosServer.getMedidasCalculadasSensores(JSON.stringify(sensores), milisegundos, normalizar)
    .then(json => {
      return res.status(200).json(json)
    })
    .catch(err => {
      logger.error("Error getting the sensors data: " + err)
      return res.status(500).json({ error: 'Error en el servidor' });
    });
  });


 fs.readFile('config.json', 'utf8', (err, data) => {
  if (err) {
    logger.error("Error reading the config data: " + err)
    return;
  }

  const config = JSON.parse(data);
  const serverPort = config.port;

  const server = http.createServer(app);
  server.timeout = 5000000;
  server.listen(serverPort);
  logger.info('Server listening on port ' + serverPort);
});
