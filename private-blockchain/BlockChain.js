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
                let genBlock = new Block.Block('20/April/2017 - Meesh on brink from bailout from School.');

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
                await _this.db.get(previousBlock)
                .then((prevBlock) => {
                    // check's integirty
                    console.log(prevBlock);
                    console.log(SHA256(prevBlock).toString());
                    block.prevBlockHash = SHA256(prevBlock).toString(); 
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

