district_select = document.getElementById('district');
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
                        district_select.innerHTML = optionHTML;
                        district_select.value = "";
                });
});



district_select.onchange = function(){
        parallel_select.innerHTML = "";
        subject_select.innerHTML = "";
        report_select.innerHTML = "";

        district = district_select.value;
        fetch('oo/' + district).then(function(response){
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
        if (district_select.value == "all" || oo_select.value == "all"){
                 fetch('all_subjects/' + parallel).then(function(response){
                        response.json().then(function(data) {
                                optionHTML = '';
                                for (subject of data.subjects) {
                                        optionHTML += '<option value="' + subject.id+'">' + subject.name + '</option>'
                                }
                                subject_select.innerHTML = optionHTML;
                                subject_select.value = "";
                        });
                });
        }else{
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


function draw_report_type_0(json_data){
	let content_text = json_data.plot_settings.content;
	let sub_content_list = json_data.plot_settings.sub_content;
	let title_text = json_data.plot_settings.title;
	let x_axis = json_data.plot_settings.x_axis;
	let y_axis = json_data.plot_settings.y_axis;

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
                  datasets: [],
                },
                options: {
                        scales: {
                           x: {
                               title: {
                                   color: '#1F1F1F',
                                   display: true,
                                   text: x_axis,
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
                                   text: y_axis,
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
                                    text: title_text,
                                    color: '#1F1F1F',
                                    font: {
                                      size: 15
                                    }
                                }
                        },
                        layout: {
                            padding: {
                                top: 30
                            }
                        },
                }

                });
		let colors = [	'rgba(243, 121, 126, 0.7)',
				'rgba(237, 216, 26, 0.7)',
				'rgba(125, 160, 250, 0.7)'];
		let lables_list = json_data.plot_settings.lables;
        	for (let lable in lables_list){
        		plot.data.labels.push(lables_list[lable]);
		}
          for(let i = 0; i < Object.keys(json_data.percents).length; i++) {
          	let keys = Object.keys(json_data.percents);
		key = json_data.percents[keys[i]];
          	plot.data.datasets[i] = {};
		plot.data.datasets[i].data = [];
		plot.data.datasets[i].backgroundColor = [];
		plot.data.datasets[i].label = key.name;

          	for (let mark in key.value){
          		plot.data.datasets[i].data.push(key.value[mark]);
			plot.data.datasets[i].backgroundColor.push(colors[i]);

          	}

          	plot.data.datasets[i].borderColor = [
	            'rgba(255, 0, 0, 1);'
        	    ];
           	 plot.data.datasets[i].borderWidth = 1
        	}
  plot.update();
  div_title.innerHTML += content_text;
  for(let i in sub_content_list){
  	sub_content = sub_content_list[i];
  	let h3 = document.createElement('h3');
  	let text = document.createTextNode(sub_content);
  	h3.appendChild(text);
  	div_subtitle.appendChild(h3);
  }
  div.appendChild(div_title);
  div.appendChild(div_subtitle);
  div.appendChild(canvas);
  container.appendChild(div);
  section.appendChild(container);
  body.appendChild(section);
  return plot;
};


function createTable_type_0(jsonObj) {
  let fieldTitles = jsonObj.table_settings.titles;
  let fields = jsonObj.table_settings.fields;
  let objectArray = jsonObj.table_settings.values;
  let body = document.getElementById('report_container');
  let div = document.createElement('div');
  div.className = "TwoPage__wrapper";
  let title = document.createElement('h3');
  title.className = "TwoPage__wrapper_title";
  let text = document.createTextNode('Таблица результатов:');
  let tbl = document.createElement('table');
  let thr = document.createElement('tr');
  let tbdy = document.createElement('tbody');

  fieldTitles.forEach((fieldTitle) => {
    let th = document.createElement('td');
    th.appendChild(document.createTextNode(fieldTitle));
    thr.appendChild(th);
  });
  tbdy.appendChild(thr);
  for(let i = 0; i < objectArray.groups.length; i++){
  let tr = document.createElement('tr');
  for (field of fields){
        {
                var td = document.createElement('td');
                td.appendChild(document.createTextNode(objectArray[field][i]));
                tr.appendChild(td);
        }
        tbdy.appendChild(tr);
  }

}
  title.appendChild(text);
  div.appendChild(title);
  tbl.appendChild(tbdy);
  div.appendChild(tbl);
  body.appendChild(div);
  return tbl;
};

function draw_report(json_data){
        let content_text = json_data.plot_settings.content;
        let title_text = json_data.plot_settings.title;
        let x_axis = json_data.plot_settings.x_axis;
        let y_axis = json_data.plot_settings.y_axis;
	let index = 0;
	if (Object.keys(json_data.percents).length > 1){
		draw_report_type_1_all(json_data, content_text, title_text, x_axis, y_axis);
        	index += 1;
	}
        for([key, sub_content_list] of Object.entries(json_data.plot_settings.sub_content)){
		if( key != "all"){
                draw_report_type_1(json_data, content_text, title_text, x_axis, y_axis, key, sub_content_list, index);
		createTable_type_1(json_data, key, index);
		index += 1;
		}
        }
}

function draw_report_type_1_all(json_data, content_text, title_text, x_axis, y_axis){
  let sub_content_list = json_data.plot_settings.sub_content.all
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
                  datasets: [],
                },
                options: {
                        scales: {
                           x: {
                               title: {
                                   color: '#1F1F1F',
                                   display: true,
                                   text: x_axis,
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
                                   text: y_axis,
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
                                    text: title_text,
                                    color: '#1F1F1F',
                                    font: {
                                      size: 15
                                    }
                                }
                        },
                        layout: {
                            padding: {
                                top: 30
                            }
                        },
                }

                });
                let colors = [  'rgba(243, 121, 126, 0.7)',
                                'rgba(237, 216, 26, 0.7)',
                                'rgba(125, 160, 250, 0.7)'];
                let lables_list = json_data.plot_settings.lables;
                for (let lable in lables_list){
                        plot.data.labels.push(lables_list[lable]);
                }
          for(let i = 0; i < Object.keys(json_data.percents).length; i++) {
                let keys = Object.keys(json_data.percents);
                key = json_data.percents[keys[i]];
                plot.data.datasets[i] = {};
                plot.data.datasets[i].data = [];
                plot.data.datasets[i].backgroundColor = [];
                plot.data.datasets[i].label = key.name;
                let col_names = ["Понизили", "Подтвердили", "Повысили"]
                for (let col of col_names){
                        plot.data.datasets[i].data.push(key.value[col]["%"]);
                        plot.data.datasets[i].backgroundColor.push(colors[i]);

                }

                plot.data.datasets[i].borderColor = [
                    'rgba(255, 0, 0, 1);'
                    ];
                 plot.data.datasets[i].borderWidth = 1
                }
  plot.update();
  div_title.innerHTML += content_text;
  for(let i in sub_content_list){
        sub_content = sub_content_list[i];
        let h3 = document.createElement('h3');
        let text = document.createTextNode(sub_content);
        h3.appendChild(text);
        div_subtitle.appendChild(h3);
  }
  div.appendChild(div_title);
  div.appendChild(div_subtitle);
  div.appendChild(canvas);
  container.appendChild(div);
  section.appendChild(container);
  body.appendChild(section);
  return plot;
};

