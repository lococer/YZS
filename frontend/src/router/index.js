import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Movies from '../views/Movies.vue';
import MovieDetail from '../views/MovieDetail.vue';
import Persons from '../views/Persons.vue';
import PersonDetail from '../views/PersonDetail.vue';

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/movies', name: 'Movies', component: Movies },
  { path: '/movies/:id', name: 'MovieDetail', component: MovieDetail, props: true },
  { path: '/persons', name: 'Persons', component: Persons },
  { path: '/persons/:id', name: 'PersonDetail', component: PersonDetail, props: true },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
