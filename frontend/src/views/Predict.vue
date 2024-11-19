<template>
  <a-form layout="vertical">
    <a-form-item label="导演">
      <a-select
        show-search
        placeholder="选择导演"
        :options="directors"
        v-model="selectedDirector"
      ></a-select>
    </a-form-item>
    <a-form-item label="编剧">
      <a-select
        show-search
        placeholder="选择编剧"
        :options="screenwriters"
        v-model="selectedScreenwriter"
      ></a-select>
    </a-form-item>
    <a-form-item label="主演1">
      <a-select
        show-search
        placeholder="选择主演1"
        :options="actors"
        v-model="selectedActor1"
      ></a-select>
    </a-form-item>
    <a-form-item label="主演2">
      <a-select
        show-search
        placeholder="选择主演2"
        :options="actors"
        v-model="selectedActor2"
      ></a-select>
    </a-form-item>
    <a-button type="primary" @click="predictRating">推测评分</a-button>
  </a-form>
  <div v-if="predictedRating">
    推测评分：{{ predictedRating }}
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { Select, Form } from 'ant-design-vue';
import axios from 'axios';

export default {
  components: {
    'a-select': Select,
    'a-form': Form,
    'a-form-item': Form.Item,
    'a-button': Select.Button,
  },
  setup() {
    const directors = ref([]);
    const screenwriters = ref([]);
    const actors = ref([]);
    const selectedDirector = ref(null);
    const selectedScreenwriter = ref(null);
    const selectedActor1 = ref(null);
    const selectedActor2 = ref(null);
    const predictedRating = ref(null);

    const fetchOptions = async () => {
      const directorRes = await axios.get('http://127.0.0.1:5001/api/persons/directors');
      // console.log(directorRes.data);
      directors.value = directorRes.data.map(item => ({ value: item.id, label: item.name }));

      const screenwriterRes = await axios.get('http://127.0.0.1:5001/api/persons/authors');
      // console.log(screenwriterRes.data);
      screenwriters.value = screenwriterRes.data.map(item => ({ value: item.id, label: item.name }));

      const actorRes = await axios.get('http://127.0.0.1:5001/api/persons/actors');
      // console.log(actorRes.data);
      actors.value = actorRes.data.map(item => ({ value: item.id, label: item.name }));
    };

    const predictRating = () => {
      // 这里可以添加你的逻辑来根据选择的导演、编剧和演员来推测电影评分
      // 例如，可以是一个简单的算法，或者调用后端API获取评分
      predictedRating.value = '8.5'; // 假设的评分
    };

    onMounted(fetchOptions);

    return {
      directors,
      screenwriters,
      actors,
      selectedDirector,
      selectedScreenwriter,
      selectedActor1,
      selectedActor2,
      predictedRating,
      predictRating,
    };
  },
};
</script>