function draw_report_type_1(json_data, content_text, title_text, x_axis, y_axis, key, sub_content_list, index){

        let body = document.getElementById('report_place');
        let section = document.createElement('section');
        section.className = "TwoPage";
        section.id = "report_section_" + index;
        let container = document.createElement('div');
        container.className = "container";
        container.id = "report_container_" + index;
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
                  datasets: [],
                },
                options: {
                        scales: {
                           x: {
                               title: {
                                   color: '#1F1F1F',
                                   display: true,
                                   text: x_axis,
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
                                   text: y_axis,
                                   font: {
                                       size: 15
                                   },
                                   align: 'center'
                               }
                           },

                        },
                        plugins: {
                                legend: {
                                        display: false,
                        position: "bottom"
                                },
                    datalabels: {
                        color: "#000000",
                        anchor: "end",
                        align: "end"
                    },
                                title: {
                                    display: true,
                                    text: title_text,
                                    color: '#1F1F1F',
                                    font: {
                                      size: 15
                                    }
                                }
                        },
                        layout: {
                            padding: {
                                top: 30
                            }
                        },
                }

                });
                let colors = [  'rgba(192, 0, 0, 0.7)',
				'rgba(245, 200, 0, 0.7)',
				'rgba(0, 153, 0, 0.7)']
                let lables_list = json_data.plot_settings.lables;

                for (let lable in lables_list){
                        plot.data.labels.push(lables_list[lable]);
                }
                key_value = json_data.percents[key];
                plot.data.datasets[0] = {};
                plot.data.datasets[0].data = [];
                plot.data.datasets[0].backgroundColor = [];
                plot.data.datasets[0].label = "";

                plot.data.datasets[0].data.push(key_value.value["Понизили"]["%"]);
                plot.data.datasets[0].backgroundColor.push(colors[0]);
                plot.data.datasets[0].data.push(key_value.value["Подтвердили"]["%"]);
                plot.data.datasets[0].backgroundColor.push(colors[1]);
                plot.data.datasets[0].data.push(key_value.value["Повысили"]["%"]);
                plot.data.datasets[0].backgroundColor.push(colors[2]);

                plot.data.datasets[0].borderColor = [
                    'rgba(255, 0, 0, 1);'
                    ];
                 plot.data.datasets[0].borderWidth = 1
        plot.update();
        div_title.innerHTML += content_text;
        for(let i in sub_content_list){
        sub_content = sub_content_list[i];
        let h3 = document.createElement('h3');
        let text = document.createTextNode(sub_content);
        h3.appendChild(text);
        div_subtitle.appendChild(h3);
        }
        div.appendChild(div_title);
        div.appendChild(div_subtitle);
        div.appendChild(canvas);
        container.appendChild(div);
        section.appendChild(container);
        body.appendChild(section);
        return plot;
        };
