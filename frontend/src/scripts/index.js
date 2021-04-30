import "../styles/index.scss";

import $ from "jquery/dist/jquery.slim";
import "bootstrap/dist/js/bootstrap.bundle";
import moment from "moment";


import Vue from "vue";
import Calendar from "./vue/calendar.vue";

Vue.config.productionTip = true;

new Vue({
  render: (h) => h(HelloWorld),
}).$mount("#calendar");


$(document).ready(function () {
  window.console.log("dom ready");
});
