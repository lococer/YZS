<template>
    <div>
        <h2>演员名</h2>
        <a-row :gutter="16">
            <a-col :span="12">
                <a-input v-model:value="searchText" placeholder="搜索演员" />
            </a-col>
        </a-row>
        <h2>性别筛选</h2>
        <a-row :gutter="16">
            <a-col :span="12">
                <a-checkbox v-model:checked="genderMale">男</a-checkbox>
                <a-checkbox v-model:checked="genderFemale">女</a-checkbox>
            </a-col>
        </a-row>
        <h2>出生地</h2>
        <a-row :gutter="16">
            <a-col :span="12">
                <a-select mode="tags" allow-clear placeholder="选择国家" style="width: 100%" >
                    <a-select-option v-for="country in actorCountry" :key="country" :value="country">
                        {{ country }}
                    </a-select-option>
                </a-select>
            </a-col>
        </a-row>
        <h2>生日筛选</h2>
        <a-row :gutter="16">
            <a-col :span="12">
                <a-slider v-model:value="birthYearRange" :min="minbirthYear" :max="maxbirthYear" :range="true" />
            </a-col>
        </a-row>
        <div>
            <a-button type="primary" @click="fetchPersons(1, pageSize)">筛选</a-button>
        </div>
    </div>
    <div>
        <a-pagination v-model:value="current" :page-size-options="pageSizeOptions" :total="total" show-size-changer
            :page-size="pageSize" @change="onPaginationChange">
            <template slot="buildOptionText" slot-scope="props">
                <span>{{ props.value }}条/页</span>
            </template>
        </a-pagination>
        <div v-if="persons.length > 0">
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
        <div v-else>
            <a-empty description="No persons found" />
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
            searchText: '',
            minbirthYear: 1900,
            maxbirthYear: 2022,
            birthYearRange: [1900, 2022],
            genderMale: true,
            genderFemale: true,
            actorCountry: [
                    "不丹", "东德", "中国", "中国大陆", "丹麦", "乌克兰", "乌拉圭", "乍得", "亚美尼亚",
                    "以色列", "伊朗", "俄罗斯", "保加利亚", "克罗地亚", "八一电影制片厂", "冰岛", "冰島Iceland",
                    "刚果", "利比亚", "加拿大", "加拿大Canada", "加纳", "匈牙利", "南斯拉夫", "南斯拉夫联盟共和国",
                    "南非", "卡塔尔", "卢森堡", "印度", "印度尼西亚", "原西德", "古巴", "台湾", "吉尔吉斯斯坦", "哈萨克斯坦",
                    "哥伦比亚", "土耳其", "塔吉克斯坦", "塞尔维亚", "塞黑", "墨西哥", "奥地利", "委内瑞拉", "孟加拉国",
                    "尼日尔", "巴西", "布基纳法索", "希腊", "德国", "意大利", "挪威", "捷克", "捷克斯洛伐克", "摩洛哥",
                    "摩纳哥", "斯洛伐克", "斯洛文尼亚", "新加坡", "新西兰", "日本", "智利", "朝鲜", "柬埔寨", "格鲁吉亚",
                    "比利时", "毛利塔尼亚", "法国", "波兰", "波多黎各", "波黑", "泰国", "澳大利亚", "澳大利亚Australia", "澳门",
                    "爱尔兰", "爱沙尼亚", "瑞典", "瑞士", "白俄罗斯", "秘鲁", "突尼斯", "立陶宛", "缅甸", "罗马尼亚", "美国",
                    "老挝", "芬兰", "芬兰Finland", "苏联", "英国", "英国BBC", "荷兰", "菲律宾", "葡萄牙", "蒙古",
                    "西德", "西班牙", "越南", "阿尔及利亚", "阿尔巴尼亚", "阿根廷", "阿联酋", "韩国",
                    "香港", "马其顿", "马提尼克", "马来西亚", "马耳他", "黎巴嫩",
                ],
        };
    },
    methods: {
        async fetchPersons(page, pageSize) {
            const searchText = this.searchText;
            const birthYearRange = this.birthYearRange;
            const genderMale = this.genderMale;
            const genderFemale = this.genderFemale;
            try {
                const response = await axios.get('http://127.0.0.1:5001/api/persons', {
                    params: {
                        page: page,
                        pageSize: pageSize,
                        searchText: searchText,
                        birthYearRange: birthYearRange.join(','),
                        genderMale: genderMale,
                        genderFemale: genderFemale,
                    }
                });
                this.persons = response.data.persons;
                this.total = response.data.total;
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