function createTable_type_1(jsonObj, key, index){
  let fieldTitles = jsonObj.table_settings.titles;
  let fields = jsonObj.table_settings.fields;

  let body = document.getElementById('report_container_' + index);
  let div = document.createElement('div');
  div.className = "TwoPage__wrapper";
  let title = document.createElement('h3');
  title.className = "TwoPage__wrapper_title";
  let text = document.createTextNode('Таблица результатов:');
  let tbl = document.createElement('table');
  let thr = document.createElement('tr');
  let tbdy = document.createElement('tbody');

  fieldTitles.forEach((fieldTitle) => {
    let th = document.createElement('td');
    th.appendChild(document.createTextNode(fieldTitle));
    thr.appendChild(th);
  });
  tbdy.appendChild(thr);
  let row_names = ["Понизили", "Подтвердили", "Повысили", "Всего"];
  for (row in row_names){
        let tr = document.createElement('tr');
	var td = document.createElement('td');
        td.appendChild(document.createTextNode(jsonObj.table_settings.groups[row]));
        tr.appendChild(td);

        for (row_key of ["count_of_students", "%"]){
              var td = document.createElement('td');
                td.appendChild(document.createTextNode(jsonObj.percents[key].value[row_names[row]][row_key]));
                tr.appendChild(td);
        }
        tbdy.appendChild(tr);
  }
  title.appendChild(text);
  div.appendChild(title);
  tbl.appendChild(tbdy);
  div.appendChild(tbl);
  body.appendChild(div);
  return tbl;
};


$(document).ready(function(){
        $("#submit_btn").click(function(){

                var id_district = $('#district').val();
                var id_oo = $('#oo').val();
                var id_oo_parallels = $('#parallel').val();
                var id_oo_parallels_subjects = $('#subject').val();
                var id_report = $('#report').val();


                var sendInfo = {
                district: {
                        'id': id_district,
                        "name": $( "#district option:selected" ).text()
                        },

                oo:     {
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
        if (id_district == null){
                $('#district').after('<span class="error">Это поле не может быть пустым</span>');
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
			$(".TwoPage").remove();
			if (id_report == 0){
                        	draw_report_type_0(jsonObj);
                        	createTable_type_0(jsonObj);
			}
			if (id_report == 1){
				 draw_report(jsonObj);
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

$(document).ready(function(){
        $("#clear_btn").click(function(){
                $(".error").remove();
                $(".TwoPage").remove();

                parallel_select.innerHTML = "";
                subject_select.innerHTML = "";
                report_select.innerHTML = "";

                district = district_select.value;
                fetch('oo/' + district).then(function(response){
                        response.json().then(function(data) {
                                optionHTML = '';
                                for (oo of data.oo) {
                                        optionHTML += '<option value="' + oo.id+'">' + oo.name + '</option>'
                                }
                                oo_select.innerHTML = optionHTML;
                                oo_select.value = "";
                        });
                });
        });
});

