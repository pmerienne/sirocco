<script setup>
const { $courses } = useNuxtApp()

const courses = await $courses.findAll()

async function createCourse() {
  const course = await $courses.create()
  navigateTo(`/courses/${course.id}`)
}
</script>

<template>
  <v-app-bar density="comfortable" elevation="0">
    <v-app-bar-title>Courses</v-app-bar-title>
    <template v-slot:append>
      <v-btn icon="mdi-dots-vertical"></v-btn>
    </template>
  </v-app-bar>

  <v-navigation-drawer permanent>
    <div class="pa-2">
      <v-btn
        block
        color="primary"
        prepend-icon="mdi-plus"
        @click="createCourse"
      >
        New
      </v-btn>
    </div>
    <v-list>
      <v-list-item title="Home" value="contacts">
        <template v-slot:prepend>
          <v-icon icon="mdi-home"></v-icon>
        </template>
      </v-list-item>

      <v-list-item title="Recent" value="contacts">
        <template v-slot:prepend>
          <v-icon icon="mdi-clock"></v-icon>
        </template>
      </v-list-item>

      <v-list-item title="Starred" value="contacts">
        <template v-slot:prepend>
          <v-icon icon="mdi-star-outline"></v-icon>
        </template>
      </v-list-item>

      <v-list-item title="Settings" value="contacts">
        <template v-slot:prepend>
          <v-icon icon="mdi-cog"></v-icon>
        </template>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>

  <v-main>
    <v-container class="pt-0">
      <v-list lines="two">
        <v-list-subheader inset>Courses</v-list-subheader>
        <v-list-item
          v-for="course in courses"
          :key="course.id"
          :title="course.name"
          :subtitle="new Date(course.created_at).toDateString()"
          :to="`/courses/${course.id}`"
        >
          <template v-slot:prepend>
            <v-avatar color="primary">
              <v-icon color="white">mdi-bookmark-box-multiple</v-icon>
            </v-avatar>
          </template>

          <template v-slot:append>
            <v-btn
              color="grey-lighten-1"
              icon="mdi-information"
              variant="text"
            ></v-btn>
          </template>
        </v-list-item>
      </v-list>
    </v-container>
  </v-main>
</template>
