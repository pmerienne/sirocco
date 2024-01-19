<template>
  <CourseAppBar :course="state.course" />
  <CourseMenu :course="state.course" />

  <v-main>
    <v-container class="pt-0">
      <h1>Informations</h1>
      <v-text-field
        label="Name"
        variant="solo"
        v-model="state.course.name"
        append-inner-icon="mdi-refresh-auto"
        :loading="state.generating.name"
        :disabled="state.generating.name"
        @click:append-inner="generateInfo('name')"
        @input="save"
      />
      <v-combobox
        label="Topics"
        multiple
        chips
        closable-chips
        variant="solo"
        v-model="state.course.topics"
        append-inner-icon="mdi-refresh-auto"
        :loading="state.generating.topics"
        :disabled="state.generating.topics"
        @click:append-inner="generateInfo('topics')"
        @update:modelValue="save"
      />
      <v-textarea
        label="Description"
        variant="outlined"
        v-model="state.course.description"
        append-inner-icon="mdi-refresh-auto"
        auto-grow
        :loading="state.generating.description"
        :disabled="state.generating.description"
        @click:append-inner="generateInfo('description')"
        @input="save"
      />
    </v-container>
  </v-main>
</template>

<script setup>
const { $courses, $documents } = useNuxtApp()
const route = useRoute()

const state = reactive({
  generating: {
    name: false,
    topics: false,
    description: false
  },
  course: null
})
state.course = await $courses.getById(route.params.id)

async function save() {
  state.course = await $courses.save(state.course)
}

async function generateInfo(fieldName) {
  state.generating[fieldName] = true
  state.course = await $courses.generateInfo(state.course, fieldName)
  state.generating[fieldName] = false
}
</script>
