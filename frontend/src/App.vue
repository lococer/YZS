<template>
  <div id="app">
    isNavVisible: {{ isNavVisible }}
    <div v-show="isNavVisible">
      <router-link to="/login">登录</router-link> |
      <router-link to="/">Home</router-link> |
      <router-link to="/movies">电影</router-link> |
      <router-link to="/persons">演员</router-link>
    </div>
    <router-view />
  </div>
</template>

<script>
// TODO 设置导航
import axios from 'axios';
import { onMounted, ref, watch } from 'vue';
import { useRouter } from 'vue-router';
export default {
  name: 'App',
  setup() {
    let isNavVisible = ref(true);
    const router = useRouter();

    // 监听路由变化
    watch(
      () => router.currentRoute.value,
      (route) => {
        // 检查路由名称是否为 'Login'
        if (route.name === 'Login') {
          isNavVisible.value = false;
        } else {
          isNavVisible.value = true;
        }
      },
      { immediate: true } // 立即执行监听函数
    );

    return {
      isNavVisible,
    };
  },
};
</script>

<style></style>
