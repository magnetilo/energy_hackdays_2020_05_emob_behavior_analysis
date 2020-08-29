<template>
  <v-container>
    <v-row class="text-center">
      <v-col class="mb-4">
        <h1 class="display-2 font-weight-bold mb-3">
          E-Mobility Behaviour at Home
        </h1>
      </v-col>
    </v-row>
    <v-row>
      <v-col class="mb-5" cols="6">
        <v-card elevation="5">
          <v-card-title>User 15_20</v-card-title>
          <v-card-text>
            <Plotly
              :data="plot1"
              :layout="layout"
              :display-mode-bar="false"
            ></Plotly>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col class="mb-5" cols="6">
        <v-card elevation="5">
          <v-card-title>User 12_17</v-card-title>
          <v-card-text>
            <Plotly
              :data="plot2"
              :layout="layout"
              :display-mode-bar="false"
            ></Plotly>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col class="mb-5" cols="6">
        <v-card elevation="5">
          <v-card-title>User 4_9</v-card-title>
          <v-card-text>
            <Plotly
              :data="plot3"
              :layout="layout"
              :display-mode-bar="false"
            ></Plotly>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col class="mb-5" cols="6">
        <v-card elevation="5">
          <v-card-title>User 6_11</v-card-title>
          <v-card-text>
            <Plotly
              :data="plot4"
              :layout="layout"
              :display-mode-bar="false"
            ></Plotly>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col class="mb-5" cols="6">
        <v-card elevation="5">
          <v-card-title>User 5_10</v-card-title>
          <v-card-text>
            <Plotly
              :data="plot5"
              :layout="layout"
              :display-mode-bar="false"
            ></Plotly>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col class="mb-5" cols="6">
        <v-card elevation="5">
          <v-card-title>User 18_23</v-card-title>
          <v-card-text>
            <Plotly
              :data="plot6"
              :layout="layout"
              :display-mode-bar="false"
            ></Plotly>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col class="mb-5" cols="6">
        <v-card elevation="5">
          <v-card-title>User 5_10</v-card-title>
          <v-card-text>
            <Plotly
              :data="plot7"
              :layout="layout"
              :display-mode-bar="false"
            ></Plotly>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col class="mb-5" cols="6">
        <v-card elevation="5">
          <v-card-title>User 11_16</v-card-title>
          <v-card-text>
            <Plotly
              :data="plot8"
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
      plot1: [],
      plot2: [],
      plot3: [],
      plot4: [],
      plot5: [],
      plot6: [],
      plot7: [],
      plot8: [],
    };
  },
  methods: {
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
          this.datapointsBar = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getPlot1() {
      const path = "http://localhost:5000/plot1";
      axios
        .get(path)
        .then((res) => {
          this.plot1 = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getPlot2() {
      const path = "http://localhost:5000/plot2";
      axios
        .get(path)
        .then((res) => {
          this.plot2 = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getPlot3() {
      const path = "http://localhost:5000/plot3";
      axios
        .get(path)
        .then((res) => {
          this.plot3 = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getPlot4() {
      const path = "http://localhost:5000/plot4";
      axios
        .get(path)
        .then((res) => {
          this.plot4 = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getPlot5() {
      const path = "http://localhost:5000/plot5";
      axios
        .get(path)
        .then((res) => {
          this.plot5 = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getPlot6() {
      const path = "http://localhost:5000/plot6";
      axios
        .get(path)
        .then((res) => {
          this.plot6 = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getPlot7() {
      const path = "http://localhost:5000/plot7";
      axios
        .get(path)
        .then((res) => {
          this.plot7 = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getPlot8() {
      const path = "http://localhost:5000/plot8";
      axios
        .get(path)
        .then((res) => {
          this.plot8 = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getPlot1();
    this.getPlot2();
    this.getPlot3();
    this.getPlot4();
    this.getPlot5();
    this.getPlot6();
    this.getPlot7();
    this.getPlot8();
  },
};
</script>
