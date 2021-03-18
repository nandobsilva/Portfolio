
const express = require('express');
const router = express.Router();
const options = require('../knexfile.js');
const knex = require ('knex')(options);
const bcrypt = require('bcrypt');




/* GET users listing. */
router.get('/', function(req, res, next) {
    return res.status(404).json({
        'error': true,
        'message': "Not Found"
    })
});

/* POST API  - "/stocks" page. */
router.post('/', function(req, res, next) {

    const email    = req.body.email;
    const password = req.body.password;

    // Verify body
    if(!email || !password){
        return res.status(400).json({
            'error': true,
            'message': "Request body incomplete - email and password needed"
        })
    }
    
    // Verify if email already exist 
    function  doesEmailExist(email) {
        return new Promise((resolve, reject) => {
            knex.select("*").from('users').where('email', '=', email)
            .then((rows) =>{
                const data = rows;
                if(data.length === 0){
                    resolve(false);
                }
                else{
                    resolve(true);
                }
            })
            .catch((err) =>{
                console.log("Error: " + err);
                reject(err);
            })
        })
    }

    // Process request and return status to the client
    if(email && password){
        doesEmailExist(email)
        .then((result) =>{
            //console.log("Email: " + email + ", Password: " + password);
            if(result === true){
                //console.log("User already exist");
                return res.status(409).json({"error": true, "message": "User already exists"});
            }
            else{
                //console.log("User does not exist");
                const saltRounds = 10;
                let hash = bcrypt.hashSync(password,saltRounds);
                hash = hash;
                console.log("Hash: " + hash);
                knex('users').insert({email: email, password: hash})
                .then (()=> {
                    return res.status(201).json({"success": true, "message": "User created"});
                })
                .catch((error)=>{
                    console.log("Error: " + error);
                    return res.status(500).json({"success": false, "message": "Internal server error"})
                })
            }
        })
        .catch((err) =>{
            console.log("Error: " + err);
            return res.status(500).json({"success": false, "message": "Internal server error"})
        })

    }  

});


module.exports = router;