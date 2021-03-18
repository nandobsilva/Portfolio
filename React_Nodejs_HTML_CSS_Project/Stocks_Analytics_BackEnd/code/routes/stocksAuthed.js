const express = require('express');
const router = express.Router();
const options = require('../knexfile.js');
const knex = require ('knex')(options);
const jwt = require('jsonwebtoken');

/* GET API page. */
const message400_01 = {"error":true,"message":"Request on /stocks must include symbol as path parameter, or alternatively you can hit /stocks/symbols to get all symbols"};
const message400_02 = {"error":true,"message":"Stock symbol incorrect format - must be 1-5 capital letters"};
const message400_03 = {"error":true,"message":"Parameters allowed are 'from' and 'to', example: /stocks/authed/ALL?from=2020-03-15"};
const message400_04 = {"error":true,"message":"From date cannot be parsed by Date.parse()"};
const message400_05 = {"error":true,"message":"To date cannot be parsed by Date.parse()"};
const message400_06 = {"error":true,"message":"Invalid date in the parameter 'from' or 'to'"};
const message404 = {"error": true, "message": "No entries available for query symbol for supplied date range"};
const message500 = {"error": true, "message": "Error executing MySQL query - Query is invalid"}


/* GET API - "stocks/authed" page. */
router.get('/', function(req, res, next) {
    console.log("Bad request '400' on /stocks: Invalid query parameter");
    return res.status(400).json(message400_02);
});

