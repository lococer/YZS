<template>
    <div>
        <a-row gutter="16">
            <!-- 标签筛选部分 -->
            <a-col :span="24">
                <a-button-group>
                    <a-button v-for="tag in movieTags" :key="tag" @click="filterMovies(tag)">
                        {{ tag }}
                    </a-button>
                </a-button-group>
            </a-col>
        </a-row>
    </div>
    <div>
        <!-- BUG: 筛选后换页会导致筛选失效，应该保存筛选条件 -->
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
            movieTags: ['动作', '喜剧'], // 电影标签
        };
    },
    methods: {
        async fetchMovies(page, pageSize, tags = []) {
            try {
                console.log("Fetching movies with page:", page, "pageSize:", pageSize, "tags:", tags);
                const response = await axios.get(`http://127.0.0.1:5001/api/movies?page=${page}&pageSize=${pageSize}&tags=${tags.join(',')}`);
                this.movies = response.data.movies;
                this.total = response.data.total;
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
        },
        // 获取所有标签
        async fetchTags() {
            try {
                // const response = await axios.get('http://127.0.0.1:5001/api/tags');
                // tags.value = response.data;  // 假设后端返回所有电影标签
                this.movieTags = ['动作', '喜剧', '爱情', '科幻', '动画', '悬疑', '惊悚', '恐怖', '犯罪', '同性'];
            } catch (error) {
                console.error('Error fetching tags:', error);
            }
        },

        filterMovies(tag) {
            this.fetchMovies(1, this.pageSize, [tag]);
        },
    },
    mounted() {
        this.fetchTotal()
        this.fetchMovies(this.current, this.pageSize);
        this.fetchTags();
    }
};
</script>
<style scoped>
.movie-list {
    padding: 20px;
}
</style>