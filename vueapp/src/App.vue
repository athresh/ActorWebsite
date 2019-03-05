<template>
<div>
    <nav class="navbar navbar-expand-md navbar-dark fixed-top bg-dark">
      <a class="navbar-brand" href="#">Library</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarCollapse">
        <ul class="navbar-nav mr-auto">

          <li class="nav-item">
          <a class="btn btn-primary" href="/">Home</a>
          </li>
          <li class="nav-item">
          <a class="btn btn-primary" href="/actors">Actors</a>
          </li>

        </ul>

      </div>
    </nav>

    <div class="container">
      <router-view 
        :auth="auth" 
        :authenticated="authenticated">
      </router-view>
    </div>

</div>  
</template>

<script>
/* eslint-disable */

import AuthService from './auth/AuthService'
import {APIService} from './http/APIService';
const API_URL = 'http://localhost:8000';
const auth = new AuthService();
const apiService = new APIService();
const { login, logout, authenticated, authNotifier } = auth

export default {
  name: 'app',
  data () {
    console.log(this.$store)
    /*
    authNotifier.on('authChange', authState => {
      this.authenticated = authState.authenticated
    })
    */
    return {
      auth,
      authenticated
    }
  },
  methods: {
    login,
    logout,
    calculatefines(){
      apiService.calculatefines().then((data)=>{
        alert("Fines updated!");
        this.$router.go();
      })
    }
  }
}
</script>

<style>
@import './assets/bootstrap.min.css';
body {
  min-height: 75rem;
  padding-top: 4.5rem;
  font-size:12px;
  margin-right:0;
  padding-right:0px;
}
.container{
  margin-left: 0px;
  margin-right: 0px;
  padding-right: 0px;
  padding-left: 0px;
  }
h1{
  width:50%;
  font-size:20px;
  margin-left: 0px;
  margin-right: 0px;
  margin-block-start:0em;
}
.nav-item{
  padding:1px;
  margin-left: 5px;
}
</style>
