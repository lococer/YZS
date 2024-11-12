<template>
    <div>
        <a-pagination v-model:value="current" :page-size-options="pageSizeOptions" :total="total" show-size-changer
            :page-size="pageSize" @change="onPaginationChange">
            <template slot="buildOptionText" slot-scope="props">
                <span>{{ props.value }}条/页</span>
            </template>
        </a-pagination>
        <h2>电影列表{{ current }}</h2>
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
import { Card, Row, Col, Pagination } from 'ant-design-vue';  // 导入需要的组件

export default {
    components: { 'a-card': Card, 'a-row': Row, 'a-col': Col },
    data() {
        return {
            movies: [],
            total: 200, // 总条数
            pageSize: 10, // 每页条数
            current: 1, // 当前页
            pageSizeOptions: ['10', '20', '30', '40', '50'], // 分页选项
        };
    },
    methods: {
        async fetchMovies(page, pageSize) {
            try {
                const response = await axios.get(`http://127.0.0.1:5001/api/movies?page=${page}&pageSize=${pageSize}`);
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
        },
        onPaginationChange(current, pageSize) {
            this.current = current;
            this.pageSize = pageSize;
            this.fetchMovies(current, pageSize);
        },
        async fetchTotal() {
            try {
                const response = await axios.get(`http://127.0.0.1:5001/api/movies/count`);
                this.total = response.data.count;
            } catch (error) {
                console.error("Error fetching total:", error);
            }
        }
    },
    mounted() {
        this.fetchTotal()
        this.fetchMovies(this.current, this.pageSize);
    }
};
</script>
<style scoped>
.movie-list {
    padding: 20px;
}
</style>