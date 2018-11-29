const request = require('request');

// request('http://localhost:3000/alunos', function(error, response, body){
//     if(error) console.log(error);
//     else console.log(body, "\n");
// });

// request('http://localhost:3000/eventos', function(error, response, body){
//     if(error) console.log(error);
//     else console.log(body, "\n");
// });

request('http://localhost:3000/professores/?key=8', function(error, response, body){
    if(error) console.log(error);
    else console.log(body, "\n");
});

// request('http://localhost:3000/aulas', function(error, response, body){
//     if(error) console.log(error);
//     else console.log(body, "\n");
// });

// request('http://localhost:3000/workshops', function(error, response, body){
//     if(error) console.log(error);
//     else console.log(body, "\n");
// });