<template>
  <div class="">
    <!-- <div v-if="!atBeginning">
      <h2>You have selected: {{ selectedContinent }}, {{selectedCountry}}, {{ selectedProvState }}</h2>
    </div> -->
    <div class="start pa3 pa5-ns">

      <article class="center mw5 mw6-ns hidden ba mv4" v-if="atBeginning">
        <h1 class="f4 bg-near-black white mv0 pv2 ph3">Which continent would you like to explore?</h1>
        <div class="pa3 bt white">
          <ul class="list ph3 ph5-ns pv4">
            <li v-for="continent in continents" :key="continent.continent_id" class="dib mr1 mb2">
              <a class="f6 grow no-underline br-pill ba bw1 ph3 pv2 mb2 dib dark-blue"
                v-on:click="getTheSelectedContinent(continent.name)">{{continent.name}}
              </a>
            </li>
            <p>{{ selectedContinent }}</p>
          </ul>
        </div>
      </article>

      <article class="center mw5 mw6-ns hidden ba mv4" v-if="continentSelectedIndicator">
        <h1 class="f4 bg-near-black white mv0 pv2 ph3">Which country?</h1>
        <div class="pa3 bt white">
          <a v-if="!atBeginning" class="f6 link dim br3 ph3 pv2 mb2 dib white bg-light-blue" @click="resetQuestions">Go
            back
            to beginning</a>
          <ul class="list ph3 ph5-ns pv4">
            <li v-for="country in countries" :key="country" class="dib mr1 mb2">
              <a class="f6 grow no-underline br-pill ba bw1 ph3 pv2 mb2 dib dark-green"
                v-on:click="getTheSelectedCountry(country)">{{country}}
              </a>
            </li>
          </ul>
        </div>
      </article>

      <article class="center mw5 mw6-ns hidden ba mv4" v-if="countrySelectedIndicator">
        <a v-if="!atBeginning" class="f6 link dim br3 ph3 pv2 mb2 dib white bg-light-blue"
              @click="resetQuestions">Go
              back
              to beginning</a>
        <div v-if="provinces_states.length == 0">
          <h1 class="f4 bg-near-black white mv0 pv2 ph3">No provinces or state in this dataset</h1>
        </div>
        <div v-else-if="provinces_states.length > 0">
          <h1 class="f4 bg-near-black white mv0 pv2 ph3">Which province or state?</h1>
          <div class="pa3 bt white">
            
            <ul class="list ph3 ph5-ns pv4">
              <li v-for="prov_state in provinces_states" :key="prov_state" class="dib mr1 mb2">
                <a class="f6 grow no-underline br-pill ba bw1 ph3 pv2 mb2 dib dark-green"
                  v-on:click="getTheSelectedProvinceState(prov_state)">{{prov_state}}
                </a>
              </li>
            </ul>
          </div>
        </div>
      </article>

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
        provStateSelectedIndicator: false,
        selectedContinent: '',
        selectedCountry: '',
        selectedProvState: '',
        showGoToBeginning: false,
        continents: [],
        countries: [],
        provinces_states: [],
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
      getProvinceStateData(country_name) {
        session.get(''.concat(country_name, '/provinces_states'))
          .then(response => {
            console.log(response)
            this.provinces_states = response.data.provinces_states
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
        this.emitToMain('continent', continent_name)
      },
      getTheSelectedCountry(country_name) {
        this.getProvinceStateData(country_name)
        this.selectedCountry = country_name
        this.countrySelectedIndicator = true
        this.continentSelectedIndicator = false
        this.emitToMain('country', country_name)
      },
      getTheSelectedProvinceState(province_state_name) {
        this.selectedProvState = province_state_name
        this.countrySelectedIndicator = true
        this.provStateSelectedIndicator = true
        this.emitToMain('province_state', province_state_name)
      },
      resetQuestions() {
        this.atBeginning = true,
        this.continentSelectedIndicator = false,
        this.countrySelectedIndicator = false,
        this.provStateSelectedIndicator = false,
        this.selectedContinent = '',
        this.selectedCountry = '',
        this.selectedProvState = '',
        this.showGoToBeginning = false,
        this.countries = [],
        this.provinces_states = []
        this.emitToMain('reset')
      },
      emitToMain(location_type, value) {
        this.$emit('valueToMain', location_type, value)
      },
    },
  }
</script>

<style>

</style>