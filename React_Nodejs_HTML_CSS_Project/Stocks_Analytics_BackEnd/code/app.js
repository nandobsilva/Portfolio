const createError     = require('http-errors');
const express         = require('express');
const path            = require('path');
const cookieParser    = require('cookie-parser');
const logger          = require('morgan');
const swaggerUI       = require('swagger-ui-express');
const swaggerDocument = require('./docs/swaggerStocks.json');
const helmet          = require('helmet');
const cors            = require('cors');

const indexRouter         = require('./routes/index');
const stocksSymbolsRouter = require('./routes/stocksSymbols');
const stocksRouter        = require('./routes/stocks');
const stocksAuthedRouter  = require('./routes/stocksAuthed');
const userRegisterRouter  = require('./routes/userRegister');
const userLoginRoute      = require('./routes/userLogin');

const fs = require('fs');
const https = require('https');
const privateKey = fs.readFileSync('./sslcert/cert.key', 'utf8');
const certificate = fs.readFileSync('./sslcert/cert.pem', 'utf8');
const credentials = {
  key: privateKey,
  cert: certificate
}

var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');
app.use(helmet());
app.use(logger('dev'));
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));


app.use('/stocks/authed', stocksAuthedRouter);
app.use('/stocks/symbols', stocksSymbolsRouter);
app.use('/stocks', stocksRouter);
app.use('/user/login', userLoginRoute);
app.use('/user/register', userRegisterRouter);
app.use('/docs', swaggerUI.serve, swaggerUI.setup(swaggerDocument));
app.use('/', indexRouter);

//app.use('/', indexRouter);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;
