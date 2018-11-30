const express = require('express');
const app = express();
const port = 3000;

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
app.use(express.static('dist'));
app.listen(port, () => console.log(`Example app listening on port ${port}!`));
