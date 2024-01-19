<template>
  <CourseAppBar :course="state.course" />
  <CourseMenu :course="state.course" />

  <v-main>
    <v-container class="pt-0">
      <h1>Table of contents</h1>
      <draggable v-model="state.course.chapters" item-key="id">
        <template #item="{ element, index }">
          <v-text-field
            variant="solo"
            v-model="element.title"
            append-inner-icon="mdi-refresh-auto"
            :loading="state.generating.chapters"
            :disabled="state.generating.chapters"
            @click:append-inner="regenerateChapter(index)"
            @input="save()"
          >
            <template v-slot:prepend-inner>
              <v-icon
                color="primary"
                :icon="`mdi-numeric-${index + 1}-box-outline`"
                size="x-large"
              />
            </template>
          </v-text-field>
        </template>
      </draggable>

      <div class="d-flex justify-center">
        <v-btn
          variant="text"
          size="x-large"
          icon="mdi-plus-circle-outline"
          color="secondary"
          :loading="state.generating.chapters"
          :disabled="state.generating.chapters"
          @click="createChapter"
        />
        <v-btn
          variant="text"
          size="x-large"
          icon="mdi-plus-circle-multiple-outline"
          color="primary"
          :loading="state.generating.chapters"
          :disabled="state.generating.chapters"
          @click="generateChapters"
        />
      </div>
    </v-container>
  </v-main>
</template>

<script setup>
const { $courses, $documents } = useNuxtApp()
const route = useRoute()
const state = reactive({
  generating: {
    chapters: false
  },
  course: null
})

state.course = await $courses.getById(route.params.id)

async function save() {
  state.course = await $courses.save(state.course)
}

async function createChapter() {
  state.generating.chapters = true
  state.course = await $courses.createChapter(state.course)
  state.generating.chapters = false
}

async function generateChapters() {
  state.generating.chapters = true
  state.course = await $courses.generateChapters(state.course)
  state.generating.chapters = false
}

async function regenerateChapter(index) {
  state.generating.chapters = true
  state.course = await $courses.regenerateChapter(state.course, index)
  state.generating.chapters = false
}
</script>
