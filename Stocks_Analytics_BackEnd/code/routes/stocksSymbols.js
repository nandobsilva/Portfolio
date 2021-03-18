var express = require('express');
var router = express.Router();
const options = require('../knexfile.js');
const knex = require ('knex')(options);


/* GET API - "/stocks/symbols" page. */
router.get('/', function(req, res) {
  const queryLength = Object.keys(req.query).length;
  //console.log("Query length: " + queryLength)

  var key = ""; //Object.keys(req.query)[0];
  var parameter = "" //Object.keys(req.query[key]);
  const hasQuery = (queryLength !== 0);


  if(hasQuery){
    for (const item in req.query){
      key = item;
      parameter = req.query[item];
    }
    //console.log("Key: " + key);
    //console.log("Parameter: " + parameter);

    if(queryLength > 1 || key !== "industry"){
        console.log("Bad request '400' on /stocks/symbols: Invalid query parameter");
        return res.status(400).json({"error": true, "message": "Invalid query parameter: only 'industry' is permitted"});
    }else{
          knex.distinct().from('stocks').select('name', 'symbol', 'industry').where('industry', 'like', '%'+parameter+'%')
            .then((rows)=> {
              var data = rows;
              if(data.length === 0){
                res.status(404).json({"error": true, "message": "Industry sector not found"});
              }else{
                res.status(200).json(data);
              }
            })
            .catch((err)=> {
              console.log(err);
              res.json({"error": true, "message": "Error executing MySQL query"})
            }
          );   
      }
  }
  else{
    knex.distinct().from('stocks').select('name', 'symbol', 'industry')
      .then((rows)=> {
        var data = rows;
        res.status(200).json(data)
      })
      .catch((err)=> {
        console.log(err);
        res.json({"error": true, "message": "Error executing MySQL query"})
      });
  }
});

module.exports = router;