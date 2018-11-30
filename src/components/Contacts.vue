<template>
  <div class="Vlt-card">
    <h3>Contacts</h3>
    <div class="Vlt-table">
      <table>
        <tbody>
          <tr  v-for="contact in contacts" v-bind:key="contact.id">
            <td>
              {{contact.name}}
            </td>
            <td class="Vlt-table__cell--nowrap">
              <button @click="toggleContactSelected(contact)"
                      v-if="!contact.isSelected"
                      class="Vlt-btn Vlt-btn--tertiary Vlt-btn--icon">
                <svg><use xlink:href="/icons/volta-icons.svg#Vlt-icon-check"></use></svg>
              </button>
              <button @click="toggleContactSelected(contact)"
                      v-if="contact.isSelected"
                      class="Vlt-btn Vlt-btn--tertiary Vlt-btn--icon">
                <svg><use xlink:href="/icons/volta-icons.svg#Vlt-icon-cross"></use></svg>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
const axios = require('axios');
import store from '../store/store';

export default {
  name: 'Contacts',
  data: function () {
    return {
      videoCallEnabled: false,
      contacts: [
        {
          name: "John",
          supportsVideo: true,
          isSelected: false
        },
        {
          name: 'Michael',
          supportsVideo: true,
          isSelected: false
        },
        {
          name: 'FB Contact',
          supportsVideo: false,
          isSelected: false
        },
        {
          name: 'SMS Contact',
          supportsVideo: false,
          isSelected: false
        },
      ]
    }
  },
  props: ['selectedContacts'],
  methods: {
    toggleContactSelected: function(contact) {
      contact.isSelected = !contact.isSelected;
      const selectedContacts = this.contacts.filter(contact => contact.isSelected);
      this.videoCallEnabled = selectedContacts.length &&
        selectedContacts.filter(contact => !contact.supportsVideo).length === 0;
      this.$emit('contacts-updated', selectedContacts);
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
