<script setup>
const { $courses, $documents } = useNuxtApp()

const route = useRoute()
const courseId = route.params.id
const chapterIndex = route.params.chapterIndex

const state = reactive({
  course: null
})
state.course = await $courses.getById(courseId)

async function save() {
  state.course = await $courses.save(state.course)
}

async function generateChapterStructure() {
  state.course = await $courses.generateChapterStructure(
    state.course,
    chapterIndex
  )
  return state.course.chapters[chapterIndex].blocks
}

async function generateChapterParagraph(headerIndex) {
  state.course = await $courses.generateChapterParagraph(
    state.course,
    chapterIndex,
    headerIndex
  )
  return state.course.chapters[chapterIndex].blocks
}
</script>

<template>
  <CourseAppBar :course="state.course" />
  <CourseMenu :course="state.course" />

  <v-main class="main">
    <v-container>
      <DocumentEditor
        v-model="state.course.chapters[chapterIndex]"
        @update:modelValue="save"
        :generateStructure="generateChapterStructure"
        :generateParagraph="generateChapterParagraph"
      />
    </v-container>
  </v-main>
</template>

<style scoped>
.main {
  background-color: rgb(249, 251, 253);
}
</style>
