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

  <div>
    <h2>气泡图</h2>
    <BubbleChart :data="bubbleData" />
  </div>
</template>

<script>
import MoviesrationgPie from "../components/MoviesRatingPie.vue";
import MoviesCountryPie from "../components/MoviesCountryPie.vue";
import BubbleChart from "../components/BubbleChart.vue";
import axios from "axios";

export default {
  data(){
    return {
      moviesRatings: [], 
      moviesCountries:[],
      bubbleData: [
        { tag: "动作", count: 120 },
        { tag: "喜剧", count: 95 },
        { tag: "爱情", count: 85 },
        { tag: "科幻", count: 78 },
        { tag: "冒险", count: 65 },
        { tag: "惊悚", count: 60 },
        { tag: "动画", count: 55 },
        { tag: "剧情", count: 50 },
        { tag: "犯罪", count: 45 },
        { tag: "战争", count: 40 },
      ],
    }
  },
  components: {
    MoviesrationgPie,
    MoviesCountryPie,
    BubbleChart,
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
        // console.log("data1",this.moviesCountries)
        console.log(this.moviesCountries)
      } catch(error) {
        console.log(error)
      }
    },
    async getMoviesGenres(){
      try{
        const response = await fetch("http://127.0.0.1:5001/api/MoviesGenres")
        const data = await response.json()
        console.log("data",this.bubbleData)
        // this.bubbleData = data.genre_counts;
        this.bubbleData = data.map(item => {
          return { tag: item.genre, count: item.value };
        });
        console.log("data",this.bubbleData)
      } catch(error) {
        console.log(error)
      }
    }
  },
  created() {
    this.getMoviesRatings();
    this.getMoviesCountries();
    this.getMoviesGenres();
  },
};

</script>
