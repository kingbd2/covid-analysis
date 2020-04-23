<template>
  <div>
    <select id="locationtypes" class="w-20 db h2 f6 bg-near-white ba b--sliver gray br-pill" v-model="locationValue">
      <option value="">Location Values</option>
      <option v-for="value in allLocationValues.query_result" :key="value.name" v-on:click="emitToParent"> {{ value.name }}</option>      
    </select>
    <!-- <button >Click to update</button> -->
  </div>
</template>

<script>
  import session from '../api/session';
  export default {
    data() {
      return {
        locationValue: '',
        allLocationValues: [],
        loaded: false,
        errorMessage: '',
        showError: false,
      };
    },
    created() {
      this.getValues()
    },
    methods: {
      emitToParent(event) {
        this.$emit('valueToMain', this.locationValue)
      },
      getValues() {
        session.get('/country')
          .then(response => {
            console.log(response)
            this.allLocationValues = response.data
            this.loaded = true
          })
          .catch(err => {
            this.errorMessage = err
            this.showError = true
          })
      },
    }
  }
</script>

<style>

</style>