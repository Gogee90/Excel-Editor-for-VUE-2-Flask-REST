<template>
  <div class="fixed-top d-flex align-items-center justify-content-center"
       style="bottom: 0; overflow-y: auto">
    <b-card style="max-width: 600px;">
      <b-form-group
          id="fieldset-1"
          label="Login"
          label-for="input-1"
      >
        <b-form-input id="input-1" v-model="email"></b-form-input>
      </b-form-group>
      <b-form-group
          id="fieldset-1"
          label="Password"
          label-for="input-1"
      >
        <b-form-input type="password" id="input-2" v-model="password"></b-form-input>
      </b-form-group>
      <b-button style="margin-top: 15px" @click="authenticate">Login</b-button>
    </b-card>
  </div>
</template>

<script>
export default {
  name: "Login",
  data() {
    return {
      email: '',
      password: ''
    }
  },
  methods: {
    authenticate() {
      let credentials = {'email': this.email, 'password': this.password}
      fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(credentials)
      }).then(response => {
        return response.json()
      }).then(data => {
        localStorage.setItem('authenticated', data.authenticated)
        this.$router.push({name: 'Index'})
      })
    }
  }
}
</script>

<style scoped>

</style>