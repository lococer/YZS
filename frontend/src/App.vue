<script>
export default {
  name: 'App'
};
</script>

<template>
  <div id="app">
    <router-link to="/">Home</router-link> |
    <router-link to="/movies">Movies</router-link>
    <router-view />
  </div>
</template>

<style>
</style>
