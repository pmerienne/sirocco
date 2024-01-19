<template>
  <v-navigation-drawer>
    <div class="pa-2" v-if="document">
      <v-text-field
        v-model="document.title"
        label="title"
        @input="saveDocument"
      />
      <v-textarea
        label="Description"
        variant="outlined"
        v-model="document.description"
        @input="saveDocument"
      />
    </div>
  </v-navigation-drawer>

  <v-main>
    <div :id="holder" ref="holder"></div>
  </v-main>
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

const props = defineProps({
  documentId: {
    type: String,
    require: true
  },
  config: {
    type: Object,
    default: () => ({}),
    require: true
  }
})

const state = reactive({ editor: null, loading: false })
const document = await $documents.getById(props.documentId)

async function saveDocument() {
  const { blocks } = await state.editor.save()
  document.blocks = blocks
  await $documents.save(document)
}

onMounted(async () => {
  state.editor = new EditorJS({
    autofocus: true,
    holder: holder.value,
    onChange: saveDocument,
    data: { blocks: document.blocks },
    tools: {
      header: {
        class: BlogHeader
      }
    },
    ...props.config
  })
})

async function generateParagraph() {
  state.loading = true
  const headerIndex = state.editor.blocks.getCurrentBlockIndex()
  const { blocks } = await $courses.generateParagraph(document.id, headerIndex)
  document.blocks = blocks
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
