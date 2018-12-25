
const express   = require('express');
const Chain     = require('Blockchain');
const Block     = require('Block');


app = express();
let chain = new Chain.Blockchain();


app.get('/block/:height', function(req, res) {
    console.log(req.params['height']);
});


app.post('/block', function(req, res) {

});


app.listen(process.env.PORT || 8000, function() {
    console.log('Listening on port ' + app.get('port'));
});

