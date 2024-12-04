<template>
  <a-form layout="vertical">
    <a-form-item label="导演">
      <a-select
        mode="tags"
        style="width: 100%"
        :max-tag-count="1"
        :max-tag-text="() => '最多只能选择一个'"
        placeholder="选择导演"
        :options="directors"
        v-model:value="selectedDirector"
        @change="handleDirectorChange"
      ></a-select>
    </a-form-item>
    <a-form-item label="编剧">
      <a-select
        mode="tags"
        style="width: 100%"
        :max-tag-count="1"
        :max-tag-text="() => '最多只能选择一个'"
        placeholder="选择编剧"
        :options="screenwriters"
        v-model:value="selectedScreenwriter"
        @change="handleScreenwriterChange"
      ></a-select>
    </a-form-item>
    <a-form-item label="主演1">
      <a-select
        mode="tags"
        style="width: 100%"
        :max-tag-count="1"
        :max-tag-text="() => '最多只能选择一个'"
        placeholder="选择主演1"
        :options="actors"
        v-model:value="selectedActor1"
        @change="handleActor1Change"
      ></a-select>
    </a-form-item>
    <a-form-item label="主演2">
      <a-select
        mode="tags"
        style="width: 100%"
        :max-tag-count="1"
        :max-tag-text="() => '最多只能选择一个'"
        placeholder="选择主演2"
        :options="actors"
        v-model:value="selectedActor2"
        @change="handleActor2Change"
      ></a-select>
    </a-form-item>
    <a-form-item label="类型">
      <a-select
        mode="tags"
        style="width: 100%"
        placeholder="选择类型"
        :options="genre"
        v-model:value="selectedGenre"
        @change="handleChange"
      ></a-select>
    </a-form-item>
    <a-button type="primary" @click="predictRating">推测评分</a-button>
  </a-form>
  <div v-if="predictedRating">
    推测评分：{{ predictedRating }}
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue';
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
    const selectedDirector = ref([]);
    const selectedScreenwriter = ref([]);
    const selectedActor1 = ref([]);
    const selectedActor2 = ref([]);
    const predictedRating = ref(null);
    const genre = ref([]);
    const selectedGenre = ref([]);

    // const options = [...Array(25)].map((_, i) => ({
    //   value: (i + 10).toString(36) + (i + 1), label: `Option ${i + 1}`,
    // }));
    const options = [
      { value: '1', label: 'Option 1' },
      { value: '2', label: 'Option 2' },
      { value: '3', label: 'Option 3' },
      { value: '4', label: 'Option 4' },
      { value: '13', label: 'Option 13' }
    ];

    const handleChange = value => {
      console.log(`selected ${value}`);
    };

    // 处理导演变化
    const handleDirectorChange = (value) => {
      console.log('Selected director:', value);
      selectedDirector.value = value;
    };

    // 监听selectedDirector变化，确保不超过一个选择
    watch(selectedDirector, (newVal) => {
      if (newVal.length > 1) {
        selectedDirector.value = [newVal[0]]; // 只保留第一个选择
      }
    });

    // 处理编剧变化
    const handleScreenwriterChange = (value) => {
      selectedScreenwriter.value = value;
    };

    watch(selectedScreenwriter, (newVal) => {
      if (newVal.length > 1) {
        selectedScreenwriter.value = [newVal[0]]; // 只保留第一个选择
      }
    });

    // 处理主演1变化
    const handleActor1Change = (value) => {
      selectedActor1.value = value;
    };

    watch(selectedActor1, (newVal) => {
      if (newVal.length > 1) {
        selectedActor1.value = [newVal[0]]; // 只保留第一个选择
      }
    });

    // 处理主演2变化
    const handleActor2Change = (value) => {
      selectedActor2.value = value;
    };

    watch(selectedActor2, (newVal) => {
      if (newVal.length > 1) {
        selectedActor2.value = [newVal[0]]; // 只保留第一个选择
      }
    });

    const predictRating = async () => {
      // 获取选择的id
      const directorName = selectedDirector.value;
      const screenwriterName = selectedScreenwriter.value;
      const actor1Name = selectedActor1.value;
      const actor2Name = selectedActor2.value;
      const genreName = selectedGenre.value;

      console.log('Predicting rating for:', directorName, screenwriterName, actor1Name, actor2Name, genreName);

      // 调用后端API获取评分，这里假设API为 http://127.0.0.1:5001/api/predict-rating
      // 并假设它接受导演、编剧和两个主演的id作为参数
      try {
        const response = await axios.get('http://127.0.0.1:5001/api/predict-rating', {
          params:{
            director: selectedDirector.value,
            autor: selectedScreenwriter.value,
            actor1: selectedActor1.value,
            actor2: selectedActor2.value,
            genre: selectedGenre.value,
          }
        });
        predictedRating.value = response.data; // 假设返回的评分在response.data中
      } catch (error) {
        console.error('Error predicting rating:', error);
        predictedRating.value = 'Failed to predict rating';
      }
    };

    const fetchOptions = async () => {
      const directorRes = await axios.get('http://127.0.0.1:5001/api/persons/directors');
      directors.value = directorRes.data.map(item => ({ value: item.name, label: item.name }));

      const screenwriterRes = await axios.get('http://127.0.0.1:5001/api/persons/authors');
      screenwriters.value = screenwriterRes.data.map(item => ({ value: item.name, label: item.name }));

      const actorRes = await axios.get('http://127.0.0.1:5001/api/persons/actors');
      actors.value = actorRes.data.map(item => ({ value: item.name, label: item.name }));

      const genreRes = await axios.get('http://127.0.0.1:5001/api/movies/genres');
      genre.value = genreRes.data.map(item => ({ value: item, label: item }));
      
      // genre.value = [ {value:'动作', label:'动作'}, {value:'喜剧', label:'喜剧'} ];
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
      handleChange,
      handleDirectorChange,
      handleScreenwriterChange,
      handleActor1Change,
      handleActor2Change,
      options,
      genre,
      selectedGenre,
    };
  },
};
</script>