<template>
    <div>
        <h2>标签筛选</h2>
        <a-row gutter="16">
            <a-col :span="24">
                <!-- 使用 Select 组件 -->
                <a-select mode="multiple" allow-clear placeholder="请选择标签" style="width: 100%" @change="filterMovies">
                    <a-select-option v-for="tag in movieTags" :key="tag" :value="tag">
                        {{ tag }}
                    </a-select-option>
                </a-select>
            </a-col>
        </a-row>
        <div>
            <h2>年份筛选</h2>
            <!-- 滑动输入条 -->
            <a-slider v-model:value="yearRange" :min="minYear" :max="maxYear" :range="true"
                onUpdate:value="handleYearChange" />
        </div>
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
        <a-button type="primary" @click="fetchMovies(1, pageSize)">筛选</a-button>
    </div>
    <div v-if = "movies.length > 0">
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
    <div v-else>
        <a-empty/>
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
            minYear: 1900, // 最小年份
            maxYear: 2021, // 最大年份
            yearRange: [1900, 2021], // 选择的年份范围
        };
    },
    methods: {
        async fetchMovies(page, pageSize) {
            const tags = this.filterTag;
            const actors = this.selectedActors;
            const yearRange = this.yearRange;
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
                        yearRange: yearRange.join(','),
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
                this.movieTags = [
                    '喜剧', '剧情', '儿童', '青春', '家庭', '爱情', '科幻', '魔幻','奇幻', '灾难',
                    '恐怖', '惊悚', '悬疑', '犯罪', '黑帮', '冒险',
                    '功夫', '武侠', '人物', '传记', '纪录',
                    '动画', '短片',
                ]
            } catch (error) {
                console.error('Error fetching tags:', error);
            }
        },

        filterMovies(tag) {
            this.filterTag = [tag];
            // this.fetchMovies(1, this.pageSize);
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
        handleYearChange(yearRange) {
            console.log('Year range:', yearRange);
            // this.fetchMovies(1, this.pageSize);
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