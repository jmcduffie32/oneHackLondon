const express = require('express');
const proxy = require('http-proxy-middleware');
const app = express();
const port = process.env.PORT || 3000;

app.get('/openTok.env.json', function (req, res) {
  const apiKey = process.env.API_KEY;
  const sessionId = process.env.SESSION_ID;
  const token = process.env.TOKEN;

  // Respond to the client
  res.json({
    "credentials": {
      "apiKey": apiKey,
      "sessionId": sessionId,
      "token": token
    }
  });
});
app.use('/test', proxy({
  target: "https://tfy254ekqf.execute-api.eu-west-1.amazonaws.com/test",
  changeOrigin: true
}));
app.use(express.static('dist'));
app.listen(port, () => console.log(`Example app listening on port ${port}!`));
