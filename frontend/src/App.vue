<template>
  <div id="app">
    <div>
      <!-- <router-link to="/login">登录</router-link> |
      <router-link to="/">Home</router-link> |
      <router-link to="/movies">电影</router-link> |
      <router-link to="/persons">演员</router-link> -->
      <a-layout>
      <!-- Header -->
      <a-layout-header>
        <a-menu
          theme="dark"
          mode="horizontal"
          :selectedKeys="[selectedKey]"
        >
          <a-menu-item key="login">
            <router-link to="/login">登录</router-link>
          </a-menu-item>
          <a-menu-item key="home">
            <router-link to="/">主页</router-link>
          </a-menu-item>
          <a-menu-item key="movies">
            <router-link to="/movies">电影</router-link>
          </a-menu-item>
          <a-menu-item key="persons">
            <router-link to="/persons">演员</router-link>
          </a-menu-item>
          <a-menu-item key="predict">
            <router-link to="/predict">评分预测</router-link>
          </a-menu-item>
        </a-menu>
      </a-layout-header>

      <!-- Content -->
      <a-layout-content style="padding: 24px; min-height: 280px">
        <router-view />
      </a-layout-content>
    </a-layout>
    </div>
    <!-- <router-view /> -->
  </div>
</template>

<script>
// TODO 设置导航
import axios from 'axios';
import { onMounted, ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import { Menu, Layout } from 'ant-design-vue';
import router from './router';

export default {
  name: 'App',
  components: {
    'a-layout-sider': Layout.Sider,
    'a-menu': Menu,
    'a-menu-item': Menu.Item,
  },
  setup() {
    let isNavVisible = ref(true);
    const router = useRouter();
    const selectedKey = ref("");

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

    watch(
      () => router.currentRoute.value.path,
      (newPath) => {
        if (newPath.startsWith("/login")) {
          selectedKey.value = "login";
        } else if (newPath === "/") {
          selectedKey.value = "home";
        } else if (newPath.startsWith("/movies")) {
          selectedKey.value = "movies";
        } else if (newPath.startsWith("/persons")) {
          selectedKey.value = "persons";
        } else {
          selectedKey.value = "";
        }
      },
      { immediate: true }
    );

    return {
      isNavVisible,
      selectedKey,
    };
  },
};
</script>

<style></style>
