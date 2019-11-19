const fastify = require('fastify')();
const path = require('path');

fastify.register(require('fastify-static'), {
  root: path.join(__dirname, 'dist')
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
