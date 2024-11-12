<template>
  <div>
    <h2>Register</h2>
    <form @submit.prevent="handleRegister">
      <div>
        <label for="username">Username:</label>
        <input type="text" v-model="username" id="username" required />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" v-model="password" id="password" required />
      </div>
      <button type="submit">Register</button>
    </form>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: '',
      message: ''
    };
  },
  methods: {
    async handleRegister() {
      try {
        const response = await axios.post('http://127.0.0.1:5001/api/register', {
          username: this.username,
          password: this.password
        });
        this.message = response.data.message;
      } catch (error) {
        this.message = error.response.data.message;
      }
    }
  }
};
</script>
