const fastify = require('fastify')();
const path = require('path');
const apiRouter = require('./routers/api');

fastify.register(require('fastify-static'), {
    root: path.join(__dirname, 'dist', 'projectashe')
});
fastify.register(apiRouter, {prefix: '/api'});

fastify.get('/', function (req, reply) {
    reply.sendFile('index.html');
});

const start = async () => {
    try {
        await fastify.listen(process.env.PORT || 3000);
    } catch (err) {
        fastify.log.error(err);
        process.exit(1);
    }
}
start();
