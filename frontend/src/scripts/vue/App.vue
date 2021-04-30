<template>
  <div id="app">
    <dashboardgrid />
    <hr />
    <hr />
    <hr />
    <hr />
    <hr />
    <br />
    <br />
    <br />
    <h1>Weitere Vue-Komponenten zur Einbindung auf der neuen Website</h1>
    <calendar date="2021-12-03" />
    <loginform />
    <registrationform />
    <userprofilecard />
  </div>
</template>

<script>
import calendar from "./components/calendar";
import userprofilecard from "./components/userprofilecard";
import dashboardgrid from "./components/dashboardgrid";
import loginform from "./components/loginform";
import registrationform from "./components/registrationform";

export default {
  name: "App",
  components: {
    calendar,
    userprofilecard,
    dashboardgrid,
    loginform,
    registrationform,
  },
};
</script>

<style>
</style>
