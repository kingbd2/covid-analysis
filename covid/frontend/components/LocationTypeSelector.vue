<template>
  <div>
    <select id="locationtypes" class="w-20 db h2 f6 bg-near-white ba b--silver gray br-pill" v-model="locationType" v-on:click="emitToParent">
      <option value=''>Location Types</option>
      <option label="Continent">Continent
      </option>
      <option label="Country">Country
      </option>
      <option label="Province or State">Province or State
      </option>
    </select>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        locationType: '',
      };
    },
    methods: {
      emitToParent(event) {
        this.$emit('typeToMain', this.locationType)
      }
    }
  }
</script>

<style>

</style>