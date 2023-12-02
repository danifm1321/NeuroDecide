const {transports, createLogger, format} = require('winston');

// Configuración de Winston
const logger = createLogger({
  level: 'info', // Nivel mínimo de logs a mostrar
  format: format.combine(
    format.timestamp(),
    format.json()
    ),
  transports: [
    new transports.Console(), // Salida de consola
    new transports.File({ filename: 'logs/error.log', level: 'error' }), // Archivo de errores
    new transports.File({ filename: 'logs/combined.log' }) // Archivo general
  ]
});

module.exports = logger;