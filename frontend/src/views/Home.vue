<template>
  <div>
    <!-- TODO 添加图 -->
    <!-- TODO 添加跳转 -->
    <h1>欢迎来到影智算</h1>
    <p>Use this app to predict movie ratings and explore movies.</p>
  </div>
  <div>
    <h2>电影评分分布</h2>
    <moviesrationg-pie v-if="moviesRatings.length > 0" :ratings="moviesRatings"></moviesrationg-pie>
  </div>
</template>

<script>
import MoviesrationgPie from "../components/MoviesRatingPie.vue";
import axios from "axios";

export default {
  data(){
    return {
      moviesRatings: [], 
    }
  },
  components: {
    MoviesrationgPie
  },
  methods: {
    async getMoviesRatings() {
      try{
        const response = await fetch("http://127.0.0.1:5001/api/MoviesRatings")
        const data = await response.json()
        this.moviesRatings = data.ratings
      } catch(error) {
        console.log(error)
      }
    },
  },
  created() {
    this.getMoviesRatings()
  },
};

</script>
