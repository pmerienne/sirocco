<template>
  <v-toolbar
    density="compact"
    collapse
    class="toolbar"
    floating
    color="primary"
  >
    <v-tooltip text="Generate structure">
      <template v-slot:activator="{ props }">
        <v-btn
          v-bind="props"
          icon="mdi-refresh-auto"
          @click="generateStructure"
        />
      </template>
    </v-tooltip>
    <v-btn icon="mdi-cog"> </v-btn>

    <v-progress-linear
      :active="state.loading"
      :indeterminate="state.loading"
      absolute
      bottom
      color="white"
    />
  </v-toolbar>

  <div class="editor">
    <v-overlay
      v-model="state.loading"
      contained
      persistent
      class="align-center justify-center"
    />
    <h2 class="text-h2">{{ props.modelValue.title }}</h2>
    <!-- TODO: Side menu with anchor links (https://codepen.io/RafaS1/pen/LYrQKZr) -->
    <div :id="holder" ref="holder"></div>
  </div>
</template>

<script setup>
import Header from "@editorjs/header"
// import Paragraph from "@editorjs/paragraph"
import EditorJS from "@editorjs/editorjs"

const { $documents, $courses } = useNuxtApp()

class BlogHeader extends Header {
  renderSettings() {
    const basicSettings = super.renderSettings()
    basicSettings.unshift({
      icon: '<i class="mdi mdi-plus text-primary" />',
      label: "Generate",
      onActivate: () => generateParagraph(),
      closeOnActivate: true,
      isActive: false
    })

    return basicSettings
  }
}

const holder = ref(null)
const emit = defineEmits(["update:modelValue"])

// For v-model
const props = defineProps({
  modelValue: Object,
  modelModifiers: { default: () => ({}) },

  generateStructure: { type: Function },
  generateParagraph: { type: Function }
})
const state = reactive({ editor: null, loading: false })

onMounted(async () => {
  state.editor = new EditorJS({
    autofocus: true,
    holder: holder.value,
    onChange: onChange,
    data: { blocks: props.modelValue.blocks },
    tools: {
      header: {
        class: BlogHeader
      }
    }
  })
})

async function onChange() {
  // Get blocks data
  const { blocks } = await state.editor.save()
  // Update v-model
  props.modelValue.blocks = blocks
  // Emit update
  emit("update:modelValue", props.modelValue)
}

async function generateStructure() {
  state.loading = true
  document.blocks = await props.generateStructure()
  state.editor.render(document)
  state.loading = false
}

async function generateParagraph() {
  state.loading = true
  const headerIndex = state.editor.blocks.getCurrentBlockIndex()
  document.blocks = await props.generateParagraph(headerIndex)
  state.editor.render(document)
  state.loading = false
}

onUnmounted(() => {
  if (state.editor) {
    state.editor.destroy()
    state.editor = null
  }
})
</script>

<style scoped>
.toolbar {
  position: absolute;
  z-index: 999 !important;
}

.editor {
  position: relative; /* for overlay */
  background-color: white;
  border: 1px gray solid;
  padding: 60px 124px 60px 124px;
}
</style>

<style>
.ce-block__content,
.ce-toolbar__content {
  max-width: unset; /* calc(100% - 124px) !important; */
}
.cdx-block {
  /* max-width: 100% !important; */
}
</style>
