<script>
// TODO 设置导航
// import { h, ref } from 'vue';
// import { MailOutlined, AppstoreOutlined, SettingOutlined } from '@ant-design/icons-vue';
// const current = ref(['mail']);
// const items = ref([
//   {
//     key: 'mail',
//     icon: () => h(MailOutlined),
//     label: 'Navigation One',
//     title: 'Navigation One',
//   },
//   {
//     key: 'app',
//     icon: () => h(AppstoreOutlined),
//     label: 'Navigation Two',
//     title: 'Navigation Two',
//   },
// ]);
export default {
  name: 'App'
};
</script>

<template>
  <div id="app">
    <router-link to="/">Home</router-link> |
    <router-link to="/movies">电影</router-link> |
    <router-link to="/persons">演员</router-link>
    <router-view />
  </div>
</template>

<style>
</style>
