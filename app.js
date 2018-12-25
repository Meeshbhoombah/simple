
const express    = require('express');
const bodyParser = require('body-parser')
const Chain     = require('./simple/Blockchain');
const Block     = require('./simple/Block');


app = express();
const PORT = 8000;


let chain = new Chain.Blockchain();


app.get('/block/:height', function(req, res) {
    console.log(req.params['height']);
});


app.post('/block', function(req, res) {
    console.log(req.body);
});


app.listen(PORT, function() {
    console.log('Listening on port:', PORT);
});

