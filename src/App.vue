<template>
  <router-view/>
</template>

<script>
export default {
  created() {
    this.downloadData()
  },
  methods: {
    downloadData () {
      Vue.http.get('http://localhost:8000/api/root/')
        .then(response => response.json())
        .then(data => {
          this.$store
          this.$router.push('/define')
        })
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
