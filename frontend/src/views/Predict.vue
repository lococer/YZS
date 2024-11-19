<template>
    <div>
    <h1>Predict</h1>
  </div>
  <div>
    <rating-pie :ratings="ratings" />
  </div>
</template>

<script>
import ratingPie from '../components/MoviesRatingPie.vue';

export default {
  name: 'Predict',
  data() {
    return {
      ratings: [
        { name: "8分以上", value: 50 },
        { name: "6-8分", value: 30 },
        { name: "6分以下", value: 20 },
      ],
    };
  },
  components: {
    ratingPie,
  },
}
</script>

<style scoped>
</style>