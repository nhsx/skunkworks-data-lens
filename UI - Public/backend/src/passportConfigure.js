const LdapStrategy = require('passport-ldapauth');
const passport = require('passport');

module.exports = app => {
    const {
        LDAP_URL,
        LDAP_BIND_DN,
        LDAP_BIND_PASSWORD,
        LDAP_SEARCH_BASE,
        LDAP_SEARCH_FILTER,
    } = process.env;

    const LDAP_OPTS = {
        server: {
            url: LDAP_URL,
            bindDN: LDAP_BIND_DN,
            bindCredentials: LDAP_BIND_PASSWORD,
            searchBase: LDAP_SEARCH_BASE,
            searchFilter: LDAP_SEARCH_FILTER,
        }
    }

    passport.serializeUser(function(user, done) {
        done(null, user);
    });
    
    passport.deserializeUser(function(user, done) {
        done(null, user);
    });
    
    passport.use('ldap-login', new LdapStrategy(LDAP_OPTS, function(user, done) {
        done(null, user);
    }));
}