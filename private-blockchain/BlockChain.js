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
        .then((height) => {
            if (height !== 0) {
                return Error('Pre-existing Blocks: Block Height is ' + String(height));
            } else {
                let genesisBlock = new Block.Block('Fiat is dead. Long live USD Coupons.');
                genesisBlock.time = new Date().getTime();
                console.log(genesisBlock);
                //_this.addBlock(genesisBlock);
            }
        })
        .catch((err) => {
            console.log(err);
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

        return new Promise((resolve, reject) => {
        })
    };

    getBlock(height) {
        let _this = this;
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

        return new Promise( (resolve, reject) => {
            self.db.addLevelDBData(height, JSON.stringify(block).toString())
            .then((blockModified) => {
                resolve(blockModified);
            })
            .catch((err) => { console.log(err); reject(err)});
        });
    };

};

module.exports.Blockchain = Blockchain;

