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
                            <p><strong>生日:</strong>{{ person.birthday }}</p>
                            <p><strong>出生地:</strong>{{ person.birthplace }}</p>
                        </a-card>
                    </a-col>

                    <!-- 右侧详细信息和作品列表 -->
                    <a-col :span="12">
                        <a-card title="简介" hoverable>
                            <p>{{ person.summary }}</p>
                        </a-card>
                        <a-card title="作品列表" hoverable>
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

export default {
    props: ['id'],
    data() {
        return {
            person: {},
            echartData: {},
        };
    },
    async created() {
        try {
            // 请求人员数据
            const response = await axios.get(`http://127.0.0.1:5001/api/persons/${this.id}`);
            this.person = response.data;
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
                if( params.dataType == 'node' ){
                    console.log(navigateToPerson)
                    navigateToPerson(params.data.url)
                }
            })
        },
    },
    mounted() {
        this.fetchEchartData();

    }
};
</script>

<style scoped>
.header {
    color: white;
    font-size: 24px;
    text-align: center;
    background-color: #1890ff;
    padding: 16px;
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
</style>