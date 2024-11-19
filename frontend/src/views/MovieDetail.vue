<template>
  <div>
    <a-layout>
      <a-layout-header class="header">
        电影详情
      </a-layout-header>

      <a-layout-content>
        <a-row :gutter="16">
          <a-col :span="12">
            <a-card hoverable>
              <img :src="fetchImage(movie.img)" alt="cover" />
              <h2>{{ movie.name }}</h2>
              <!-- <p>评分: {{ movie.rating }}</p>
              <p>年份: {{ movie.year }}</p>
              <p>类型: {{ movie.genre }}</p> -->
              <a-descriptions >
                <a-descriptions-item label="电影名"> {{ movie.name }} </a-descriptions-item>
                <a-descriptions-item label="导演">  </a-descriptions-item>
                <a-descriptions-item label="年份"> {{ movie.year }} </a-descriptions-item>
                <a-descriptions-item label="评分"> {{ movie.rating }} </a-descriptions-item>
                <a-descriptions-item label="类型"> {{ movie.genre }} </a-descriptions-item>
                <a-descriptions-item lable="评分图">  </a-descriptions-item>
              </a-descriptions>
            </a-card>
            <a-card hoverable style="margin-top: 20px;">
              <a-collapse>
                <a-collapse-panel header="简介">
                  {{ movie.summary }}
                </a-collapse-panel>
              </a-collapse>
            </a-card>
          </a-col>

          <a-col :span="12">
            <a-card hoverable title="演员列表">
              <a-carousel arrows>
                <template #prevArrow>
                  <div class="custom-slick-arrow" style="left: 10px; z-index: 1">
                    <left-circle-outlined />
                  </div>
                </template>
                <template #nextArrow>
                  <div class="custom-slick-arrow" style="right: 10px; z-index: 1">
                    <right-circle-outlined />
                  </div>
                </template>
                <div v-for="actor in actors" :key="actor.id">
                  <a-card :hoverable="true" @click="goToActorDetail(actor.id)">
                    <a-card-meta :title="actor.name" />
                    <template #cover>
                      <img :src="fetchImage(actor.img)" alt="cover" :title='actor.name' />
                    </template>
                  </a-card>
                </div>
              </a-carousel>
            </a-card>
          </a-col>
        </a-row>
      </a-layout-content>

    </a-layout>
    <MyComment :movieId="movie.id" :currentUsername="currentUsername" />
  </div>
</template>

<script>
import axios from 'axios';
import { Carousel } from 'ant-design-vue';
import { LeftCircleOutlined, RightCircleOutlined } from '@ant-design/icons-vue';
import MyComment from '../components/myComment.vue';
import { useUserStore } from '../stores/user.js';


export default {
  props: ['id'],
  data() {
    return {
      movie: {},
      actors: {},
      currentUsername: '',
    };
  },
  components: {
    'a-carousel': Carousel,
    LeftCircleOutlined,
    RightCircleOutlined,
    MyComment,
  },
  async created() {
    try {
      let response = await axios.get(`http://127.0.0.1:5001/api/movies/${this.id}`);
      this.movie = response.data;
      response = await axios.get(`http://127.0.0.1:5001/api/movies/actors/${this.id}`);
      this.actors = response.data;
    } catch (error) {
      console.error("Error fetching movie details:", error);
    }
    const userStore = useUserStore();
    console.log(userStore.userInfo.name);
    this.currentUsername = userStore.userInfo.name;
  },
  methods: {
    fetchImage(imageUrl) {
      return `http://127.0.0.1:5001/proxy-image/${imageUrl}`;
    },
    goToActorDetail(actorId) {
      this.$router.push({ name: 'PersonDetail', params: { id: actorId } });
    }
  },
  onMounted() {
  },
  updated() {

  },
};
</script>

<style scoped>
.header {
  background-color: #1890ff;
  padding: 0 24px;
  height: 64px;
  line-height: 64px;
  font-size: 20px;
  color: white;
  text-align: center;
}
:deep(.slick-slide) {
    text-align: center;
    height: 600px;
    line-height: 160px;
    background: #364d79;
    overflow: hidden;
}

:deep(.slick-arrow.custom-slick-arrow) {
    width: 25px;
    height: 25px;
    font-size: 25px;
    color: #fff;
    background-color: rgba(31, 45, 61, 0.11);
    transition: ease all 0.3s;
    opacity: 0.3;
    z-index: 1;
}

:deep(.slick-arrow.custom-slick-arrow:before) {
    display: none;
}

:deep(.slick-arrow.custom-slick-arrow:hover) {
    color: #fff;
    opacity: 0.5;
}

:deep(.slick-slide h3) {
    color: #fff;
}
</style>
