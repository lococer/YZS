<template>
  <div>
    <h1>{{ movie.name }}</h1>
    <img :src="fetchImage(movie.img)" alt="cover" />
    <p>Rating: {{ movie.rating }}</p>
    <p>{{ movie.description }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: ['id'],
  data() {
    return {
      movie: {}
    };
  },
  async created() {
    try {
      const response = await axios.get(`http://127.0.0.1:5001/api/movies/${this.id}`);
      this.movie = response.data;
    } catch (error) {
      console.error("Error fetching movie details:", error);
    }
  },
  methods: {
    fetchImage(imageUrl) {
        return `http://127.0.0.1:5001/proxy-image/${imageUrl}`;
    }
  }
};
</script>
