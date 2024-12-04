<template>
    <div id="bubble" style="width: 100%; height: 500px;"></div>
</template>

<script>
import * as echarts from "echarts/core";
import { DatasetComponent, TooltipComponent, VisualMapComponent } from "echarts/components";
import { CustomChart } from "echarts/charts";
import { CanvasRenderer } from "echarts/renderers";
import * as d3 from "d3";

echarts.use([DatasetComponent, TooltipComponent, VisualMapComponent, CustomChart, CanvasRenderer]);

export default {
    name: "BubbleChart",
    props: {
        data: {
            type: Array,
            required: true,
            default: () => [],
        },
    },
    data() {
        return {
            colorList: ["#5470c6", "#91cc75", "#fac858", "#ee6666", "#73c0de", "#3ba272", "#fc8452", "#9a60b4", "#ea7ccc"],
        };
    },
    mounted() {
        this.initChart();
    },
    methods: {
        initChart() {
            try {
                const seriesData = this.data.map((item, index) => ({
                    depth: 1,
                    id: item.tag,
                    index,
                    value: item.count,
                }));

                const displayRoot = this.stratifyData(seriesData);

                const element = document.getElementById("bubble");
                if (!element) {
                    console.error("Bubble container not found");
                    return;
                }

                const myChart = echarts.init(element);
                myChart.setOption(this.createOption(seriesData, displayRoot));
            } catch (error) {
                console.error("Error initializing chart:", error);
            }
        },
        stratifyData(seriesData) {
            // 添加一个虚拟根节点
            const rootId = "root";
            const stratifyData = [
                { id: rootId, value: 0 }, // 根节点
                ...seriesData.map((item) => ({
                    id: item.id,
                    value: item.value,
                    parentId: rootId, // 所有其他节点的父节点是 root
                })),
            ];

            return d3
                .stratify()
                .id((d) => d.id) // 节点的唯一 ID
                .parentId((d) => d.parentId || null)(stratifyData) // 通过 parentId 指定父节点
                .sum((d) => d.value) // 求和
                .sort((a, b) => b.value - a.value); // 根据值排序
        },

        createOption(seriesData, displayRoot) {
            const overallLayout = (params, api) => {
                const context = params.context;
                d3
                    .pack()
                    .size([api.getWidth() - 2, api.getHeight() - 2])
                    .padding(10)(displayRoot);

                context.nodes = {};
                displayRoot.descendants().forEach((node) => {
                    context.nodes[node.id] = node;
                });
            };

            const renderItem = (params, api) => {
                const context = params.context;
                if (!context.layout) {
                    context.layout = true;
                    overallLayout(params, api);
                }

                const node = context.nodes[api.value("id")];
                if (!node) return;

                // console.log(node);

                return {
                    type: "circle",
                    shape: {
                        cx: node.x,
                        cy: node.y,
                        r: node.r,
                    },
                    textContent: {
                        type: "text",
                        style: {
                            text: node.id,
                            fontSize: Math.max(node.r / 3, 12),
                            fill: "#fff",
                        },
                        position: [node.x - node.r / 3, node.y - node.r / 10], // 文本位置
                    },
                    style: {
                        fill: this.colorList[params.dataIndex % this.colorList.length],
                    },
                };
            };

            return {
                dataset: {
                    source: seriesData,
                },
                tooltip: {
                    formatter: (params) => `${params.data.id}: ${params.data.value}`,
                },
                series: [
                    {
                        type: "custom",
                        renderItem,
                        progressive: 0,
                        coordinateSystem: "none",
                    },
                ],
            };
        },
    },
};
</script>


  
