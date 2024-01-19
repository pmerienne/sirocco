<template>
  <v-app>
    <v-navigation-drawer rail>
      <v-list>
        <v-list-item
          prepend-avatar="/moi.jpeg"
          title="Pierre Merienne"
          subtitle="pierre@gmailcom"
          to="/"
          :active="false"
        />
      </v-list>

      <v-divider></v-divider>

      <v-list density="compact" nav>
        <v-list-item prepend-icon="mdi-library" to="/courses" />
        <v-list-item prepend-icon="mdi-folder-multiple" />
      </v-list>
    </v-navigation-drawer>

    <slot></slot>
  </v-app>
</template>
