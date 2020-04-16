<template>
  <div class="container">
    <!-- <div>
      <logo />
      <h1 class="title">
        dashboard_frontend
      </h1>
      <h2 class="subtitle">
        My fantastic Nuxt.js project
      </h2>
      <div class="links">
        <a href="https://nuxtjs.org/" target="_blank" class="button--green">
          Documentation
        </a>
        <a href="https://github.com/nuxt/nuxt.js" target="_blank" class="button--grey">
          GitHub
        </a>
      </div>
    </div> -->
    <p v-for="(value, name, index) in results.Canada" :key="value.date">
        <!-- {{value[index].sum}} -->
        {{ value.sum }}
      </p>
  </div>
</template>

<script>
  import Logo from '~/components/Logo.vue'
  import session from '../store/api/session';
  import * as d3 from 'd3'
  export default {
    components: {
      Logo
    },
    data() {
      return {
        results: [],
        error: null
      };
    },
    created() {
      this.getTable()
    },
    methods: {
      getTable() {
        session.get('/country/Canada/Deaths/')
          .then(response => (this.results = response.data));
      },
      fetchData() {
        this.error = this.post = null
        this.loading = true
        const url_base = '/continent/'
        // console.log(url)
        session.get(url_base)
          .then(response => (this.results = response.data))
        console.log(this.results)
        // replace `getPost` with your data fetching util / API wrapper
        // session.get(url, (err, post) => {
        //     console.log(url)
        //     this.loading = false
        //     if (err) {
        //         this.error = err.toString()
        //     } else {
        //         this.post = post
        //     }
        // })
      },

    }
  }
</script>

<style>
  .container {
    margin: 0 auto;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
  }

  .title {
    font-family: 'Quicksand', 'Source Sans Pro', -apple-system, BlinkMacSystemFont,
      'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    display: block;
    font-weight: 300;
    font-size: 100px;
    color: #35495e;
    letter-spacing: 1px;
  }

  .subtitle {
    font-weight: 300;
    font-size: 42px;
    color: #526488;
    word-spacing: 5px;
    padding-bottom: 15px;
  }

  .links {
    padding-top: 15px;
  }
</style>