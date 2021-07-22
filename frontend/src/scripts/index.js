import "../styles/index.scss";

import $ from "jquery/dist/jquery.slim";
import "bootstrap/dist/js/bootstrap.bundle";
import * as moment from 'moment';


import Vue from "vue";
import Vuetify from "vuetify";
import calendar from "./vue/dashboard/calendar.vue";

// Vue.config.productionTip = true;

// new Vue({
//   render: (h) => h(calendar),
// }).$mount("calendar");

new Vue({
  render: (h) => h(calendar),
}).$mount("calendar");


$(document).ready(function () {
  window.console.log("dom ready");
});
