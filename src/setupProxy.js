const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(createProxyMiddleware('/getOne', { target: 'http://localhost:5000/' }));
};
