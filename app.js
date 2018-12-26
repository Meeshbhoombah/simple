
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


const VALIDATION_TIMEOUT = 300; // (seconds)
var cache = {};


/******** REQUEST MESSAGE VALIDATION *********/
const addressSchema = yup.object().shape({
    address: yup.string().max(34).required()
})

app.post('/requestValidation', (req, res) => {
    let requestAddress = req.body;

    addressSchema
    .validate(requestAddress)
    .catch((err) => {
        let response = {
            statusCode: 400,
            error: err
        };

        return res.status(response.statusCode).send(response);
    });


    let address = requestAddress['address'];
    let requestObject = cache[address];
    let timestamp = new Date().getTime().toString().slice(0, -3);
    
    if (requestObject) {
        let elapsedTime = timestamp - requestObject.timestamp;
        let refreshedWindow = 300 - elapsedTime;

        requestObject.timestamp = refreshedWindow;
        cache[address] = requestObject;

        return res.status(200)        
            .set("Content-Type", "application/json")
            .send(cache[address]);
    }


    let response = {
        walletAddress: address,
        requestTimeStamp: timestamp,
        message: `${address}:${timestamp}:starRegistry`,
        validationWindow: 300
    }

    cache[address] = response;
    let timeout = response.validationWindow * 1000;
    setTimeout(() => { delete requestCache[userResponse.address]; }, timeout);

    return res.status(200)
        .set("Content-Type", "application/json") 
        .send(response);
});


/******** VALIDATE MESSAGE SIGNATURE *********/
const signedMessageSchema = yup.object().shape({
    address: yup.string().max(34).required(),
    signature: yup.string().max(88).required()
})

app.post('/message-signature/validate', (req, res) => { 
    var signedMessageRequest = req.body;
   
    signedMessageSchema
    .validate(signedMessageRequest)
    .catch((err) => {
        let response = {
            statusCode: 400,
            error: err
        };

        return res.status(response.statusCode).send(response);
    });


    let address = req.body['address'];
    let signature = req.body['signature'];
    let requestObject = cache[address];

    if (!requestObject) {
        let response = {
            statusCode: 400,
            error: 'Validation request not made within window/wallet address invalid.'
        };

        return res.status(response.statusCode).send(response);
    }

});


/* CREATE star */
const starBodySchema = yup.object().shape({
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

