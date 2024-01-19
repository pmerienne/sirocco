<template>
  <v-app-bar density="comfortable" elevation="0">
    <v-app-bar-title>Courses > {{ props.course.name }}</v-app-bar-title>
    <template v-slot:append>
      <v-btn icon="mdi-dots-vertical"></v-btn>
    </template>
  </v-app-bar>
</template>

<script setup>
const props = defineProps({
  course: {
    require: true
  }
})
</script>
