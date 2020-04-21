<script>
  import {
    Line
  } from 'vue-chartjs'
  export default {
    extends: Line,
    props: {
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
      // https://stackoverflow.com/questions/43728332/vue-chart-js-chart-is-not-updating-when-data-is-changing
      renderLineChart: function (data, options) {
        // if (this.$data._chart) {
        //   this.$data._chart.destroy();
        // }
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
      watch: {
        chartData: function () {
          console.log(this._chart)
          this._chart.destroy();
          //this.renderChart(this.data, this.options);
          this.renderLineChart(this.newData, this.options);
          // console.log(this.$data._chart)
        },
      },
      computed: {
        newData: function () {
          return this.chartData;
        }
      },
    }
  }
</script>

<style scoped>
  canvas {
    width: 100%;
  }
</style>