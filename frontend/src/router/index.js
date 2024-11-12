import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Movies from '../views/Movies.vue';
import MovieDetail from '../views/MovieDetail.vue';

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/movies', name: 'Movies', component: Movies },
  { path: '/movies/:id', name: 'MovieDetail', component: MovieDetail, props: true }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
