const request = require('request');

// request('http://localhost:5000/hello/?key=8', function(error, response, body){
//     if(error) console.log(error);
//     else console.log(body, "\n");
// });

request('http://localhost:5000/healthcheck', function(error, response, body){
    if(error) console.log(error);
    else console.log(body, "\n");
});
