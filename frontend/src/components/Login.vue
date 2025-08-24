<template>
  <div class="login">
    <h2>Login</h2>
    <form @submit.prevent="handleLogin">
      <input v-model="email" type="email" placeholder="Email" required />
      <br /><br />
      <input v-model="password" type="password" placeholder="Password" required />
      <br /><br />
      <button type="submit">Login</button>
    </form>
    <p>
      Don’t have an account?
      <button @click="$emit('switchView', 'register')">Register</button>
    </p>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import axios from "axios";

const email = ref("");
const password = ref("");

const handleLogin = async () => {
  try {
    const res = await axios.post("http://localhost:4000/login", {
      email: email.value,
      password: password.value,
    });
    alert("Login successful!");
    console.log(res.data);
  } catch (err: any) {
    alert(err.response?.data?.error || "Login failed");
  }
};
</script>
