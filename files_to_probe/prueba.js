// LEER JSON
/*
// Usando FS
const fs = require('fs')
let data = fs.readFileSync('../future_json_structures/info_users.json')
let usuarios = JSON.parse(data);
console.log(usuarios)
*/

/*
// Recurriendo directamente al fichero (CUIDADO ESTA OPCION SOLO FUNCIONA LA PRIMERA VEZ)
let jsonData = require('../future_json_structures/info_users.json')
console.log(jsonData)
*/

// ESCRIBIR JSON
const fs = require('fs')

let data = [
    {
      "username": "admin",
      "password": "1234",
      "role": "ADMIN"
    },
    {
      "username": "monitor",
      "password": "1234",
      "role": "MONITOR"
    },
    {
      "username": "U1",
      "password": "Contraseña",
      "role": "MONITOR"
    },
    {
      "username": "U2",
      "password": "Contraseña",
      "role": "MONITOR"
    }
]

let jsonData = JSON.stringify(data);
console.log(jsonData)

fs.writeFile('./prueba.json', jsonData, (error) => {
    if(error) {
        console.log(`Error: ${error}`);
    } else {
        console.log("Archivo JSON generado")
    }
})