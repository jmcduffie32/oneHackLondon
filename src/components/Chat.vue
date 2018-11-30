<template>
  <div class="Vlt-card">
    <button class="Vlt-btn Vlt-btn--primary Vlt-btn--app"
            v-if="isVideoEnabled"
            @click="inviteToVideo()">
      <svg><use xlink:href="/icons/volta-icons.svg#Vlt-icon-video"></use></svg>
      Invite to video chat
    </button>

    <div class="Vlt-table">
      <table>
        <tbody>
          <tr v-for="message in history" v-bind:key="message.text">
            <td>{{message.text}}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="Vlt-form__element">
      <div class="Vlt-composite">
        <div class="Vlt-input">
          <input type="text" id="input-appended-icon-button"
                 placeholder="Type your message"
                 v-model="message"
                 @keyup.enter="sendMessage(message)" />
        </div>
        <div class="Vlt-composite__append">
          <button class="Vlt-btn Vlt-btn--icon" @click="sendMessage(message)">
            <svg><use xlink:href="icons/volta-icons.svg#Vlt-icon-send"></use></svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
const axios = require('axios');
const _ = require('lodash');
const SERVICE_URL = '/test';

export default {
  name: 'Chat',
  data: function () {
    return {
      message: '',
      history: [{
        text: 'Hello World!'
      }],
    }
  },
  props: ['selectedContacts'],
  methods: {
    sendMessage: function (message) {
      this.history = [...this.history, { text: message }];
      this.message = '';
      this.selectedContacts.forEach((contact) => {
        axios.post(SERVICE_URL, {
          sendMessage: contact.name.toLowerCase(),
          message: message
        }).then((resp) => {
        }) ;
      });
    },
    inviteToVideo() {
      const message = "You've been invited to a video chat. Follow this link to join: http://10.122.102.69:8080/#/oneHackLondon"
      this.selectedContacts.forEach((contact) => {
        axios.post(SERVICE_URL, {
          sendMessage: contact.name.toLowerCase(),
          message: message
        }).then((resp) => {
        }) ;
      });
    }
  },
  computed: {
    isVideoEnabled: function() {
      return this.selectedContacts.length &&
        this.selectedContacts.filter(contact => !contact.supportsVideo).length === 0;
    }
  },
  created: function() {
    const contacts = this.selectedContacts;
    this.interval = setInterval(function () {
      console.log(contacts);
      axios.post(SERVICE_URL, {
        getUsers: true
      }).then((resp) => {
        if (resp && resp.data && resp.data.users) {
          const newMessages = resp.data.users
                .filter(user => user.message)
                .map((user) => {
                  return { text: user.user + ': ' + user.message }
                });
          this.history = _.uniqBy([...this.history, ...newMessages], 'text');
          console.log(history);
        }
      });
    }.bind(this), 2000)
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
