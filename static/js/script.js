var test = document.getElementById('myCharts').getContext('2d');
var test = document.getElementById('myCharts');

//Второй график
var testTwo = document.getElementById('myChartsTwo').getContext('2d');
var testTwo = document.getElementById('myChartsTwo');
//

var round = document.getElementById('roundlet').getContext('2d');
var round = document.getElementById('roundlet');

var xhr_chart_1 = new XMLHttpRequest();
var url_chart_1 = "https://jsonplaceholder.typicode.com/posts";
xhr_chart_1.open('GET', url_chart_1, true);
xhr_chart_1.send();

var xhr_chart_2 = new XMLHttpRequest();
var url_chart_2 = "https://jsonplaceholder.typicode.com/posts";
xhr_chart_2.open('GET', url_chart_2, true);
xhr_chart_2.send();

const roundlet = new Chart(round, {
	type: 'pie',
	data: {
	   labels: ['ОО 1', 'ОО 2', 'ОО 3'],
	   datasets: [{
		  label: '# of Votes',
		  data: [300, 50, 100],
		  backgroundColor: [
		          'rgb(255, 99, 132, 0.7)',
			  'rgb(54, 162, 235, 0.7)',
			  'rgb(255, 205, 86, 0.7)'
	          ],
		  hoverOffset: 4
	   }]
	},
	options: {
	    scales: {

	    },
	    radius: '90%',
	    maintainAspectRatio: false,           
            responsive: true,


	    plugins: {
	       legend: {
		display: true,
		position: "bottom"
	       }

	    }
        }
});



var chart_1 = new Chart(test, {
    plugins: [ChartDataLabels],
	type: 'bar',
	data: {
		labels: [],
		datasets: [{
            label: 'Алтайский край',
            data: [],
            backgroundColor: [
		'rgba(71, 71, 161, 0.7)',
		'rgba(71, 71, 161, 0.7)',
		'rgba(71, 71, 161, 0.7)',
		'rgba(71, 71, 161, 0.7)',
            ],
            borderColor: [
                 'rgba(102, 133, 255, 1)',
                // 'rgba(54, 162, 235, 1)',
                // 'rgba(255, 206, 86, 1)',
            ],
            borderWidth: 1
        }
        ],
	},
	options: {
                scales: {
		  x: {
                    title: {
                       color: '#1F1F1F',
                       display: true,
                       text: 'Классы',
                       font: {
                         size: 15
                       },
	               align: 'center'
                    }
                  },
		  y: {
                    title: {
                       color: '#1F1F1F',
                       display: true,
                       text: 'Соотношение в процентах, %',
                       font: {
                         size: 15
                       },
                       align: 'center'
                    }
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
				display: true,
				text: 'Заголовок',
				color: '#1F1F1F',
				font: {
				  size: 15
				}
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
		'rgba(71, 71, 161, 0.7)',
		'rgba(71, 71, 161, 0.7)',
		'rgba(71, 71, 161, 0.7)',
		'rgba(71, 71, 161, 0.7)',
            ],
            borderColor: [
                 'rgba(102, 133, 255, 1)',
                // 'rgba(54, 162, 235, 1)',
                // 'rgba(255, 206, 86, 1)',
            ],
            borderWidth: 1
        }
        ],
	},
	options: {
		scales: {
		  x: {
                    title: {
                       color: '#1F1F1F',
                       display: true,
                       text: 'Классы',
                       font: {
                         size: 15
                       },
                       align: 'center'
                    }
                  },
		  y: {
                    title: {
                       color: '#1F1F1F',
                       display: true,
                       text: 'Соотношение в процентах, %',
                       font: {
                         size: 15
                       },
                       align: 'center'
                    }
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


			   display: true,
        		   text: 'Заголовок',
        		   color: '#1F1F1F',
       			   font: {
            	             size: 15
        	           }
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
