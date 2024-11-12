<template>
    <div>
        <h2>电影列表</h2>
        <div class="movie-list">
            <a-row :gutter="16">
                <a-col :span="6" v-for="movie in movies" :key="movie.id">
                    <a-card :hoverable="true" @click="goToDetail(movie.id)">
                        <a-card-meta :title="movie.name" :description="'Rating: ' + movie.rating" />
                        <template #cover>
                            <!-- <img :src="`http://127.0.0.1:5001//proxy-image/${movie.img}`" alt="cover" /> -->
                            <img :src="fetchImage(movie.img)" alt="cover">
                        </template>
                    </a-card>
                </a-col>
            </a-row>
        </div>

    </div>

</template>

<script>
import axios from 'axios';
import { Card, Row, Col } from 'ant-design-vue';  // 导入需要的组件

export default {
    components: { 'a-card': Card, 'a-row': Row, 'a-col': Col },
    data() {
        return {
            movies: []
        };
    },
    methods: {
        async fetchMovies() {
            try {
                const response = await axios.get('http://127.0.0.1:5001/api/movies');
                this.movies = response.data;
            } catch (error) {
                console.error("Error fetching movies:", error);
            }
        },
        goToDetail(id) {
            console.log("Going to movie detail for movie with id:", id);
            this.$router.push({ name: 'MovieDetail', params: { id } });
        },
        fetchImage(imageUrl) {
            return `http://127.0.0.1:5001/proxy-image/${imageUrl}`;
        }
    },
    mounted() {
        this.fetchMovies();
    }
};
</script>
<style scoped>
.movie-list {
    padding: 20px;
}
</style>