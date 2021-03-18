const express = require('express');
const router = express.Router();
const options = require('../knexfile.js');
const knex = require ('knex')(options);
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');




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

    // Verify body of the request
    if(!email || !password){
        return res.status(400).json({
            'error': true,
            'message': "Request body invalid - email and password are required"
        })
    }
    
    // Process request and return status to the client
    if(email && password){
        console.log("Email: " + email +", Password: " + password);
        knex.select('*').from('users').where('email', '=', email)
        .then((users)=>{
            if(users.length === 0){
                console.log("User does not exist");
                return res.status(401).json({"error": true, "message":"Incorret email or password"});
            }
            // Validate password
            const user = users[0];
            return bcrypt.compare(password, user.password)
        })
        .then((match)=>{
            if(!match){
                console.log("Password does not match")
                return res.status(401).json({"error": true, "message":"Incorret email or password"});
            }else{
                console.log("Password match")
                // Create and return token to the client
                const secretKey = "cometa";
                const expires = 60 * 60 * 24 // One day
                const exp = Math.floor(Date.now()/1000) + expires;
                const token = jwt.sign({email, exp }, secretKey);
                //return res.status(200).json({   "token_type": "Bearer", token, expiresIn });
                return res.status(200).json({ token, expires_in: expires,  "token_type": "Bearer" });
            }

        })

    }  

});
module.exports = router