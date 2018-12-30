/* ===== Blockchain Class ==========================
|  Class with a constructor for new blockchain 		|
|  ================================================*/

const SHA256 = require('crypto-js/sha256');
const Level = require('./LevelInterface.js');
const Block = require('./Block.js');

class Blockchain {
    constructor() {
        this.db = new Level.Wrapper();
        this.generateGenesisBlock();
    }

    generateGenesisBlock() {
        let _this = this
        
        _this.getBlockHeight()
        .then((blockHeight) => {
            if (blockHeight == 0) {
                let genBlock = new Block.Block('The New Frontier');

                _this.addBlock(genBlock)
                .then((genesisBlock) => {
                    console.log('Initalized chain with Genesis Block: ', genBlock);
                    return;
                })
                .catch((err) => {
                    console.log('Failed to generate Genesis Block:', err);
                    process.exit();
                });

            } else {
                return; 
            }
        })
        .catch((err) => {
            return err;
        });
    };

    getBlockHeight() {
        let _this = this;

        return new Promise(async (resolve, reject) => {
            await _this.db.getBlocksCount()
            .then((height) => {
                resolve(height)
            })
            .catch((err) => {
                reject(err)
            });
        });
    };

    addBlock(block) {
        let _this = this;

        block.time = new Date().getTime();

        return _this.getBlockHeight()
        .then(async (blockHeight) => {
            block.height = blockHeight;
            // Genesis block prevBlockHash is empty
            if (block.height !== 0) {
                var previousBlock = block.height - 1;
                console.log('Block to get', previousBlock);
                await _this.getBlock(previousBlock)
                .then((prevBlock) => {
                    // check's integirty
                    block.prevBlockHash = SHA256(JSON.stringify(prevBlock)).toString(); 
                })
                .catch((err) => {
                    return err; 
                });
            }

            // The block hash is composed
            block.hash = SHA256(JSON.stringify(block)).toString();

            return new Promise(async (resolve, reject) => {
                await _this.db.put(block.height, block)
                .then(() => {
                    resolve(block);
                })
                .catch((err) => {
                    reject(err);
                });
            });
        })
        .catch((err) => {
            return err;
        });
    };

    getBlock(height) {
        let _this = this;

        var blockRef = height;

        return new Promise(async (resolve, reject) => {
            await _this.db.get(blockRef)
            .then((block) => {
                resolve(block);
            })
            .catch((err) => {
                reject(err);
            });
        });
    };

    getStar(hashToMatch) {
        let _this = this;
        let star;

        return new Promise((resolve, reject) => {
            _this.db.createReadStream()
            .on('data', (data) => {
                var block = JSON.parse(data.value);
                var blockDigest = block.parse;
        
                if (hashToMatch == blockDigest) {
                    star = block; 
                }
            })
            .on('close', (data) => {
                resolve(star);
            })
            .on('error', (err) => {
                reject(err);
            });
        });
    };

    getStartFromAddress(addressToMatch) {
        let _this = this;
        let stars = [];
        let starObject;

        return new Promise((resolve, reject) => {
            _this.db.createReadStream().on('data', function (data) {
                try {
                  starObject = JSON.parse(data.value.toString());
                  //console.log(starObject);
                } catch(e) {
                    console.log("parse exception:  ", e.stack);
                    reject(e);
                }

                if (starObject.body.address === walletAddress) {
                  stars.push(starObject);
                }
            }).on('error', function (err) {
                reject(err);
            }).on('close', function () {
                resolve(stars);
            });
        });

    };

    validateBlock(height) {
        let _this = this;
    };

    validateChain() {
        let _this = this;
    };

    // Boilerplate provided test method to test validation methods
    _modifyBlock(height, block) {
        let self = this;

        return new Promise((resolve, reject) => {
            self.db.addLevelDBData(height, JSON.stringify(block).toString())
            .then((blockModified) => {
                resolve(blockModified);
            })
            .catch((err) => { console.log(err); reject(err)});
        });
    };

};

module.exports.Blockchain = Blockchain;

