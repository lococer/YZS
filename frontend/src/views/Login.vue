<template>

  <div>
    <!-- <a-alert type="success" message="欢迎回来！" show-icon /> -->
     <!-- <a-alert v-if="showLoginAlert" message="请先登录" type="warning" show_icon />
     {{ showLoginAlert}} <br>
     isLoggedIn:{{ isLoggedIn }}
     <a-alert v-if="isJustLoginOut" type="success" message="退出成功" show-icon /> -->
  </div>

  <a-card class="login-form">
    <h2>{{ isLogin ? '登录' : '注册' }}</h2>
    <a-form @submit.prevent="handleSubmit">
      <!-- 用户名字段 -->
      <a-form-item>
        <a-input v-model:value="form.username" :rules="[
          { required: true, message: '请输入用户名' },
        ]" placeholder="请输入用户名">
          <a-icon slot="prefix" type="user" />
        </a-input>
        <!-- <h4>{{ form.username }}</h4> -->
      </a-form-item>

      <!-- 密码字段 -->
      <a-form-item>
        <a-input v-model:value="form.password" :rules="[
          { required: true, message: '请输入密码' },
        ]" type="password" placeholder="请输入密码">
          <a-icon slot="prefix" type="lock" />
        </a-input>
      </a-form-item>

      <!-- 确认密码字段 -->
      <a-form-item v-if="!isLogin">
        <a-input v-model:value="form.confirmPassword" :rules="[{ required: true, message: '请确认密码!' }]" type="password"
          placeholder="确认密码">
          <a-icon slot="prefix" type="lock" />
        </a-input>
      </a-form-item>

      <!-- 提交按钮和切换按钮 -->
      <a-form-item>
        <a-button type="primary" html-type="submit" :loading="submitting">{{ isLogin ? '登录' : '注册'
          }}</a-button>
        <!-- <a-button @click="switchForm" style="margin-left: 8px">切换到{{ isLogin ? '注册' : '登录' }}</a-button> -->
        <a-switch v-model:checked="isLogin" style="margin-left: 8px"
          checked-children="登录" un-checked-children="注册"
        >{{ isLogin ? '登录' : '注册' }}</a-switch>
      </a-form-item>
    </a-form>
    <a-button @click="loginOut" style="margin-top: 16px">退出登录</a-button>
  </a-card>
</template>

<script>
import axios from 'axios';
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import { notification } from 'ant-design-vue';
import { useUserStore } from '../stores/user.js';

export default {
  data() {
    return {
      form: {
        username: '123',
        password: '',
        confirmPassword: '',
      },
      isLogin: true,
      submitting: false,
      showLoginAlert: false,
      isJustLoginOut: false,
      isLoggedIn: computed(() => {
        return localStorage.getItem('isLoggedIn') === 'true';
      }),
    };
  },
  setup(){
    const notifyUser = (message, description) => {
      notification.open({
        message: message,
        description: description,
        duration: 4.5,
      });
    };

    return {
      notifyUser,
    };
  },
  created(){
    if(this.$route.query.redirect){
      this.showLoginAlert = true;
    }
  },
  methods: {
    async handleSubmit() {
      this.submitting = true;

      const apiUrl = this.isLogin
        ? 'http://127.0.0.1:5001/api/login'
        : 'http://127.0.0.1:5001/api/register'; // 拼接正确的 URL

      console.log(apiUrl);
      console.log(this.form);

      // 表单验证通过后发送请求
      try {
        const response = await axios.post(apiUrl, this.form);
        this.submitting = false;
        // 请求成功后执行的操作
        console.log(response.data);
        // 例如，跳转到其他页面或存储用户信息
        localStorage.setItem('isLoggedIn', 'true');  // 登录后设置状态
        const userStore = useUserStore();
        userStore.setUserInfo( {name: this.form.username });
        const userinfo = userStore.userInfo;
        console.log(userinfo);

        // 跳转到首页
        this.$router.push('/');
      } catch (error) {
        this.submitting = false;
        // 请求失败后的错误处理
        console.error(error.response.data.message);
        if (error.response && error.response.status === 409) {
          // 假设 409 状态码是用户名已存在
          this.$message.error('用户名已存在');
        } else {
          this.$message.error('发生错误，请重试');
        }
      }
    },
    switchForm() {
      this.isLogin = !this.isLogin;
      // 重置表单字段
      this.form.username = '123';
      this.form.password = '';
      this.form.confirmPassword = '';
    },
    loginOut(){
      if(!this.isLoggedIn){
        // this.showLoginAlert = true;
        this.notifyUser('请先登录', '登录后才能退出');
        return;
      }
      try{
        axios.post('http://127.0.0.1:5001/api/logout');
        this.isJustLoginOut = true;
        localStorage.removeItem('isLoggedIn');
        this.$router.push('/login');
        this.notifyUser('退出成功', '您已成功退出登录');
      }catch(error){
        console.error(error);
      }
    },
  },
  onMounted(){
    // 监听路由变化，如果有 redirect 参数，则显示登录提示
    this.$watch(
      () => this.$route.query.redirect,
      (newVal) => {
        if (newVal) {
          this.showLoginAlert = true;
        }
      },
    );
  },
};
</script>

<style scoped>
.login-form {
  max-width: 300px;
  margin: 100px auto;
}
</style>
