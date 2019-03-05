<template lang="html">
  <form class="login form">
    <div class="field">
      <label for="id_username">Username</label>
      <input
        v-model="username"
        type="text"
        placeholder="Username"
        autofocus="autofocus"
        maxlength="150"
        id="id_username">
    </div>
    <div class="field">
      <label for="id_password">Password</label>
      <input
        v-model="password"
        type="password"
        placeholder="Password"
        id="id_password">
    </div>
    <button
      @click.prevent="authenticate"
      class="btn btn-primary"
      type="submit">
      Log In
    </button>
  </form>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    authenticate () {
      const payload = {
        username: this.username,
        password: this.password
      }
      axios.post(this.$store.state.endpoints.obtainJWT, payload)
        .then((response) => {
          this.$store.commit('updateToken', response.data.token)
          // get and set auth user
          const base = {
            baseURL: this.$store.state.endpoints.baseUrl,
            headers: {
            // Set your Authorization to 'JWT', not Bearer!!!
              Authorization: `JWT ${this.$store.state.jwt}`,
              'Content-Type': 'application/json'
            },
            xhrFields: {
                withCredentials: true
            }
          }
          this.$store.commit("setAuthUser",
                {authUser: this.username, isAuthenticated: true}
              )
              this.$router.push({name: 'Home'})
          // Even though the authentication returned a user object that can be
          // decoded, we fetch it again. This way we aren't super dependant on
          // JWT and can plug in something else.
          //const axiosInstance = axios.create(base)
          /*
          axiosInstance({
            url: "/user/",
            method: "get",
            params: {}
          })
            .then((response) => {
              this.$store.commit("setAuthUser",
                {authUser: response.data, isAuthenticated: true}
              )
              this.$router.push({name: 'Home'})
            })
            */

        })
        /*
        .then((response)=>{
          this.$store.commit("setAuthUser",
                {authUser: response.data, isAuthenticated: true}
              )
          this.$router.push({name:'Home'})
        })
        */
        .catch((error) => {
          console.log(error);
          console.debug(error);
          console.dir(error);
        })
        
    }
  }
}
</script>

<style lang="css">
.list-horizontal li {
	display:inline;
}
.list-horizontal li:before {
	content: '\00a0\2022\00a0\00a0';
	color:#999;
	color:rgba(0,0,0,0.5);
	font-size:11px;
}
.list-horizontal li:first-child:before {
	content: '';
}
</style>