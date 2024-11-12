<template>
    <div>
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
import { Card, Row, Col } from 'ant-design-vue';  // 导入需要的组件

export default {
    components: { 'a-card': Card, 'a-row': Row, 'a-col': Col },
    data() {
        return {
            persons: []
        };
    },
    methods: {
        async fetchPersons() {
            try {
                const response = await axios.get('http://127.0.0.1:5001/api/persons');
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
        }
    },
    mounted() {
        this.fetchPersons();
    }
};
</script>
<style scoped>
.person-list {
    padding: 20px;
}
</style>