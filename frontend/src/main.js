import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
// import 'ant-design-vue/dist/antd.css';
import Antd from 'ant-design-vue';
import { createPinia } from 'pinia';

const app = createApp(App);

app.config.globalProperties.$userInfo = null;
app.config.globalProperties.$setUserInfo = (info) => {
  app.config.globalProperties.$userInfo = info;
};

app.use(createPinia());
app.use(router);
app.use(Antd);
app.mount('#app');