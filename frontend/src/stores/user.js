import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
    state: () => ({
        userInfo: null, // 保存用户信息
    }),
    actions: {
        setUserInfo(info) {
            this.userInfo = info;
        },
        clearUserInfo() {
            this.userInfo = null;
        },
    },
    getters: {
        isLoggedIn: (state) => !!state.userInfo,
    },
});
