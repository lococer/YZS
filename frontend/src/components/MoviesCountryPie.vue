<template>
    <div>
      <div id="country-bar-chart" style="width: 800px; height: 400px;"></div>
    </div>
  </template>
  
  <script>
  import * as echarts from "echarts";
  import { useRouter } from 'vue-router'; // 引入 vue-router
  
  export default {
    props: {
      countries: {
        type: Array, // 示例：[{ name: '美国', value: 50 }, { name: '中国', value: 30 }, { name: '法国', value: 20 }, ...]
        required: true,
      },
    },
    // data(){
    //     return{
    //         countries: [{ name: '美国', value: 50 }, { name: '中国', value: 30 }, { name: '法国', value: 20 }],
    //     }
    // },
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
        const chartDom = document.getElementById("country-bar-chart");
        const myChart = echarts.init(chartDom);
  
        // 只取前10个国家的数据
        this.countries.sort((a, b) => b.value - a.value);
        const topCountries = this.countries.slice(0, 10);
  
        // 配置项
        const option = {
          title: {
            text: "电影国家分布（前10）",
            left: "center",
          },
          tooltip: {
            trigger: "axis",
            axisPointer: {
              type: "shadow"
            }
          },
          xAxis: {
            type: "category",
            data: topCountries.map(item => item.name)
          },
          yAxis: {
            type: "value"
          },
          series: [
            {
              name: "数量",
              type: "bar",
              data: topCountries.map(item => item.value),
              itemStyle: {
                normal: {
                  label: {
                    show: true,
                    position: "top",
                    formatter: function(params) {
                      return params.value;
                    }
                  }
                }
              },
            }
          ]
        };
  
        const navigateToMovies = (params) => {
          console.log(params);
          const query = {
            country: params,
          };

          console.log(query);
          this.$router.push({
            name: "Movies",
            query,
          });
        };
        
        // 绑定点击事件
        myChart.on("click", (params) => {
          console.log(params);
          if (params.componentType === "series" && params.seriesType === "bar") {
            navigateToMovies(params.name);
          }
        });

        // 绘制图表
        myChart.setOption(option);
      },
    },
  };
  </script>