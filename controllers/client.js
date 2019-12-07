const CLIENT_ID = process.env.CLIENT_ID || 323173717968683019;
const CLIENT_SECRET = process.env.CLIENT_SECRET;
const redirect = encodeURIComponent('http://localhost:3000/client/dashboard');

function login(req, res) {
    res.redirect(`https://discordapp.com/api/oauth2/authorize?client_id=${CLIENT_ID}&redirect_uri=${redirect}&response_type=code&scope=guilds`);
}

module.exports = {
    login: login
}
