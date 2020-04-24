<template>
  <div class="page-container">
    <header>
      <header-component></header-component>
    </header>

    <aside>
      <sidebar></sidebar>
    </aside>

    <nav>
      <!-- Navigation -->
    </nav>

    <main>
      <!-- Dashboard Information -->
      
      <article class="pa3 pa5-ns">
        <a class="f6 link dim br3 ph3 pv2 mb2 dib white bg-light-purple" @click="render">Refresh chart</a>
        <h1 class="f3 f2-m f1-l">{{locationTypeFromAPI | capitalize}}: {{locationValueFromAPI}}</h1>
        <p class="measure lh-copy">
          This is a count over time of all {{ case_type }} in {{ locationValueFromAPI }}
        </p>
      </article>

      <!-- UI Selectors -->
      <!-- <location-type-selector v-on:typeToMain="onTypeUpdate"></location-type-selector>
    <location-selector v-on:valueToMain="onValueUpdate"></location-selector> -->
      <!-- <button type="submit" @click="render">Update chart</button> -->
      <!-- Chart Container -->
      <div class="chart-container">
        <div class="chart">
          <chart v-if="loaded" :location-type="locationTypeSelection" :location-value="locationValueSelection"
            :chart-data="case_counts" :chart-labels="labels" :location-name="locationValueSelection" :styles="myStyles"
            ref="chart">
          </chart>
        </div>
      </div>
      <div class="error-message" v-if="showError">
        {{ errorMessage }}
      </div>
    </main>
    <footer>
      <!-- <footer-component></footer-component> -->
    </footer>
  </div>
</template>

<script>
  import HeaderComponent from '~/components/HeaderComponent.vue'
  import Sidebar from '~/components/Sidebar.vue'
  import Chart from '~/components/Chart.vue'
  import LocationSelector from '~/components/LocationSelector.vue'
  import LocationTypeSelector from '~/components/LocationTypeSelector.vue'
  import FooterComponent from '~/components/FooterComponent.vue'

  import getAllTable from '../api/endpoints';
  import session from '../api/session';
  export default {
    components: {
      HeaderComponent,
      Sidebar,
      Chart,
      LocationSelector,
      LocationTypeSelector,
      FooterComponent,
    },
    data() {
      return {
        continent_selected: 'North America',
        locationTypeSelection: 'country',
        locationValueSelection: 'Canada',
        locationTypeFromAPI: '',
        locationValueFromAPI: '',
        case_type: '',
        loaded: false,
        showError: false,
        errorMessage: 'There is an error, and this is the default message',
        error: null,
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
        this.$refs.chart.renderLineChart(this.case_counts, this.options)
      },
      increase() {
        this.height += 10
      },
      onTypeUpdate(value) {
        this.locationTypeSelection = value
      },

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
    },
  }
</script>

<style>
  header {
    grid-area: header;
  }

  nav {
    grid-area: nav;
    margin-left: 0.5rem;
  }

  main {
    grid-area: content;
  }

  aside {
    grid-area: side;
    margin-right: 0.5rem;
  }

  footer {
    grid-area: footer;
  }

  nav,
  aside {
    margin: 0;
  }

  .chart-container {
    margin: 0 auto;
    min-height: 50vh;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
  }

  /* .parent {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    grid-template-rows: repeat(2, 1fr);
    grid-column-gap: 10px;
    grid-row-gap: 30px;
  } */

  .page-container {
    display: grid;

    grid-template-areas:
      "header header header"
      "side content nav"
      "footer footer footer";

    grid-template-columns: 400px 1fr 200px;
    grid-template-rows: auto 1fr auto;
    grid-gap: 10px;

    height: 100vh;
  }

  @media (max-width: 768px) {
    .page-container {
      grid-template-areas:
        "header"
        "side"
        "nav"
        "content"
        "footer";

      grid-template-columns: 1fr;
      grid-template-rows:
        auto
        /* Header */
        minmax(75px, auto)
        /* Nav */
        1fr
        /* Content */
        minmax(75px, auto)
        /* Sidebar */
        auto;
      /* Footer */
    }
  }
</style>