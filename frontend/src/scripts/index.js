import "../styles/index.scss";

import $ from "jquery/dist/jquery.slim";
import "bootstrap/dist/js/bootstrap.bundle";

import Vue from "vue";
//import Vue from "vue/dist/vue.esm.js";
import HelloWorld from "./vue/HelloWorld.vue";

Vue.config.productionTip = true;

new Vue({
  render: (h) => h(HelloWorld),
}).$mount("#hello-world");

//createApp(App).mount('#hello-world')

alert('test');

$(document).ready(function () {
  window.console.log("dom ready");
});
