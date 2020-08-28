<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      Energy Hackdays 2020
      <v-spacer></v-spacer>
      <v-btn
      class="mr-2 black"
      ><router-link to="/" class="white--text">Public Charging Stations</router-link></v-btn>
      <v-btn
      class="black"
      ><router-link to="/private" class="white--text">Private Charging Stations</router-link></v-btn>
    </v-app-bar>

    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>

export default {
  name: "App",

  components: {
  },

  data: () => ({
    //
  }),
};
</script>
