<template>
  <div class="page-container">
    <!-- Dashboard Information -->
    <article class="pa3 pa5-ns">
      <h1 class="f3 f2-m f1-l">{{locationTypeFromAPI | capitalize}}: {{locationValueFromAPI}}</h1>
      <p class="measure lh-copy">
        This is a count over time of all {{ case_type }} in {{ locationValueFromAPI }}
      </p>
    </article>
    <!-- UI Selectors -->
    <location-type-selector v-on:typeToMain="onTypeUpdate"></location-type-selector>
    <location-selector v-on:valueToMain="onValueUpdate"></location-selector>
    <button type="submit" @click="render">Update chart</button>
    <!-- Chart Container -->
    <div class="container">
      <chart v-if="loaded" :chart-data="case_counts" :chart-labels="labels" :styles="myStyles" ref="chart"></chart>
      <div class="error-message" v-if="showError">
        {{ errorMessage }}
      </div>
    </div>
  </div>
</template>

<script>
  import Chart from '~/components/Chart.vue'
  import LocationSelector from '~/components/LocationSelector.vue'
  import LocationTypeSelector from '~/components/LocationTypeSelector.vue'
  import session from '../store/api/session';
  export default {
    components: {
      Chart,
      LocationSelector,
      LocationTypeSelector
    },
    data() {
      return {
        locationTypeSelection: 'country',
        locationValueSelection: 'Canada',
        ids: [],
        case_counts: [],
        labels: [],
        case_type: '',
        locationTypeFromAPI: '',
        locationValueFromAPI: '',
        loaded: false,
        showError: false,
        errorMessage: 'There is an error, and this is the default message',
        error: null,
        height: 300
      };
    },
    created() {
      this.getData()
    },
    methods: {
      getData() {
        session.get('/'.concat(this.locationTypeSelection, '/', this.locationValueSelection, '/Confirmed'))
          .then(response => {
            console.log(response)
            this.case_counts = response.data.counts.map(count => count)
            this.labels = response.data.dates.map(date => date)
            this.locationTypeFromAPI = response.data.location_type
            this.locationValueFromAPI = response.data.location_value
            this.case_type = response.data.case_type
            this.loaded = true
          })
          .catch(err => {
            this.errorMessage = err
            this.showError = true
          })
      },
      render() {
        this.$refs.chart.renderChart()
      },
      increase() {
        this.height += 10
      },
      onTypeUpdate(value) {
        this.locationTypeSelection = value
      },
      onValueUpdate(value) {
        this.locationValueSelection = value
        this.getData()
      }
    },
    computed: {
      myStyles() {
        return {
          height: `${this.height}px`,
          position: 'relative'
        }
      }
    },
    filters: {
      capitalize: function (value) {
        if (!value) return ''
        value = value.toString()
        return value.charAt(0).toUpperCase() + value.slice(1)
      }
    }
  }
</script>

<style>
  .container {
    margin: 0 auto;
    min-height: 50vh;
    /* display: flex; */
    /* justify-content: center;
    align-items: center;
    text-align: center; */
  }
</style>