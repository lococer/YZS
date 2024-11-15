<template>
    <div>
        <a-layout>
            <!-- 顶部标题区域 -->
            <a-layout-header class="header">
                演员详情
            </a-layout-header>

            <a-layout-content class="content">
                <a-row gutter="16">
                    <!-- 左侧基本信息 -->
                    <a-col :span="12">
                        <a-card hoverable>
                            <img class="actor-img" :src="fetchImage(person.img)" alt="actor-image" />
                            <h2>{{ person.name }}</h2>
                            <p><strong>性别:</strong>{{ person.sex }}</p>
                            <p><strong>生日:</strong>{{ person.birthday }}</p>
                            <p><strong>出生地:</strong>{{ person.birthplace }}</p>
                        </a-card>
                        <a-card title="" hoverable style="margin-top: 20px;">
                            <a-collapse>
                                <a-collapse-panel header="简介">
                                    {{ person.summary }}
                                </a-collapse-panel>
                            </a-collapse>
                            <!-- <p>{{ person.summary }}</p> -->
                        </a-card>
                    </a-col>

                    <!-- 右侧详细信息和作品列表 -->
                    <a-col :span="12">
                        <a-card title="作品列表" hoverable >
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
                                <div v-for="movie in movies" :key="movie.id">
                                    <a-card :hoverable="true" @click="goToMovieDetail(movie.id)">
                                        <a-card-meta :title="movie.name" :description="'Rating: ' + movie.rating" />
                                        <template #cover>
                                            <img :src="fetchImage(movie.img)" alt="cover" :title="movie.name"/>
                                        </template>
                                    </a-card>
                                </div>
                            </a-carousel>
                        </a-card>
                    </a-col>
                </a-row>
            </a-layout-content>
        </a-layout>
        <a-divider />
        <!-- 新增区块用于显示 ECharts -->
        <a-row :gutter="16" style="margin-top: 20px;">
            <a-col :span="24">
                <div ref="chartContainer" style="width: 100%; height: 400px;"></div> <!-- 用于显示 ECharts 图表 -->
            </a-col>
        </a-row>
    </div>
</template>

<script>
import axios from 'axios';
import * as echarts from 'echarts';
import { useRouter } from 'vue-router'; // 引入 vue-router
import { Carousel } from 'ant-design-vue';
import { LeftCircleOutlined, RightCircleOutlined } from '@ant-design/icons-vue';

export default {
    props: ['id'],
    data() {
        return {
            person: {},
            echartData: {},
            movies: {},
        };
    },
    components: {
        'a-carousel': Carousel,
        LeftCircleOutlined,
        RightCircleOutlined
    },
    async created() {
        try {
            // 请求人员数据
            let response = await axios.get(`http://127.0.0.1:5001/api/persons/${this.id}`);
            this.person = response.data;
            response = await axios.get(`http://127.0.0.1:5001/api/persons/movies/${this.id}`);
            this.movies = response.data;
            console.log(this.movies)
        } catch (error) {
            console.error("Error fetching person details:", error);
        }
    },
    setup() {
        const router = useRouter(); // 获取路由实例

        return {
            router
        };
    },
    methods: {
        // 拼接图片路径
        fetchImage(imageUrl) {
            return `http://127.0.0.1:5001/proxy-image/${imageUrl}`;
        },
        fetchPersonData() {
            // 请求演员数据
            axios.get(`http://127.0.0.1:5001/api/persons/${this.id}`).then(response => {
                this.person = response.data;
            });
        },
        fetchEchartData() {
            // 请求演员关系数据
            axios.get(`http://127.0.0.1:5001/api/persons/relations/${this.id}`).then(response => {
                this.echartData = response.data;
                this.renderEchart();
            });
        },
        renderEchart() {
            // 渲染 ECharts 图表
            // 获取图表容器
            const chartContainer = this.$refs.chartContainer;

            console.log(this.echartData);
            console.log(this.echartData.actors)

            // 初始化 ECharts 实例
            const myChart = echarts.init(chartContainer);

            var option = {
                title: {
                    text: '演员关系图'
                },
                tooltip: {},
                series: [
                    {
                        type: 'graph',
                        layout: 'force',  // 使用力导向布局
                        nodes: this.echartData.actors.map(actor => ({
                            name: actor.name,
                            value: actor.name,
                            itemStyle: {
                                color: actor.name == this.person.name ? '#ff0000' : '#5474c4'
                            },
                            url: actor.id
                        })),
                        links: this.echartData.links.map(link => ({
                            source: link.source,
                            target: link.target,
                            value: link.value,
                            url: link.url
                        })),
                        roam: true,  // 允许拖拽
                        draggable: true,
                        label: {
                            show: true,
                            position: 'right',
                            formatter: '{b}'  // 显示演员名字
                        },
                        force: {
                            repulsion: 50,  // 设置节点之间的斥力
                            edgeLength: [50, 200]
                        },
                        layoutAnimation: true,
                        focusNodeAdjacency: true,
                    }
                ]
            };

            // 设置图表选项
            myChart.setOption(option);

            // 将 router 存储为外部变量
            const navigateToPerson = (url) => {
                // this.router.push({ path: `/persons/${url}` });
                // this.fetchPersonData();
                // this.fetchEchartData();
                window.location.href = `/persons/${url}`;
            };

            myChart.on('click', function (params) {
                if (params.dataType == 'node') {
                    console.log(navigateToPerson)
                    navigateToPerson(params.data.url)
                }
            })
        },
        goToMovieDetail(id) {
            console.log("Going to movie detail for movie with id:", id);
            this.$router.push({ name: 'MovieDetail', params: { id } });
        },
    },
    mounted() {
        this.fetchEchartData();

    }
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

.content {
    padding: 24px;
    background: #f0f2f5;
}

.actor-image {
    width: 100%;
    height: auto;
    border-radius: 8px;
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