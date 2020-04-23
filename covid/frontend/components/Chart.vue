<script>
  import {
    Line
  } from 'vue-chartjs'
  import session from '../api/session';
  export default {
    extends: Line,
    props: {
      locationType: {
        type: String,
        required: false
      },
      locationValue: {
        type: String,
        required: false
      },
      chartData: {
        type: Array | Object,
        required: false
      },
      chartLabels: {
        type: Array,
        required: true
      },
      locationName: {
        type: String,
        required: false
      }
    },
    data() {
      return {
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
        options: {
          scales: {
            yAxes: [{
              ticks: {
                beginAtZero: false
              },
              scaleLabel: {
                display: true,
                labelString: 'Count',
              },
              gridLines: {
                display: true
              }
            }],
            xAxes: [{
              gridLines: {
                display: false
              },
              scaleLabel: {
                display: true,
                labelString: 'Date',
              },
            }]
          },
          legend: {
            display: false
          },
          responsive: true,
          maintainAspectRatio: true
        }
      }
    },
    mounted() {
      this.renderLineChart(this.chartData, this.options);
    },
    methods: {
      renderLineChart: function (data, options) {
        this.renderChart({
          labels: this.chartLabels,
          datasets: [{
            label: 'Count',
            borderColor: '#249EBF',
            pointBackgroundColor: '#249EBF',
            borderWidth: 1,
            pointBorderColor: '#249EBF',
            backgroundColor: 'transparent',
            data: data
          }]
        }, options)
      },      
    }
  }
</script>

<style scoped>
  canvas {
    width: 100%;
  }
</style>