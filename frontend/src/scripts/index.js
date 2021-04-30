import "../styles/index.scss";

import $ from "jquery/dist/jquery.slim";
import "bootstrap/dist/js/bootstrap.bundle";
import moment from "moment";


import Vuetify from "vue";
import Vue from "vuetify";
import calendar from "./vue/calendar.vue";

Vue.config.productionTip = true;

new Vue({
  render: (h) => h(calendar),
}).$mount("calendar");


$(document).ready(function () {
  window.console.log("dom ready");
});
