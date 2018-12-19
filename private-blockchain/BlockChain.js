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
            
        let genesisBlock = new Block.Block('20/April/2017 - Meesh on brink from bailout from LSD.');
        _this.addBlock(genesisBlock)
        .then((block) => {
            console.log(block);
        })
        .catch((err) => {
            console.log(err);
        })
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
        block.time = new Date().getTime();

        let _this = this;
        return _this.getBlockHeight()
        .then(async (blockHeight) => {
            console.log(blockHeight)
            block.height = blockHeight;

            // check that previous block is not Genesis
            if (block.height !== 0) {
                var previousBlock = block.height - 1;
                await _this.db.get(previousBlock)
                .then((prevBlock) => {
                    block.prevBlockHash = SHA256(JSON.stringify(prevBlock)).toString(); 
                })
                .catch((err) => {
                    return err; 
                })
            } 

            block.hash = SHA256(JSON.stringify(block)).toString();

            return new Promise(async (resolve, reject) => {
                await _this.db.put(block.height, block) 
                .then(() => {
                    resolve(block);
                })
                .catch((err) => {
                    reject(err);
                })
            });
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

