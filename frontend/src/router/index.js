import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Movies from '../views/Movies.vue';
import MovieDetail from '../views/MovieDetail.vue';
import Persons from '../views/Persons.vue';
import PersonDetail from '../views/PersonDetail.vue';
import Login from '../views/Login.vue';

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/movies', name: 'Movies', component: Movies },
  { path: '/movies/:id', name: 'MovieDetail', component: MovieDetail, props: true },
  { path: '/persons', name: 'Persons', component: Persons },
  { path: '/persons/:id', name: 'PersonDetail', component: PersonDetail, props: true },
  { path: '/login', name: 'Login', component: Login },
];


const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to, from, next) => {
  const isLoggedIn = localStorage.getItem('isLoggedIn'); // 检查登录状态

  if (to.name !== 'Login' && !isLoggedIn) {
    // 如果未登录且试图访问非登录页面，跳转到登录页面
    next({ name: 'Login' });
  } else {
    next(); // 否则放行
  }
});

export default router;
