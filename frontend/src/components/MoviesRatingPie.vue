<template>
  <div>
    <div id="rating-pie-chart" style="width: 600px; height: 400px;"></div>
  </div>
</template>
<script>
import * as echarts from "echarts";
import { useRouter } from 'vue-router'; // 引入 vue-router

export default {
  props: {
    ratings: {
      type: Array, // 示例：[{ name: '8分以上', value: 50 }, { name: '6-8分', value: 30 }, { name: '6分以下', value: 20 }]
      required: true,
    },
  },
  mounted() {
    this.initChart();
  },
  setup(){
    const router = useRouter();
    return {
      router
    }
  },
  methods: {
    initChart() {
      const chartDom = document.getElementById("rating-pie-chart");
      const myChart = echarts.init(chartDom);

      // 配置项
      const option = {
        title: {
          text: "电影评分分布",
          left: "center",
        },
        tooltip: {
          trigger: "item",
        },
        legend: {
          orient: "vertical",
          left: "left",
        },
        series: [
          {
            name: "评分占比",
            type: "pie",
            radius: "50%",
            data: this.ratings,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: "rgba(0, 0, 0, 0.5)",
              },
            },
          },
        ],
      };

      const navigateToMovies = (params) => {
        console.log(params.name[0]);
        const query = {
          rating: parseInt(params.name[0]),
        };

        console.log(query);
        this.$router.push({
          name: "Movies",
          query,
        });
      };

      // 绑定点击事件
      myChart.on("click", (params) => {
        if( params.componentType === "series" && params.seriesType === "pie" ) {
          navigateToMovies(params.data);
        }
      });

      // 绘制图表
      myChart.setOption(option);
    },
  },
};
</script>
