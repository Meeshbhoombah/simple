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

        // check if any blocks have been created
        var height = await _this.getBlockHeight();
        if (height !== 0) {
            return 
        } else {
            let genesisBlock = new Block.Block('04/20/2017 - Rohan on brink of bail out from School')
            console.log(genesisBlock) 
        }
    }

    // Get block height, it is auxiliar method that return the height of the blockchain
    async getBlockHeight() {
        let _this = this;

        return await _this.db.getBlocksCount();
    }

    // Add new block
    addBlock(block) {
        // Add your code here
    }

    // Get Block By Height
    getBlock(height) {
        // Add your code here
    }

    // Validate if Block is being tampered by Block Height
    validateBlock(height) {
        // Add your code here
    }

    // Validate Blockchain
    validateChain() {
        // Add your code here
    }

    // Utility Method to Tamper a Block for Test Validation
    // This method is for testing purpose
    _modifyBlock(height, block) {
        let self = this;
        return new Promise( (resolve, reject) => {
            self.bd.addLevelDBData(height, JSON.stringify(block).toString()).then((blockModified) => {
                resolve(blockModified);
            }).catch((err) => { console.log(err); reject(err)});
        });
    }
   
}

module.exports.Blockchain = Blockchain;
