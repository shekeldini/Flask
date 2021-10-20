var test = document.getElementById('myCharts').getContext('2d');
var test = document.getElementById('myCharts');

var three = document.getElementById('chartsThree').getContext('2d');
var three = document.getElementById('chartsThree');
//Второй график
var testTwo = document.getElementById('myChartsTwo').getContext('2d');
var testTwo = document.getElementById('myChartsTwo');

var threeTwo = document.getElementById('chartsThreeTwo').getContext('2d');
var threeTwo = document.getElementById('chartsThreeTwo');
//
var xhr_chart_1 = new XMLHttpRequest();
var url_chart_1 = "https://jsonplaceholder.typicode.com/posts";
xhr_chart_1.open('GET', url_chart_1, true);
xhr_chart_1.send();

var xhr_chart_2 = new XMLHttpRequest();
var url_chart_2 = "https://jsonplaceholder.typicode.com/posts";
xhr_chart_2.open('GET', url_chart_2, true);
xhr_chart_2.send();

var chart_1 = new Chart(test, {
    plugins: [ChartDataLabels],
	type: 'bar',
	data: {
		labels: [],
		datasets: [{
            label: 'Алтайский край',
            data: [],
            backgroundColor: [
                'rgba(64, 152, 214, 1)',
                'rgba(64, 152, 214, 1)',
                'rgba(64, 152, 214, 1)',
                'rgba(64, 152, 214, 1)',
            ],
            borderColor: [
                // 'rgba(255, 99, 132, 1)',
                // 'rgba(54, 162, 235, 1)',
                // 'rgba(255, 206, 86, 1)',
            ],
            borderWidth: 0
        }
        ],
	},
	options: {
		scales: {
			y: {
				display: true,
				// ticks: {
				//     display: false,
				// },
				// grid: {
				//     display: false
				// }
			},
			x: {
				display: true,
				// ticks: {
				//     display: false,
				// },
				// grid: {
				//     display: false
				// }
			},
		},
		plugins: {
			legend: {
				display: true,
                position: "bottom"
			},
            datalabels: {
                color: "#000000",
                anchor: "end",
                align: "end"

                
            },
			title: {
				display: false,
				text: 'Количество учащихся, принявших участие в ВПР'
			}
		},
	}
});

var chart_2 = new Chart(testTwo, {
    plugins: [ChartDataLabels],
	type: 'bar',
	data: {
		labels: [],
		datasets: [{
            label: 'Алтайский край',
            data: [],
            backgroundColor: [
                'rgba(64, 152, 214, 1)',
                'rgba(64, 152, 214, 1)',
                'rgba(64, 152, 214, 1)',
                'rgba(64, 152, 214, 1)',
            ],
            borderColor: [
                // 'rgba(255, 99, 132, 1)',
                // 'rgba(54, 162, 235, 1)',
                // 'rgba(255, 206, 86, 1)',
            ],
            borderWidth: 0
        }
        ],
	},
	options: {
		scales: {
			y: {
				display: true,
				// ticks: {
				//     display: false,
				// },
				// grid: {
				//     display: false
				// }
			},
			x: {
				display: true,
				// ticks: {
				//     display: false,
				// },
				// grid: {
				//     display: false
				// }
			},
		},
		plugins: {
			legend: {
				display: true,
                position: "bottom"
			},
            datalabels: {
                color: "#000000",
                anchor: "end",
                align: "end"

                
            },
			title: {
				display: false,
				text: 'Количество учащихся, принявших участие в ВПР'
			}
		},
	}
});

xhr_chart_1.onreadystatechange = function() { 
  	if (xhr_chart_1.readyState != 4) return;

  	if (xhr_chart_1.status != 200) {
		  
  } else {
        let data = xhr_chart_1.responseText;
        data = {count_of_students: 106, percents: {4: 16.04, 5: 40.57, 6: 32.08, 7: 11.32}};
        for(let key in data.percents) {
            let value = data.percents[key];
            chart_1.data.labels.push(key);
            chart_1.data.datasets[0].data.push(value);
        }
        chart_1.update();
  }
};

xhr_chart_2.onreadystatechange = function() { 
    if (xhr_chart_2.readyState != 4) return;

    if (xhr_chart_2.status != 200) {
        
} else {
      let data = xhr_chart_2.responseText;
      data = {count_of_students: 106, percents: {4: 20.04, 5: 15.57, 6: 60.08, 7: 11.32}};
      for(let key in data.percents) {
          let value = data.percents[key];
          chart_2.data.labels.push(key);
          chart_2.data.datasets[0].data.push(value);
      }
      chart_2.update();
}
};
