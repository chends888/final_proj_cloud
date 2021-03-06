const express = require('express');
const mysql = require('mysql');
const app = express();
const port = 5000;


// const router = express.Router();

// const connection = mysql.createConnection({
//   host: "localhost",
//   user: "root",
//   password: "8888",
//   database: "dbtechedu"
// })


// app.get("/tarefa", function (req, res) {
    // connection.query("SELECT * FROM Alunos", function (error, results, fields) {
    //   if (error) throw error;
    //   const alunos = results;
    //   console.log(Alunos)
    //   res.json(results)
    // })
// })

// app.get("/eventos", function (req, res) {
    // connection.query("SELECT * FROM Eventos", function (error, results, fields) {
    //     if (error) throw error;
    //     const eventos = results;
        // console.log(eventos[0]['diaehora']);
        // let ano = eventos[0]['diaehora'];
        // console.log(ano.getFullYear());
        // res.json(results)
        //let x = new Date(2004-05-02T03:00:00.000Z);
    // })
// })

app.get("/hello", function (req, res) {
    //Getting key
    let key = req.query.key;
    // console.log(key);
    // console.log(typeof(key))
    // console.log(typeof(parseFloat(key)));
    iterations = parseInt(key, 10);
    helloworld_base = 'hello world \n';
    helloworld = 'hello world \n';
    for (let i = 0; i < iterations; i++) {
        helloworld = helloworld_base + helloworld;
    }
    res.send(helloworld)
})


app.get("/healthcheck", function (req, res) {
    res.send(200)
})



// app.get("/aulas", function (req, res) {
//     connection.query("SELECT * FROM Aulas", function (error, results, fields) {
//       if (error) throw error;
//       const professores = results;
//       res.json(results)
//     })
// })

// app.get("/workshops", function (req, res) {
//     connection.query("SELECT * FROM Workshops", function (error, results, fields) {
//       if (error) throw error;
//       const professores = results;
//       res.json(results)
//     })
// })

// app.get('/', function (req, res) {
//     res.json({ a: 1 });
// });

app.listen(port, function () {
    console.log('listening on port:', port)
})