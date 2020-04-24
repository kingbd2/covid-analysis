<template>
  <div class="">

    <div v-if="atBeginning" class="start pa3 pa5-ns">
      <p class="f5 lh-copy bg-light-blue">Which continent would you like to explore?</p>
      <ul class="list ph3 ph5-ns pv4 bg-light-gray">
        <li v-for="continent in continents" :key="continent.continent_id" class="dib mr1 mb2">
          <a class="f6 grow no-underline br-pill ba bw1 ph3 pv2 mb2 dib dark-blue"
            v-on:click="getTheSelectedContinent(continent.name)">{{continent.name}}
          </a>
        </li>
        <p>{{ selectedContinent }}</p>
      </ul>
    </div>

    <div class="continent_container start pa3 pa5-ns" v-if="continentSelectedIndicator">
      <h2>You have selected: {{ selectedContinent }}</h2>
      <a v-if="!atBeginning" class="f6 link dim br3 ph3 pv2 mb2 dib white bg-light-blue" @click="resetQuestions">Go back
        to beginning</a>
      <p class="measure lh-copy bg-light-blue">Which country?</p>
      <ul class="list ph3 ph5-ns pv4 bg-light-gray">
        <li v-for="country in countries" :key="country" class="dib mr1 mb2">
          <a class="f6 grow no-underline br-pill ba bw1 ph3 pv2 mb2 dib dark-green"
            v-on:click="getTheSelectedCountry(country)">{{country}}
          </a>
        </li>
        <!-- <p>{{ selectedContinent }}</p> -->
      </ul>
    </div>
    <h2>You have selected: {{ selectedContinent }}, {{selectedCountry}}</h2>
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
      getCountryData(continent_name) {
        session.get(''.concat(continent_name, '/countries'))
          .then(response => {
            console.log(response)
            this.countries = response.data.countries
            this.loaded = true
          })
          .catch(err => {
            this.errorMessage = err
            this.showError = true
          })
      },
      getTheSelectedContinent(continent_name) {
        this.getCountryData(continent_name)
        this.selectedContinent = continent_name
        this.atBeginning = false
        this.continentSelectedIndicator = true
      },
      getTheSelectedCountry(country_name) {
        this.selectedCountry = country_name
        this.countrySelectedIndicator = true
      },
      resetQuestions() {
        this.atBeginning = true,
          this.continentSelectedIndicator = false,
          this.countrySelectedIndicator = false,
          this.selectedContinent = '',
          this.selectedCountry = '',
          this.showGoToBeginning = false,
          this.countries = []
      },
    },
  }
</script>

<style>

</style>