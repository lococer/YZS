<template>
    <div>
        <a-pagination v-model:value="current" :page-size-options="pageSizeOptions" :total="total" show-size-changer
            :page-size="pageSize" @change="onPaginationChange">
            <template slot="buildOptionText" slot-scope="props">
                <span>{{ props.value }}条/页</span>
            </template>
        </a-pagination>
        <h2>演员列表</h2>
        <div class="person-list">
            <a-row :gutter="16">
                <a-col :span="6" v-for="person in persons" :key="person.id">
                    <a-card :hoverable="true" @click="goToDetail(person.id)">
                        <a-card-meta :title="person.name" :description="'Rating: ' + person.rating" />
                        <template #cover>
                            <img :src="fetchImage(person.img)" alt="cover">
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
            persons: [],
            total: 0,
            current: 1,
            pageSize: 10,
            pageSizeOptions: [10, 20, 30, 40, 50],
        };
    },
    methods: {
        async fetchPersons(page, pageSize) {
            try {
                const response = await axios.get(`http://127.0.0.1:5001/api/persons?page=${page}&pageSize=${pageSize}`);
                this.persons = response.data;
            } catch (error) {
                console.error("Error fetching movies:", error);
            }
        },
        goToDetail(id) {
            console.log("Going to person detail for person with id:", id);
            this.$router.push({ name: 'PersonDetail', params: { id } });
        },
        fetchImage(imageUrl) {
            return `http://127.0.0.1:5001/proxy-image/${imageUrl}`;
        },
        onPaginationChange(current, pageSize) {
            this.current = current;
            this.pageSize = pageSize;
            this.fetchPersons(current, pageSize);
        },
        async fetchTotal() {
            try {
                const response = await axios.get(`http://127.0.0.1:5001/api/persons/count`);
                this.total = response.data.count;
            } catch (error) {
                console.error("Error fetching total:", error);
            }
        }
    },
    mounted() {
        this.fetchTotal();
        this.fetchPersons();
    }
};
</script>
<style scoped>
.person-list {
    padding: 20px;
}
</style>