/* ===== Persist data with LevelDB ==================
|  Learn more: level: https://github.com/Level/level |
/===================================================*/

const level = require('level');
const chainDB = './chaindata';

class Wrapper {
    constructor() {
        this.db = level(chainDB);
    }

    put(key, value) {
        let _this = this;

        var block = JSON.stringify(value);

        return new Promise((resolve, reject) => {
            _this.db.put(key, block, function(err) {
                if (err) {
                    reject(err);
                } else {
                    resolve();  
                }
            });
        });
    }

    get(key) {
        let _this = this;

        return new Promise((resolve, reject) => {
            _this.db.get(key, function(err, result) {
                if (err) {
                    reject(err); 
                } else { 
                    var block = JSON.parse(result);
                    resolve(block);
                }
            });
        });
    }

    getBlocksCount() {
        let _this = this;
   
        var i = 0;
        return new Promise((resolve, reject) => {
            // Streams all underlying entities from store (start to end)
            _this.db.createReadStream()
            .on('data', (data) => {
                i++;
            })
            .on('close', (data) => {
                resolve(i);
            })
            .on('error', (err) => {
                reject(err);
            });
        });
    }
}

module.exports.Wrapper = Wrapper;

