<script setup>
const { $courses } = useNuxtApp()

const props = defineProps({
  course: {
    require: true
  }
})
</script>

<template>
  <v-navigation-drawer permanent>
    <v-list>
      <v-list-item title="Informations" :to="`/courses/${props.course.id}`">
        <template v-slot:prepend>
          <v-icon icon="mdi-information-box-outline"></v-icon>
        </template>
      </v-list-item>

      <v-list-item
        title="Table of contents"
        :to="`/courses/${props.course.id}/table-of-contents`"
      >
        <template v-slot:prepend>
          <v-icon icon="mdi-table-of-contents"></v-icon>
        </template>
      </v-list-item>
      <v-divider />

      <v-list-item
        v-for="(chapter, index) in props.course.chapters"
        :key="chapter.id"
        :title="chapter.title"
        :to="`/courses/${props.course.id}/chapters/${index}`"
      >
        <template v-slot:prepend>
          <v-icon :icon="`mdi-numeric-${index + 1}-box-outline`"></v-icon>
        </template>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>
