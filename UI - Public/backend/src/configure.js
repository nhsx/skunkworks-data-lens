const cookieParser = require('cookie-parser')
const bodyParser = require('body-parser')
const session = require('express-session');
const passport = require('passport');
const fileUpload = require('express-fileupload');

const cors = require('cors')

module.exports = app => {
  app.use(cors());
  app.use(bodyParser.json())
  app.use(bodyParser.urlencoded({extended: false}));
  app.use(cookieParser());
  app.use(session({
    secret: process.env.PASSPORT_SECRET,
    resave: true,
    saveUninitialized: true,
    cookie : { secure:false, httpOnly: true, maxAge: 2419200000 } /// maxAge in milliseconds
  }));
  app.use(fileUpload({
    createParentPath: true
  }));

  app.use(passport.initialize());
  app.use(passport.session())
}