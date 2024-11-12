<template>
  <div>
    <h1>{{ person.name }}</h1>
    <img :src="fetchImage(person.img)" alt="cover" />
    <p>Rating: {{ person.rating }}</p>
    <p>{{ person.description }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: ['id'],
  data() {
    return {
      person: {}
    };
  },
  async created() {
    try {
      const response = await axios.get(`http://127.0.0.1:5001/api/persons/${this.id}`);
      this.person = response.data;
    } catch (error) {
      console.error("Error fetching person details:", error);
    }
  },
  methods: {
    fetchImage(imageUrl) {
        return `http://127.0.0.1:5001/proxy-image/${imageUrl}`;
    }
  }
};
</script>