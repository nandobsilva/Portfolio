var express = require('express');
var router = express.Router();

/* GET API  - "/stocks" page. */
router.get('/', function(req, res, next) {
  return res.redirect('/docs');
});
router.get('/:id', function(req, res, next) {
  return res.status(404).json({"error": true, "message": "Not Found"});
});
module.exports = router;
