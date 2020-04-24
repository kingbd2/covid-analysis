<template>
  <div class="page-container">
    <header>
      <header-component></header-component>
    </header>

    <aside>
      <sidebar v-on:valueToMain="onSidebarUpdate"></sidebar>
    </aside>

    <nav>
      <!-- Navigation -->
    </nav>

    <main>
      <!-- Dashboard Information -->

      <article class="pa3 pa5-ns">
        <div class="ph3">
          <a class="f6 link dim br3 ph3 pv2 mb2 dib white bg-light-blue" @click="getCasesByDateData">Get new data</a>
          <a class="f6 link dim br3 ph3 pv2 mb2 dib white bg-light-blue" @click="getTotalsData">Get new totals</a>
          <a class="f6 link dim br3 ph3 pv2 mb2 dib white bg-light-purple" @click="render">Refresh chart</a>
        </div>
        <div class="ph3">

          <a class="f6 link dim ph3 pv2 mb2 dib white bg-mid-gray" @click="selectConfirmed">Confirmed</a>
          <a class="f6 link dim ph3 pv2 mb2 dib white bg-mid-gray" @click="selectDeaths">Deaths</a>
          <a class="f6 link dim ph3 pv2 mb2 dib white bg-mid-gray" @click="selectRecovered">Recovered</a>
        </div>
        
        <dl class="lh-title pa4 mt0">
          <dt class="f6 b">Continent</dt>
          <dd class="ml0">{{continent_selected}}</dd>
          <dt class="f6 b">Country</dt>
          <dd class="ml0">{{country_selected}}</dd>
          <dt class="f6 b">Province or state</dt>
          <dd class="ml0">{{province_state_selected}}</dd>
        </dl>
        <h1>Today</h1>
        <dl class="dib mr5">
          <dd class="f6 f5-ns b ml0">Total {{ case_type }} Cases in {{locationStringBuilder}}</dd>
          <dd class="f3 f2-ns b ml0">{{caseTotals}}</dd>
        </dl>
        <!-- <h1 class="f3 f2-m f1-l">{{locationTypeFromAPI | capitalize}}: {{locationValueFromAPI}}</h1> -->
        <p class="measure lh-copy">
          This is a count over time of all {{ case_type }} in {{ locationStringBuilder }}
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
      <!-- <div class="error-message" v-if="showError">
        {{ errorMessage }}
      </div> -->
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
        continent_selected: '',
        country_selected: '',
        province_state_selected: '',
        locationTypeSelection: 'country',
        locationValueSelection: 'Canada',
        locationTypeFromAPI: '',
        locationValueFromAPI: '',
        case_type: '',
        loaded: false,
        showError: false,
        errorMessage: 'There is an error, and this is the default message',
        error: null,
        case_counts: [],
        labels: [],
        caseTotals: null,
        confirmedTotal: null,
        recoveredTotal: null,
        deathsTotal: null
      };
    },
    created() {
      this.getInitialData()
    },
    methods: {
      getInitialData() {
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
      getTotalsData() {
        session.get(this.totalsApiBuilder)
          .then(response => {
            console.log(response)
            this.caseTotals = response.data.counts[0]
            this.case_type = response.data.case_type
            this.loaded = true

          })
          .catch(err => {
            this.errorMessage = err
            this.showError = true
          })
      },
      getCasesByDateData() {
        session.get(this.caseByDateApiBuilder)
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
      selectConfirmed() {
        this.case_type = 'Confirmed'
      },
      selectDeaths() {
        this.case_type = 'Deaths'
      },
      selectRecovered() {
        this.case_type = 'Recovered'
      },
      increase() {
        this.height += 10
      },
      onSidebarUpdate(location_type, value) {
        if (location_type == 'continent') {
          this.continent_selected = value
          this.locationTypeSelection = location_type
        } else if (location_type == 'country') {
          this.country_selected = value
          this.locationTypeSelection = location_type
        } else if (location_type == 'province_state') {
          this.province_state_selected = value
          this.locationTypeSelection = location_type
        } else if (location_type == 'reset') {
          this.continent_selected = ''
          this.country_selected = ''
          this.province_state_selected = ''
          this.locationTypeSelection = ''
        }

      },

    },
    computed: {
      myStyles() {
        return {
          height: `${this.height}px`,
          position: 'relative'
        }
      },
      totalsApiBuilder() {
        if (this.continent_selected && !this.country_selected && !this.province_state_selected) {
          return '/'.concat('totals/', this.locationTypeSelection, '/', this.continent_selected, '/', this.case_type,
            '?sum_counts=true')
        } else if (this.country_selected && this.country_selected && !this.province_state_selected) {
          return '/'.concat('totals/', this.locationTypeSelection, '/', this.country_selected, '/', this.case_type,
            '?sum_counts=true')
        } else if (this.country_selected && this.country_selected && this.province_state_selected) {
          return '/'.concat('totals/', this.locationTypeSelection, '/', this.province_state_selected, '/', this
            .case_type, '?sum_counts=true')
        }
      },
      caseByDateApiBuilder() {
        if (this.continent_selected && !this.country_selected && !this.province_state_selected) {
          return '/'.concat('continent/', this.continent_selected, '/', this.case_type)
        } else if (this.country_selected && this.country_selected && !this.province_state_selected) {
          return '/'.concat('country/', this.country_selected, '/', this.case_type)
        } else if (this.country_selected && this.country_selected && this.province_state_selected) {
          return '/'.concat('province_state/', this.province_state_selected, '/', this.case_type)
        }
      },
      locationStringBuilder() {
        if (this.continent_selected && !this.country_selected && !this.province_state_selected) {
          return ''.concat(this.continent_selected)
        } else if (this.country_selected && this.country_selected && !this.province_state_selected) {
          return ''.concat(this.continent_selected, ', ', this.country_selected)
        } else if (this.country_selected && this.country_selected && this.province_state_selected) {
          return ''.concat(this.continent_selected, ', ', this.country_selected, ', ', this.province_state_selected)
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