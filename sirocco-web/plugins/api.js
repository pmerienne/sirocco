const BASE_URL = "http://localhost:5000" // TODO $env

class Documents {
  async findAll() {
    const documents = await $fetch(`${BASE_URL}/documents`)
    return documents
  }

  async findAllFolders() {
    const folders = await $fetch(`${BASE_URL}/documents/folders`)
    return folders
  }

  async getById(id) {
    // TODO: document should be passed to editor
    const document = await $fetch(`${BASE_URL}/documents/${id}`)
    return document
  }

  async save(document) {
    await $fetch(`http://localhost:5000/documents/${document.id}`, {
      method: "PUT",
      body: document
    })
  }

  async generateParagraph(documentId, headerIndex) {
    const blocks = await $fetch(`${BASE_URL}/courses/${documentId}/paragraph`, {
      method: "PUT",
      body: {
        header_index: headerIndex
      }
    })
    return blocks
  }
}

class Courses {
  async create(description) {
    const document = await $fetch(`${BASE_URL}/courses/`, {
      method: "POST",
      body: {
        description: description
      }
    })
    return document
  }

  async findAll() {
    const courses = await $fetch(`${BASE_URL}/courses`)
    return courses
  }

  async getById(id) {
    // TODO: document should be passed to editor
    const course = await $fetch(`${BASE_URL}/courses/${id}`)
    return course
  }

  async save(course) {
    return await $fetch(`${BASE_URL}/courses/${course.id}`, {
      method: "PUT",
      body: course
    })
  }

  async generateInfo(course, fieldName) {
    return await $fetch(`${BASE_URL}/courses/${course.id}/info/${fieldName}`, {
      method: "PUT"
    })
  }

  async createChapter(course) {
    return await $fetch(`${BASE_URL}/courses/${course.id}/chapters`, {
      method: "POST" // TODO: POST vs. PUT ==> LOL
    })
  }

  async generateChapters(course) {
    return await $fetch(`${BASE_URL}/courses/${course.id}/chapters`, {
      method: "PUT" // TODO: POST vs. PUT ==> LOL
    })
  }

  async regenerateChapter(course, index) {
    return await $fetch(`${BASE_URL}/courses/${course.id}/chapters/${index}`, {
      method: "PUT"
    })
  }

  async generateChapterStructure(course, index) {
    return await $fetch(
      `${BASE_URL}/courses/${course.id}/chapters/${index}/structure`,
      {
        method: "PUT"
      }
    )
  }

  async generateChapterParagraph(course, chapterIndex, headerIndex) {
    return await $fetch(
      `${BASE_URL}/courses/${course.id}/chapters/${chapterIndex}/paragraph/${headerIndex}`,
      {
        method: "PUT"
      }
    )
  }
}

export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.provide("documents", new Documents())
  nuxtApp.provide("courses", new Courses())
})
