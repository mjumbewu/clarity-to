<template>
  <div>
    <h1>Build Your Platform</h1>
    <p>I'm concerned about&hellip;</p>

    <div class="categories">
      <root-category-button
        v-for="category in rootCategories"
        :key="category.id"
        :icon="category.icon"
        :label="category.label"
      ></root-category-button>
    </div>
  </div>
</template>

<script>
import RootCategoryButton from '@/components/RootCategoryButton.vue'

export default {
  components: {
    'root-category-button': RootCategoryButton
  },
  props: {
    rootCategories: Array
  }
}
</script>