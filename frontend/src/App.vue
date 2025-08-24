<template>
  <div id="app">
    <component :is="currentView" @switchView="switchView" />
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import Login from "./components/Login.vue";
import Register from "./components/Register.vue";

const currentView = ref(Login);

const switchView = (view: string) => {
  currentView.value = view === "login" ? Login : Register;
};
</script>
