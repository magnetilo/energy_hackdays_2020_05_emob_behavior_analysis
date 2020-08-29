<template>
  <v-container>
    <v-row class="text-center">
      <v-col class="mb-4">
        <h1 class="display-2 font-weight-bold mb-3">
          E-Mobility Behaviour at Home
        </h1>
      </v-col>

      <v-col class="mb-5" cols="12">
        <v-card elevation="5">
          <v-card-title>Dummy Line Plot</v-card-title>
          <v-card-text>
            <Plotly
              :data="datapoints"
              :layout="layout"
              :display-mode-bar="true"
            ></Plotly>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col class="mb-5" cols="12">
        <v-card elevation="5">
          <v-menu>
            <template v-slot:activator="{ on, attrs }">
              <v-btn color="primary" dark v-bind="attrs" v-on="on">
                Dropdown
              </v-btn>
            </template>
            <v-list>
              <v-list-item
                v-for="(item, index) in items"
                :key="index"
                @click="getOneBar(index + 1)"
              >
                <v-list-item-title>{{ item.title }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
          <v-card-title>Dummy Bar Plot</v-card-title>
          <v-card-text>
            <Plotly
              :data="datapointsBar"
              :layout="layout"
              :display-mode-bar="false"
            ></Plotly>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { Plotly } from "vue-plotly";
import axios from "axios";

export default {
  name: "PrivateChargingStations",
  components: {
    Plotly,
  },
  data: function() {
    return {
      datapoints: [],
      layout: {},
      datapointsBar: [],
      options: {},
      items: [
        { title: "id 1" },
        { title: "id 2" },
        { title: "id 3" },
        { title: "id 4" },
      ],
    };
  },
  methods: {
    getLine() {
      const path = "http://localhost:5000/private";
      axios
        .get(path)
        .then((res) => {
          this.datapoints = [res.data];
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getOneBar(id) {
      const path = "http://localhost:5000/private";
      const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        id: id,
      };
      axios
        .post(path, requestOptions)
        .then((res) => {
          this.datapointsBar = [res.data];
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getLine();
  },
};
</script>
