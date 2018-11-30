<template>
  <div id="app">
    <Contacts :selectedContacts="selectedContacts"
              v-on:contacts-updated="setSelectedContacts($event)"/>
    <Chat :selectedContacts="selectedContacts"/>
  </div>
</template>

<script>
import Chat from './components/Chat.vue'
import Contacts from './components/Contacts.vue'

export default {
  name: 'app',
  data: function () {
    return {
      selectedContacts: []
    }
  },
  components: {
    Chat,
    Contacts
  },
  methods: {
    setSelectedContacts: function(contacts) {
      this.selectedContacts = contacts;
    }
  }
}
</script>

<style>
</style>
