<template>
  <v-container>
    <v-row class="text-center">
      <v-col class="mb-4">
        <h1 class="display-2 font-weight-bold mb-3">
          Public E-Mobility Behaviour
        </h1>
      </v-col>

      <v-col class="mb-5" cols="12">
        <v-card elevation="5">
          <v-card-title>Occupational Ratio</v-card-title>
          <v-card-text>
            <Plotly
              :data="datapoints"
              :layout="layout"
              :display-mode-bar="false"
            ></Plotly>
          </v-card-text>
        </v-card>
      </v-col>
            <v-col class="mb-5" cols="12">
        <v-card elevation="5">
          <v-card-title>Top Shots Most Occupied</v-card-title>
          <v-card-text>
            <Plotly
              :data="datapoints"
              :layout="layout"
              :display-mode-bar="false"
            ></Plotly>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col class="mb-5" cols="12">
        <v-card elevation="5">
          <v-card-title>Regional Occupation (MAP)</v-card-title>
          <v-card-text>
            <Plotly
              :data="datapoints1"
              :layout="layoutMap"
              :display-mode-bar="false"
            ></Plotly>
          </v-card-text>
        </v-card>
      </v-col>
            <v-col class="mb-5" cols="12">
        <v-card elevation="5">
          <v-card-title>Occupation Over Time</v-card-title>
          <v-card-text>
            <Plotly
              :data="datapoints"
              :layout="layout"
              :display-mode-bar="false"
            ></Plotly>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col class="mb-5" cols="12">
        <v-card elevation="5">
          <v-card-title>Duration Time of Charging (MAP)</v-card-title>
          <v-card-text>
            <Plotly
              :data="datapoints1"
              :layout="layoutMap"
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
import axios from 'axios';

export default {
  name: "HelloWorld",
  components: {
    Plotly,
  },
  data: function() {
    return {
      datapoints: [],
      layout: {},
      datapoints1: [
        {
          type: "scattermapbox",
          lon: [8, 8.1],
          lat: [47, 46.8],
          marker: { color: "red", size: 5 },
        },
      ],
      layoutMap: {
        dragmode: "zoom",
        mapbox: {
          style: "open-street-map",
          center: { lat: 46.8, lon: 8 },
          zoom: 6.5,
        },
        margin: { r: 0, t: 0, b: 0, l: 0 },
      },
      options: {},
    };
  },
  methods: {
    getMessage() {
      const path = 'http://localhost:5000/';
      axios.get(path)
        .then((res) => {
          this.datapoints = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getMessage();
  },
};
</script>
