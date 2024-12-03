<template>
  <div>
    <!-- TODO 添加图 -->
    <h1>欢迎来到影智算</h1>
    <!-- <p>Use this app to predict movie ratings and explore movies.</p> -->
    <p>在这里，你可以查看电影信息总览以及演员电影信息总览。</p>
  </div>
  <div>
    <h2>电影评分分布</h2>
    <moviesrationg-pie v-if="moviesRatings.length > 0" :ratings="moviesRatings"></moviesrationg-pie>
  </div>
  <div>
    <h2>电影国家分布</h2>
    <MoviesCountryPie v-if="moviesCountries.length > 0" :countries="moviesCountries"></MoviesCountryPie>
  </div>
</template>

<script>
import MoviesrationgPie from "../components/MoviesRatingPie.vue";
import MoviesCountryPie from "../components/MoviesCountryPie.vue";
import axios from "axios";

export default {
  data(){
    return {
      moviesRatings: [], 
      moviesCountries:[],
    }
  },
  components: {
    MoviesrationgPie,
    MoviesCountryPie,
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
    async getMoviesCountries() {
      try{
        const response = await fetch("http://127.0.0.1:5001/api/MoviesCountries")
        const data = await response.json()
        this.moviesCountries = data.map((country)=>{
          return{
            name: country.country,
            value: country.total,
          }
        });
        console.log(this.moviesCountries)
      } catch(error) {
        console.log(error)
      }
    },
  },
  created() {
    this.getMoviesRatings();
    this.getMoviesCountries();
  },
};

</script>
