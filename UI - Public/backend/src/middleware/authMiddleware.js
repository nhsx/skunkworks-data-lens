module.exports = (req,res,next) => {
    const { BASE_URL } = require('../config')
    if(req.isAuthenticated()){
        next();
    } else {
        res.redirect(`${BASE_URL}/auth/login`);
    }
}