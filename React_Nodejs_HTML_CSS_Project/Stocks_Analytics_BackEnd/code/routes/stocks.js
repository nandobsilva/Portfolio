var express = require('express');
var router = express.Router();
const options = require('../knexfile.js');
const knex = require ('knex')(options);

/* GET API page. */
const message400_01 = {"error":true,"message":"Request on /stocks must include symbol as path parameter, or alternatively you can hit /stocks/symbols to get all symbols"};
const message400_02 = {"error":true,"message":"Stock symbol incorrect format - must be 1-5 capital letters"};
const message404 = {"error": true, "message": "No entry for symbol in stocks database"};
const message500 = {"error": true, "message": "Error executing MySQL query - Query is invalid"}
const message400_03={"error": true, "message": "Date parameters only available on authenticated route /stocks/authed"}



/* GET API  - "/stocks" page. */
router.get('/', function(req, res, next) {
    console.log("Bad request '400' on /stocks: Invalid query parameter");
    return res.status(400).json(message400_01);
});

/* GET API "/stocks/:symbol" page. */
router.get('/:symbol', function(req, res, next) {
    const parameter = req.params.symbol;
    var isParameterValid = true;
    console.log("Parameter: " + parameter)

    //If has query parameters
    const queryLength = Object.keys(req.query).length;
    const hasQuery = (queryLength !== 0);
    console.log("Has query: " + hasQuery)
    if(hasQuery){
        console.log("Bad request '400' on /stocks/:symbol : Invalid query parameter")
        return res.status(400).json(message400_03);
    }


    // Validate parameter entered
    for(let i = 0; i < parameter.length ; i++){
        let character = parameter[i];
        if(!isNaN(character * 1)){
            isParameterValid = false;
            break
        }
        if(character === character.toLowerCase()){
            isParameterValid = false;
            break
        }
        if(character === undefined){
            isParameterValid = false;
            break
        }
    }

    // Send result to the client
    if (parameter.length > 5 || !isParameterValid ){
        console.log("Bad request '400' on /stocks/:symbol : Invalid query parameter")
        return res.status(400).json(message400_02);
    }
    else {
   
        //knex.select('*').from('stocks').where('symbol', '=', parameter).orderBy('timestamp', 'desc')
        knex.select('*').from('stocks').where('symbol', '=', parameter).andWhereRaw("timestamp = (select MAX(timestamp) from stocks where symbol ='"+ parameter+"')")
        //knex.max('timestamp').from('stocks').where('symbol', '=', parameter)
        .then((rows)=> {
            const data = rows[0];
            if(data === undefined){
                return res.status(404).json(message404);
            }else{
                return res.status(200).json(data);
            }
        })
        .catch((err)=> {
            console.log(err);
            return res.status(500).json(message500);
        });




    }

});
module.exports = router;