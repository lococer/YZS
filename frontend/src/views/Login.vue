<template>

    <div>
    </div>

    <a-card class="login-form">
        <h2>{{ isLogin ? '登录' : '注册' }}</h2>
        <a-form @submit.prevent="handleSubmit">
            <!-- 用户名字段 -->
            <a-form-item>
                <a-input v-model:value="form.username" 
                    :rules="[
                        { required: true, message: '请输入用户名' },
                    ]"
                    placeholder="请输入用户名">
                    <a-icon slot="prefix" type="user" />
                </a-input>
                <!-- <h4>{{ form.username }}</h4> -->
            </a-form-item>

            <!-- 密码字段 -->
            <a-form-item>
                <a-input v-model:value="form.password" 
                    :rules="[
                        { required: true, message: '请输入密码' },
                    ]"
                    type="password" 
                    placeholder="请输入密码">
                    <a-icon slot="prefix" type="lock" />
                </a-input>
            </a-form-item>

            <!-- 确认密码字段 -->
            <a-form-item v-if="!isLogin">
                <a-input v-model:value="form.confirmPassword" 
                    :rules="[{ required: true, message: '请确认密码!' }]" 
                    type="password"
                    placeholder="确认密码">
                    <a-icon slot="prefix" type="lock" />
                </a-input>
            </a-form-item>

            <!-- 提交按钮和切换按钮 -->
            <a-form-item>
                <a-button type="primary" html-type="submit" :loading="submitting">{{ isLogin ? '登录' : '注册'
                    }}</a-button>
                <a-button @click="switchForm" style="margin-left: 8px">切换到{{ isLogin ? '注册' : '登录'
                    }}</a-button>
            </a-form-item>
        </a-form>
    </a-card>
</template>

<script>
import axios from 'axios';

export default {
  data() {
  return {
    form:{
        username: '123',
        password: '',
        confirmPassword: '',
    },
    isLogin: true,
    submitting: false,
  };
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

        // 重置表单
        // this.$nextTick(() => {
        //   this.username = '';
        //   this.password = '';
        //   this.confirmPassword = '';
        // });

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
  },
};
</script>

<style scoped>
.login-form {
  max-width: 300px;
  margin: 100px auto;
}
</style>
