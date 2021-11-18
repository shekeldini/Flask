name_of_the_settlement_select = document.getElementById('name_of_the_settlement');
oo_select = document.getElementById('oo');
parallel_select = document.getElementById('parallel');
subject_select = document.getElementById('subject');
report_select = document.getElementById('report');

fetch('get_districts').then(function(response){
		response.json().then(function(data) {
			optionHTML = '';
			for (district of data.districts) {
				optionHTML += '<option value="' + district.id+'">' + district.name + '</option>'
			}
			name_of_the_settlement_select.innerHTML = optionHTML;
			name_of_the_settlement_select.value = "";	
		});
});



name_of_the_settlement_select.onchange = function(){
	parallel_select.innerHTML = "";
	subject_select.innerHTML = "";
	report_select.innerHTML = "";

	name_of_the_settlement = name_of_the_settlement_select.value;
	fetch('oo/' + name_of_the_settlement).then(function(response){
		response.json().then(function(data) {
			optionHTML = '';
			for (oo of data.oo) {
				optionHTML += '<option value="' + oo.id+'">' + oo.name + '</option>'
			}
			oo_select.innerHTML = optionHTML;
			oo_select.value = "";
		});
	});
};

oo_select.onchange = function(){
	
	subject_select.innerHTML = "";
	report_select.innerHTML = "";

	oo = oo_select.value;
	fetch('parallels/' + oo).then(function(response){
		response.json().then(function(data) {
			optionHTML = '';
			for (parallel of data.parallels) {
				optionHTML += '<option value="' + parallel.id+'">' + parallel.name + '</option>'
			}
			parallel_select.innerHTML = optionHTML;
			parallel_select.value = "";
		});
	});
};

parallel_select.onchange = function(){
	report_select.innerHTML = "";

	parallel = parallel_select.value;
	fetch('subjects/' + parallel).then(function(response){
		response.json().then(function(data) {
			optionHTML = '';
			for (subject of data.subjects) {
				optionHTML += '<option value="' + subject.id+'">' + subject.name + '</option>'
			}
			subject_select.innerHTML = optionHTML;
			subject_select.value = "";
		});
	});
};


subject_select.onchange = function(){
fetch('get_reports').then(function(response){
		response.json().then(function(data) {
			optionHTML = '';
			for (report of data.reports) {
				optionHTML += '<option value="' + report.id+'">' + report.name + '</option>'
			}
			report_select.innerHTML = optionHTML;
			report_select.value = "";
		});
	});
};


