<template>
  <div>
    <h2>You have selected: {{ selectedContinent }}, {{selectedCountry}}</h2>  
    <div v-if="atBeginning" class="start">
    <p class="measure lh-copy">Which continent would you like to explore?</p>
    <ul class="list ph3 ph5-ns pv4">
      <li v-for="continent in continents" :key="continent.continent_id" class="dib mr1 mb2">
        <a class="f6 grow no-underline br-pill ba bw1 ph3 pv2 mb2 dib dark-blue"
          v-on:click="getTheSelectedContinent(continent.name)">{{continent.name}}
        </a>
      </li>
      <p>{{ selectedContinent }}</p>
    </ul>
    </div>
    <div class="continent_container" v-if="continentSelectedIndicator">
      <p class="measure lh-copy">Which country?</p>
      <ul class="list ph3 ph5-ns pv4">
        <li v-for="country in countries" :key="country.country_id" class="dib mr1 mb2">
          <a class="f6 grow no-underline br-pill ba bw1 ph3 pv2 mb2 dib dark-green"
            v-on:click="getTheSelectedCountry(country.name)">{{country.name}}
          </a>
        </li>
        <p>{{ selectedContinent }}</p>
      </ul>
    </div>
  </div>
</template>

<script>
  import session from '../api/session';
  export default {
    data() {
      return {
        atBeginning: true,
        continentSelectedIndicator: false,
        countrySelectedIndicator: false,
        selectedContinent: '',
        selectedCountry: '',
        showGoToBeginning: false,
        continents: [],
        countries: [],
        locationTypeSelection: 'country',
        locationValueSelection: 'Canada',
        locationTypeFromAPI: '',
        locationValueFromAPI: '',
        loaded: false,
        showError: false,
        errorMessage: 'There is an error, and this is the default message',
        error: null,
      };
    },
    created() {
      this.getContinentData()
      this.getCountryData()
    },
    methods: {
      getContinentData() {
        session.get('continent')
          .then(response => {
            console.log(response)
            this.continents = response.data.query_result.map(name => name)
            this.loaded = true
          })
          .catch(err => {
            this.errorMessage = err
            this.showError = true
          })
      },
      getCountryData() {
        session.get('country')
          .then(response => {
            console.log(response)
            this.countries = response.data.query_result.map(name => name)
            this.loaded = true
          })
          .catch(err => {
            this.errorMessage = err
            this.showError = true
          })
      },
      getTheSelectedContinent(continent_name) {
        this.selectedContinent = continent_name
        this.atBeginning = false
        this.continentSelectedIndicator = true
      },
      getTheSelectedCountry(country_name) {
        this.selectedCountry = country_name
        this.countrySelectedIndicator = true
      },
      
    },
  }
</script>

<style>

</style>