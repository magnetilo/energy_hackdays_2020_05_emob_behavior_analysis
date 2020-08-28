<template>
  <v-container>
    <v-row class="text-center">
      <v-col class="mb-4">
        <h1 class="display-2 font-weight-bold mb-3">
          E-Mobility Behaviour at Home {{msg}}
        </h1>
      </v-col>

      <v-col class="mb-5" cols="12">
        <v-card elevation="5">
          <v-card-title>Dummy Plot</v-card-title>
          <v-card-text>
            <Plotly
              :data="datapoints"
              :layout="layout"
              :display-mode-bar="true"
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
  name: "PrivateChargingStations",
  components: {
    Plotly,
  },
  data: function() {
    return {
      msg: "",
      datapoints: [{ x: [1, 7, 7, 15, 16, 21], y: [2, 3, 4, 7, 9, 13] }],
      layout: {},
      options: {},
    };
  },
  methods: {
    getMessage() {
      const path = 'http://localhost:5000/private';
      axios.get(path)
        .then((res) => {
          this.msg = res.data;
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
