const express = require('express');
const proxy = require('http-proxy-middleware');
const app = express();
const port = process.env.PORT || 3000;

const Nexmo = require('nexmo');

const users = {
  jon: {
    number: '4789936988',
    fbId: ''
  },
  michael: {
    number: '',
    fbId
  }
};

const nexmo = new Nexmo({
  apiKey: process.env.NEXMO_API_KEY,
  apiSecret: process.env.NEXMO_API_SECRET,
  applicationId: process.env.NEXMO_APP_ID,
  privateKey: process.env.NEXMO_PRIVATE_KEY,
}, options);

app.get('/openTok.env.json', function (req, res) {
  const apiKey = process.env.API_KEY;
  const sessionId = process.env.SESSION_ID;
  const token = process.env.TOKEN;

  res.json({
    "credentials": {
      "apiKey": apiKey,
      "sessionId": sessionId,
      "token": token
    }
  });
});

app.post('/sendMessage', function (req, res) {
  const message = req.body.message;

  nexmo.dispatch.create("failover", [
    {
      "from": { "type": "messenger", "id": "FB_SENDER_ID" },
      "to": { "type": "messenger", "id": "FB_RECIPIENT_ID" },
      "message": {
        "content": {
          "type": "text",
          "text": message
        }
      },
      "failover":{
        "expiry_time": 600,
        "condition_status": "delivered"
      }
    },
    {
      "from": {"type": "sms", "number": "12013408883"},
      "to": { "type": "sms", "number": "14789936988"},
      "message": {
        "content": {
          "type": "text",
          "text": message
        }
      }
    },
    (err, data) => { console.log(data.dispatch_uuid); }
  ]);
});

app.post('/status', function (req, res) {
  console.log(req.body);
});

app.post('/inbound', function (req, res) {
  console.log(req.body);
});

app.use('/test', proxy({
  target: "https://tfy254ekqf.execute-api.eu-west-1.amazonaws.com/test",
  changeOrigin: true
}));
app.use(express.static('dist'));
app.listen(port, () => console.log(`Example app listening on port ${port}!`));
