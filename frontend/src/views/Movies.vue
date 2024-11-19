<template>
    <div>
        <h2>标签筛选</h2>
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
    <div v-if="selectedActors.length > 0">
        <h2>演员筛选</h2>
        <a-select mode="multiple" placeholder="选择演员" v-model:value="selectedActors" @change="handleActorChange">
            <a-select-option v-for="actor in actors" :key="actor.id" :value="actor.id">
                {{ actor.name }}
            </a-select-option>
        </a-select>
    </div>
    <div>
        <!-- BUG: 筛选后换页会导致筛选失效，应该保存筛选条件 -->
        <a-pagination v-model:value="current" :page-size-options="pageSizeOptions" :total="total" show-size-changer
            :page-size="pageSize" @change="onPaginationChange">
            <template slot="buildOptionText" slot-scope="props">
                <span>{{ props.value }}条/页</span>
            </template>
        </a-pagination>
        <h2>电影列表</h2>
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
import { Card, Row, Col, Pagination, Select } from 'ant-design-vue';  // 导入需要的组件

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
            filterTag: [], // 当前筛选的标签
            selectedActors: [], // 用户选择的演员
            actors: [], // 所有演员列表
        };
    },
    methods: {
        async fetchMovies(page, pageSize) {
            const tags = this.filterTag;
            const actors = this.selectedActors;
            console.log("before this.selectedActors",this.selectedActors);
            try {
                console.log("Fetching movies with page:", page, "pageSize:", pageSize, "tags:", tags, "actors:", actors);
                // const response = await axios.get(`http://127.0.0.1:5001/api/movies?page=${page}&pageSize=${pageSize}&tags=${tags.join(',')}&actors=${actors.join(',')}`);
                const response = await axios.get(`http://127.0.0.1:5001/api/movies`, {
                    params: {
                        page: page,
                        pageSize: pageSize,
                        actors: actors,
                        tags: tags.join(','),
                    },
                    paramsSerializer: (params) => {
                        // 自定义序列化逻辑，将 actors 数组转换为 `actors=actor1&actors=actor2`
                        return Object.entries(params)
                            .map(([key, value]) =>
                                Array.isArray(value)
                                    ? value.map((v) => `${key}=${encodeURIComponent(v)}`).join('&')
                                    : `${key}=${encodeURIComponent(value)}`
                            )
                            .join('&');
                    },
                });
                this.movies = response.data.movies;
                this.total = response.data.total;
                console.log("Fetched movies:", this.movies.length, "total:", this.total);
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
            this.filterTag = [tag];
            this.fetchMovies(1, this.pageSize);
        },

        async fetchActors() {
            try {
                const response = await axios.get('http://127.0.0.1:5001/api/allPersons');
                this.actors = response.data.actors;
                console.log('Fetched actors:', this.actors);
            } catch (error) {
                console.error('Error fetching actors:', error);
            }
        },

        async turnActorIdToName(actorId) {
            try{
                const response = await axios.get(`http://127.0.0.1:5001/api/person/${actorId}`);
                console.log('Turning actor id to name:', actorId);
                console.log('Response:', response);
                console.log('Name:', response.data.name);
                return response.data.name;
            } catch (error) {
                console.error('Error fetching actor name:', error);
            }
        },
    },
    mounted() {
    },
    async created() {
        this.fetchTotal()
        this.fetchTags();
        this.fetchActors();
        if (this.$route.query.actor1 && this.$route.query.actor2) {
            console.log('Query actors:', this.$route.query.actor1, this.$route.query.actor2);
            this.selectedActors = [await this.turnActorIdToName(this.$route.query.actor1), await this.turnActorIdToName(this.$route.query.actor2)];
            console.log('Selected actors:', this.selectedActors);
        }
        this.fetchMovies(this.current, this.pageSize);
    },
    components: {
        'a-pagination': Pagination,
        'a-select': Select,
    },
};
</script>
<style scoped>
.movie-list {
    padding: 20px;
}
</style>