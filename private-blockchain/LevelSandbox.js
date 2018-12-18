/* ===== Persist data with LevelDB ==================
|  Learn more: level: https://github.com/Level/level |
/===================================================*/

const level = require('level');
const chainDB = './chaindata';

class LevelSandbox {
    constructor() {
        this.db = level(chainDB);
    }

    // Add data to levelDB with key and value (Promise)
    addLevelDBData(key, value) {
        let _this = this;
        return new Promise((resolve, reject) => {
            _this.db.put(key, value, function(err) {
                if (err) {
                    reject(err);
                } else {
                    resolve();  
                }
            });
        });
    }

    // Get data from levelDB with key (Promise)
    getLevelDBData(key){
        let _this = this;
        return new Promise((resolve, reject) => {
            _this.db.get(key, function(err, result) {
                if (err) {
                    reject(err); 
                } else {
                    resolve(result);
                }
            });
        });
    }

    // Method that return the height
    getBlocksCount() {
        let _this = this;
   
        var i = 0;

        return new Promise((resolve, reject) => {
            _this.db.createReadStream()
                .on('error', (err) => {
                    reject(err);
                })
                .on('data', (data) => {
                    i++;
                })
                .on('close', (data) => {
                    resolve(i);
                })
        });
    }
}

module.exports.LevelSandbox = LevelSandbox;

