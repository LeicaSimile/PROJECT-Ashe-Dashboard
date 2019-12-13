const fastify = require('fastify')();
const path = require('path');

fastify.register(require('fastify-static'), {
    root: path.join(__dirname, 'dist', 'projectashe')
});

fastify.get('/*', function (req, reply) {
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
