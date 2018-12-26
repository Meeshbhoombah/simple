
const express     = require('express');
const bodyParser  = require('body-parser')
const Chain       = require('./simple/Blockchain');
const Block       = require('./simple/Block');
const yup         = require('yup');


app = express();
const PORT = 8000;


app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));


const chain = new Chain.Blockchain();


/* READ validation */
app.post('/requestValidation', (req, res) => {

});


app.post('/message-signature/validate', (req, res) => {

});


/* CREATE star */
let starBodySchema = yup.object().shape({
    address: yup.string().max(34).required(),
    star: yup.object().shape({
        dec: yup.string().min(3).required(),
        re: yup.string().min(3).required(),
        story: yup.string().matches(/[a-zA-Z0-9]/).min(3).required()
    })
});


app.post('/block', (req, res) => {

});


/* READ one block from hash */
app.get('/stars/:hash', (req, res) => {

});


/* READ one decoded star with address */
app.get('/stars/:address', (req, res) => {

});


/* READ one block from height */
app.get('/block/:height', async (req, res) => {
    var blockRef = parseInt(req.params['height']);

    await chain.getBlock(blockRef)
    .then((block) => {
             
    })
    .catch((err) => {
        console.log('Could not retrive Block:', err.stack);
    })
});


app.listen(PORT, () => console.log('Listening on port:', PORT));