function draw_report(report_type, json_data, lable_text){
  let body = document.getElementById('report_place');
  let section = document.createElement('section');
  section.className = "TwoPage";
  section.id = "report_section";
  let container = document.createElement('div');
  container.className = "container";
  container.id = "report_container";
  let div =  document.createElement('div');
  div.className = "report_place_border";
  let div_title = document.createElement('div');
  div_title.className = "wrapper__center_low_title";
  let div_subtitle = document.createElement('div');
  div_subtitle.className = "wrapper__center_low_subtitle";

  let canvas = document.createElement('canvas');
	var plot = new Chart(canvas, {
	  plugins: [ChartDataLabels],
		type: 'bar',
		data: {
			labels: [],
			datasets: [{
	            label: lable_text,
	            data: [],
	            backgroundColor: [
	                'rgba(71, 71, 161, 1)',
			'rgba(71, 71, 161, 1)',
			'rgba(71, 71, 161, 1)',
			'rgba(71, 71, 161, 1)'
	            ],
	            borderColor: [],
	            borderWidth: 0
	        }],
		},
		options: {
			scales: {
				y: {
					display: true,
				},
				x: {
					display: true,
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
			layout: {
			    padding: {
			        top: 30
			    }
			},
		}
		
		});
	if (report_type == 0){
		for(let key in json_data.percents) {
	    let value = json_data.percents[key];
	    plot.data.labels.push(key);
	    plot.data.datasets[0].data.push(value);
  	}
	}
  if (report_type == 1){
  	var keys = ['Понизили', 'Подтвердили', 'Повысили'];
  	for(let i in keys) {
  		let key = keys[i] 
	    let value = json_data['percents'][key]['%'];
	    plot.data.labels.push(key);
	    plot.data.datasets[0].data.push(value);
  	}
  }
  plot.update();
  div_title.innerHTML += 'content';
  div_subtitle.innerHTML += 'sub_content';
  div.appendChild(div_title);
  div.appendChild(div_subtitle);
  div.appendChild(canvas);
  container.appendChild(div);
  section.appendChild(container);
  body.appendChild(section);
  return plot;
};



function createTable(objectArray, fields, fieldTitles) {
  let body = document.getElementById('report_container');
  let div = document.createElement('div');
  div.className = "TwoPage__wrapper";
  let tbl = document.createElement('table');
  let thr = document.createElement('tr');
  let tbdy = document.createElement('tbody');

  fieldTitles.forEach((fieldTitle) => {
    let th = document.createElement('td');
    th.appendChild(document.createTextNode(fieldTitle));
    thr.appendChild(th);
  });
  tbdy.appendChild(thr);

  let tr = document.createElement('tr');
  objectArray.forEach((object) => {
    let tr = document.createElement('tr');
    fields.forEach((field) => {
      var td = document.createElement('td');
      td.appendChild(document.createTextNode(object[field]));
      tr.appendChild(td);
    });
    tbdy.appendChild(tr);
  });
  tbl.appendChild(tbdy);
  div.appendChild(tbl);
  body.appendChild(div);
  return tbl;
};



$(document).ready(function(){
	$("#submit_btn").click(function(){

		var id_name_of_the_settlement = $('#name_of_the_settlement').val();
		var id_oo = $('#oo').val();
		var id_oo_parallels = $('#parallel').val();
		var id_oo_parallels_subjects = $('#subject').val();
		var id_report = $('#report').val();


		var sendInfo = {
				name_of_the_settlement: {
							'id': id_name_of_the_settlement,
							"name": $( "#name_of_the_settlement option:selected" ).text()
							},

           	oo:	{
			'id': id_oo,
			"name": $( "#oo option:selected" ).text()
			},

           	parallel: {
				'id': id_oo_parallels,
				"name": $( "#parallel option:selected" ).text()
			},

           	subject: {
	         	'id': id_oo_parallels_subjects,
			"name": $( "#subject option:selected" ).text()
			 },
           	report: {
	         	'id': id_report,
			"name": $( "#report option:selected" ).text()
			}
    		};
   	$(".error").remove();
   	if (id_name_of_the_settlement == null){
   		$('#name_of_the_settlement').after('<span class="error">Это поле не может быть пустым</span>');
   	}
   	if (id_oo == null){
   		$('#oo').after('<span class="error">Это поле не может быть пустым</span>');
   	}
   	if (id_oo_parallels == null){
   		$('#parallel').after('<span class="error">Это поле не может быть пустым</span>');
   	}
   	if (id_oo_parallels_subjects == null){
   		$('#subject').after('<span class="error">Это поле не может быть пустым</span>');
   	}
   	if (id_report == null){
   		$('#report').after('<span class="error">Это поле не может быть пустым</span>');
   	} 
   	else {
   		$("#submit_btn").attr("disabled", true);
   		$.ajax({
  		type : 'POST',
  		url : "/vpr_analysis",
  		contentType: "application/json; charset=utf-8",
  		data: JSON.stringify(sendInfo),

  		success: function(data){
  			marker = JSON.stringify(data);
  			var jsonObj = JSON.parse(marker);
  			$("#report_section").remove();
  			
  			text_name_of_the_settlement_select = jsonObj["name_of_the_settlement"]["name"];
				text_oo_select = jsonObj["oo"]["name"];
				lable_text = text_name_of_the_settlement_select + " - " + text_oo_select
  			if (id_report == 0){
					
  				draw_report(id_report, jsonObj, lable_text);
  				createTable([
						  {	count_of_all_students: jsonObj['count_of_all_students'],
						   	'2': jsonObj['percents']['2'],
								'3': jsonObj['percents']['3'],
								'4': jsonObj['percents']['4'], 
								'5': jsonObj['percents']['5']}],
						['count_of_all_students', '2', '3', '4', '5'],
						['Кол-во участников', '2', '3', '4', '5']
					);
  			}
  			if (id_report == 1){
  				draw_report(id_report, jsonObj, lable_text);
  				//'Понизили (Отметка < Отметка по журналу)'
  				createTable([
						  {	'Группы участников': 'Понизили (Отметка < Отметка по журналу)',
						   	'Кол-во участников': jsonObj['percents']['Понизили']['count_of_students'],
						   	'%': jsonObj['percents']['Понизили']['%']},
						  {
						  	'Группы участников': 'Подтвердили (Отметка = Отметка по журналу)',
						   	'Кол-во участников': jsonObj['percents']['Подтвердили']['count_of_students'],
						   	'%': jsonObj['percents']['Подтвердили']['%']
						  },
						  {
						  	'Группы участников': 'Повысили (Отметка > Отметка по журналу)',
						   	'Кол-во участников': jsonObj['percents']['Повысили']['count_of_students'],
						   	'%': jsonObj['percents']['Повысили']['%']
						  },
						  {
						  	'Группы участников': 'Всего',
						   	'Кол-во участников': jsonObj['count_of_all_students'],
						   	'%': '100'
						  }],
						['Группы участников', 'Кол-во участников', '%'],
						['Группы участников', 'Кол-во участников', '%']
					);
  			}	

  			$("#submit_btn").attr("disabled", false);
  			
    	},
    	error:function(){
    			alert("Ошибка сервера");
    			$("#submit_btn").attr("disabled", false);
    	},
			});
    };
 	});
});
