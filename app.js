
const express     = require('express');
const bodyParser  = require('body-parser')
const Chain       = require('./simple/Blockchain');
const Block       = require('./simple/Block');
const yup         = require('yup');
const btcMsg      = require('bitcoinjs-message');


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

    console.log('msg', requestObject.message);
    console.log(address);
    console.log(signature);

    try {
        let validSignature = btcMsg.verify(requestObject.message, address, signature);

        if (validSignature !== true) {
            throw new Error('Provided credentials failed to sign message.')   
        }
    } catch (err) {
        let response = {
            statusCode: 502,
            error: err
        };

        return res.status(response.statusCode).send(response);
    }

    let timestamp = new Date().getTime().toString().slice(0, -3);
    let timeElapsed = timestamp - requestObject.requestTimeStamp;
    let refreshedWindow = 300 - timeElapsed;

    let response = {
        registerStar: true,
        status: {
            address: address,
            requestTimeStamp: requestObject.requestTimeStamp,
            message: requestObject.message,
            validationWindow: refreshedWindow,
            messageSignature: 'valid'
        }
    }

    return res.status(200)
        .set("Content-Type", "application/json")
        .send(response);
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

function _toHexa(str) {
    let hexa = [];

    for (let n = 0; l = str.length; n < l, n++) {
        let hex = Number(str.charCodeAt(n).toString(16));
        hexa.push(hex);
    }

    return hexa.join('');
};

app.post('/block', async (req, res) => {
    var createStarBody = req.body;

    starBodySchema
    .validate(createStarBody)
    .catch((err) => {
        let response = {
            statusCode: 400,
            error: err
        };

        return res.status(response.statusCode).send(response);
    });

    let address = createStarBody['address'];
    let requestObject = cache[address];

    if (!requestObject) {
        let response = {
            statusCode: 400,
            error: 'Validation request not made within window/wallet address invalid.'
        };

        return res.status(response.statusCode).send(response);
    }
    
    let story = createStarBody['star']['story'];
    createStarBody['start']['story'] = toHexa(story);

    chain.addBlock(new Block(createStarBody))
    .then((registedStar) => {
        delete cache[address];

        return res.status(200)        
            .set("Content-Type", "application/json")
            .send(registeredStar);
    })
    .catch((err) => {
        let response = {
            statusCode: 502,
            error: err
        };

        return res.status(response.statusCode).send(response);
    });
});


/* READ one block from hash */
function _toAscii(hex) {
    let ascii = [];

    let hexa = hex.toString();
    let str = '';

    for (let n = 0; n < hexa.length; n += 2) {
        str += String.fromCharCode(parseInt(hexa.substr(n, 2), 16));
    }

    return str;
};

app.get('/stars/:hash', async (req, res) => {         
    var registeredStarDigest = req.params.hash.toString();
    let star = ''

    try {
        star = await chain.getStar(registeredStarDigest);

        if (!star) {
            throw new Error('No star found for given hash.')
        }
    } catch (err) {
        let response = {
            statusCode: 400,
            error: err
        };

        return res.status(response.statusCode).send(response);
    }

    let starWithDecodedStory = [];
    for (let starObject of star) {
        starObject.body.star["storyDecoded"] = hexaToAscii(starObject.body.star.story);
        starWithDecodedStory.push(starObject);
    }

    return res.status(200)
              .set("Content-Type", "application/json")
              .send(starWithDecodedStory[0]);
});


/* READ one decoded star with address */
app.get('/stars/:address', async (req, res) => {

    starBodySchema
    .validate(createStarBody)
    .catch((err) => {
        let response = {
            statusCode: 400,
            error: err
        };

        return res.status(response.statusCode).send(response);
    });

    let address = req.params.addr.toString();
    //console.log("Address is:  ", address);

    let response = {
        status_code: null,
        status: null,
        reason: null,
    };

    // Get all stars against a certain wallet address
    let stars = await blockChain.getAllStarsOfWallet(address);

    // Checking if the DB query was successfull or not
    if (!stars) {

        let reason = `Could not retrieve stars for wallet: ${address}`;
        response.status_code = 500;
        response.status = "Internal Server Error.";
        response.reason = reason;

        return res.status(response.status_code)
                  .set("Content-Type", "application/json")
                  .send(response);
    }

    // Check if the returned stars array has length. If zero, then no stars for that address
    if (stars.length === 0) {

        let reason = `Bad Request. No stars for wallet: ${address}`;
        response.status_code = 400;
        response.status = "Star Info Retrieval Failed.";
        response.reason = reason;

        return res.status(response.status_code)
                  .set("Content-Type", "application/json")
                  .send(response);
    }

    // If there are stars for the wallet address return them with decoded story
    let starsWithDecodedStory = [];
    for (let starObject of stars) {
        starObject.body.star["storyDecoded"] = hexaToAscii(starObject.body.star.story);
        starsWithDecodedStory.push(starObject);
    }

    return res.status(200)
              .set("Content-Type", "application/json")
              .send(starsWithDecodedStory);


});


/* READ one block from height */
app.get('/block/:height', async (req, res) => {
const blockHash = req.params.blockHash.toString();

    let response = {
        status_code: null,
        status: null,
        reason: null,
    };

    // Get star against blockHash
    let star = await blockChain.getStarAgainstHash(blockHash);

    // Checking if the DB query was successfull or not
    if (!star) {

        let reason = `Could not retrieve star for blockHash: ${blockHash}`;
        response.status_code = 500;
        response.status = "Internal Server Error.";
        response.reason = reason;

        return res.status(response.status_code)
                  .set("Content-Type", "application/json")
                  .send(response);
    }

    // Check if the returned star array has length. If zero, then no stars for that address
    if (star.length === 0) {

        let reason = `Bad Request. No star for blockHash: ${blockHash}`;
        response.status_code = 400;
        response.status = "Star Info Retrieval Failed.";
        response.reason = reason;

        return res.status(response.status_code)
                  .set("Content-Type", "application/json")
                  .send(response);
    }

    // If there is a star for the blockHash return it with decoded story
    let starWithDecodedStory = [];
    for (let starObject of star) {
        starObject.body.star["storyDecoded"] = hexaToAscii(starObject.body.star.story);
        starWithDecodedStory.push(starObject);
    }

    return res.status(200)
              .set("Content-Type", "application/json")
              .send(starWithDecodedStory[0]);


    var blockRef = parseInt(req.params['height']);

    await chain.getBlock(blockRef)
    .then((block) => {
             
    })
    .catch((err) => {
        console.log('Could not retrive Block:', err.stack);
    })
});


app.listen(PORT, () => console.log('Listening on port:', PORT));

