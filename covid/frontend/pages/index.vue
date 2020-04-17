<template>
  <div class="page-container">
    <article class="pa3 pa5-ns">
      <h1 class="f3 f2-m f1-l">{{location_type}}: {{location_value}}</h1>
      <p class="measure lh-copy">
        This is a count over time of all {{ case_type }} in {{ location_value }}
      </p>
    </article>
    
    <div class="container">
      <chart v-if="loaded" :chart-data="case_counts" :chart-labels="labels" :styles="myStyles"></chart>
      <div class="error-message" v-if="showError">
        {{ errorMessage }}
      </div>
    </div>
  </div>
</template>

<script>
  import Chart from '~/components/Chart.vue'
  import session from '../store/api/session';
  import * as d3 from 'd3'
  export default {
    components: {
      Chart
    },
    data() {
      return {
        ids: [],
        case_counts: [],
        labels: [],
        case_type: '',
        location_type: '',
        location_value: '',
        loaded: false,
        showError: false,
        errorMessage: 'There is an error, and this is the default message',
        query_result: [],
        error: null,
        height: 300
      };
    },
    created() {
      this.getTable()
    },
    methods: {
      getTable() {
        session.get('/country/Germany/Confirmed/')
          .then(response => {
            console.log(response)
            this.case_counts = response.data.counts.map(count => count)
            this.labels = response.data.dates.map(date => date)
            this.location_type = response.data.location_type
            this.location_value = response.data.location_value
            this.case_type = response.data.case_type
            this.loaded = true
          })
          .catch(err => {
            this.errorMessage = err
            this.showError = true
          })
      },
      increase() {
        this.height += 10
      }

    },
    computed: {
      myStyles() {
        return {
          height: `${this.height}px`,
          position: 'relative'
        }
      }
    }
  }
</script>

<style>
  .container {
    margin: 0 auto;
    min-height: 50vh;
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