/* GET API "stocks/authed"/:symbol" page. */
router.get('/:symbol', function(req, res, next) {

    //-------------------------------------------------------------------------------------------
    // Authorization - JWT
    //-------------------------------------------------------------------------------------------
    const authorization = req.headers.authorization;
    let token = null;
    if(authorization && authorization.split(" ").length === 2){
        token = authorization.split(" ")[1];
    }
    else{
        console.log("Unauthorized user");
        return res.status(403).json({"error": true, "message": "Authorization header not found"});
    }
    try{
        const decoded = jwt.verify(token, 'cometa')
        if(decoded.exp > Date.now()){
            return res.status(403).json({"error": true, "message": "Authorization failed - Token has expired"}); 
        }

    }catch(e){
        console.log("Error: " + e)
        return res.status(500).json({"error": true, "message" : "Server authorization error"})
    }
    
    //---------------------------------------------------------------------------------------------
    // Variables used by the API
    //---------------------------------------------------------------------------------------------
    const parameter = req.params.symbol;
    var isParameterValid = true;
    const queryLength = Object.keys(req.query).length;
    const hasQuery = (queryLength !== 0);
    var key = "";               
    var parameterQuery = ""     
    var hasFrom = false;
    var hasTo = false;
    var dateFrom ="";
    var dateTo ="";

    //---------------------------------------------------------------------------------------------
    // Query parameters check
    //---------------------------------------------------------------------------------------------
    if(hasQuery){
        for (const item in req.query){
            let key = item;
            let parameterQuery = req.query[item];
            if(key === "from") { 
                hasFrom = true;
                dateFrom = parameterQuery;
                let date = Date.parse(parameterQuery);
                console.log("Date test: " + date);
                if(!date){
                    console.log("Bad request '400' on /stocks/authed/:symbol : Invalid query parameter");
                    return res.status(400).json(message400_04);
                }
            }
            if(key === "to"){
                hasTo = true;
                dateTo = parameterQuery;
                let date = Date.parse(parameterQuery);
                if(!date){
                    console.log("Bad request '400' on /stocks/authed/:symbol : Invalid query parameter");
                    return res.status(400).json(message400_05);
                }
            }  
        }
    }

    //---------------------------------------------------------------------------------------------
    // Parameter validation
    //---------------------------------------------------------------------------------------------
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
    // Send result to the client if parameters are invalids
    if (parameter.length > 5 || !isParameterValid ){
        console.log("Bad request '400' on /stocks/authed/:symbol : Invalid query parameter")
        return res.status(400).json(message400_02);
    }

    //---------------------------------------------------------------------------------------------
    // If there is no query parameters "from" or "to"
    //---------------------------------------------------------------------------------------------
    if(queryLength === 0){  
        knex.select('*').from('stocks').where('symbol', '=', parameter).andWhereRaw("timestamp ="+
        " (select MAX(timestamp) from stocks where symbol ='"+ parameter+"')")
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

    //---------------------------------------------------------------------------------------------
    // Invalid parameters "from" and "to"
    //---------------------------------------------------------------------------------------------
    // If there are more than 2 query parameters 
    if(queryLength > 2 ){
        console.log("Bad request '400' on /stocks/authed/:symbol : Invalid query parameter")
        return res.status(400).json(message400_03);
    }
    // If there are 2 query parameters but one or both are invalid
    if(queryLength === 2 && (hasTo === false || hasFrom === false)){
        console.log("Bad request '400' on /stocks/authed/:symbol : Invalid query parameter")
        return res.status(400).json(message400_03);
    }
    // If there are 1 query parameters but it is invalid
    if(queryLength === 1 && (hasTo === false && hasFrom === false)){
        console.log("Bad request '400' on /stocks/authed/:symbol : Invalid query parameter")
        return res.status(400).json(message400_03);
    }

    //---------------------------------------------------------------------------------------------
    // Invalid parameters date "from" or "to"
    //---------------------------------------------------------------------------------------------
    function  isDateValid (param, from, to ) {
        return new Promise((resolve, reject) => {
            knex.select('*').from('stocks')
            .where('symbol', '=', param)
            .andWhere('timestamp', '>=', from) 
            .andWhere('timestamp', '<=', to) 
            .then((rows)=>{
                resolve(rows);
            })
            .catch((err)=>{ 
                reject(false);
            })
        })
    }

    function  isFromValid (param, from ) {
        return new Promise((resolve, reject) => {
            knex.select('*').from('stocks')
            .where('symbol', '=', param)
            .andWhere('timestamp', '>=', from) 
            .then((rows)=>{
                resolve(rows);
            })
            .catch((err)=>{ 
                reject(false);
            })
        })
    }

    function  isToValid (param, to ) {
        return new Promise((resolve, reject) => {
            knex.select('*').from('stocks')
            .where('symbol', '=', param)
            .andWhere('timestamp', '<=', to) 
            .then((rows)=>{
                resolve(rows);
            })
            .catch((err)=>{ 
                reject(false);
            })
        })
    }

    //---------------------------------------------------------------------------------------------
    // Valid parameters date "from" or "to"
    //--------------------------------------------------------------------------------------------- 
    // If it has "from" and "to"
    if(hasTo && hasFrom){
        isDateValid(parameter, dateFrom, dateTo)
        .then((rows)=> {
            const data = rows;
            if(data === undefined || data.length === 0){
                return res.status(404).json(message404);
            }else{
                return res.status(200).json(data);
            }
        })
        .catch(()=>{
            console.log("Bad request '400' on /stocks/authed/:symbol : Invalid date 'from' or 'to'");
            return res.status(400).json(message400_06);
        });
    }
    
    // If it has just parameter "from" 
    if(hasFrom && !hasTo){
        
        isFromValid(parameter, dateFrom)
        .then((rows)=> {
            const data = rows;
            if(data === undefined || data.length === 0){
                return res.status(404).json(message404);
            }else{
                return res.status(200).json(data);
            }
        })
        .catch(()=>{
            console.log("Bad request '400' on /stocks/authed/:symbol : Invalid date 'from' or 'to'");
            return res.status(400).json(message400_06);
        });  
    }

    // If it has just parameter "to"
    if(hasTo && !hasFrom){
        isToValid(parameter, dateTo)
        .then((rows)=> {
            const data = rows;
            if(data === undefined || data.length === 0){
                return res.status(404).json(message404);
            }else{
                return res.status(200).json(data);
            }
        })
        .catch(()=>{
            console.log("Bad request '400' on /stocks/authed/:symbol : Invalid date 'from' or 'to'");
            return res.status(400).json(message400_06);
        });
    }

});
module.exports = router;