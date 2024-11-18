import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
    state: () => ({
        userInfo: JSON.parse(localStorage.getItem('userInfo')) || {}  // 初始值从 localStorage 获取
    }),
    actions: {
        setUserInfo(userInfo) {
            this.userInfo = userInfo;
            localStorage.setItem('userInfo', JSON.stringify(userInfo));  // 更新时持久化到 localStorage
        },
        clearUserInfo() {
            this.userInfo = {};
            localStorage.removeItem('userInfo');
        }
    }
});
