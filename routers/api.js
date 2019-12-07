const clientController = require('../controllers/client');

module.exports = function (fastify, opts, done) {
    fastify.get('/login', clientController.login);
    done();
}
