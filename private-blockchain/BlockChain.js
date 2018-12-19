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

    async generateGenesisBlock() {
        let _this = this;

        let height = await _this.getBlockHeight()
        if (height !== 0) {
            return Error('Pre-existing Blocks: Block Height is ' + String(height))
        } else {
            let genesisBlock = new Block.Block('Fiat is dead. Long live Fiat Coupons.');
            console.log(genesisBlock);
            //_this.addBlock(genesisBlock);
        }
    };

    async getBlockHeight() {
        let _this = this;

        await _this.db.getBlocksCount()
        .then((height) => {
            console.log(height)
            return height
        })
        .catch((err) => {
            return err 
        });
    };

    addBlock(block) {
        let _this = this;
    }

    getBlock(height) {
        let _this = this;
        // Add your code here
    }

    validateBlock(height) {
        let _this = this;
        // Add your code here
    }

    validateChain() {
        let _this = this;
        // Add your code here
    }

    // Boilerplate provided test method to edit block
    _modifyBlock(height, block) {
        let self = this;

        return new Promise( (resolve, reject) => {
            self.db.addLevelDBData(height, JSON.stringify(block).toString())
            .then((blockModified) => {
                resolve(blockModified);
            })
            .catch((err) => { console.log(err); reject(err)});
        });
    }
   
}

module.exports.Blockchain = Blockchain;
