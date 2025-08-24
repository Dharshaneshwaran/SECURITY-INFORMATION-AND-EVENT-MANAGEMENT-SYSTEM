<template>
  <div class="register">
    <h2>Register</h2>
    <form @submit.prevent="handleRegister">
      <input v-model="email" type="email" placeholder="Email" required />
      <br /><br />
      <input v-model="password" type="password" placeholder="Password" required />
      <br /><br />
      <button type="submit">Register</button>
    </form>
    <p>
      Already have an account?
      <button @click="$emit('switchView', 'login')">Login</button>
    </p>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import axios from "axios";

const email = ref("");
const password = ref("");

const handleRegister = async () => {
  try {
    const res = await axios.post("http://localhost:4000/register", {
      email: email.value,
      password: password.value,
    });
    alert("Registration successful!");
    console.log(res.data);
  } catch (err: any) {
    alert(err.response?.data?.error || "Registration failed");
  }
};
</script>
