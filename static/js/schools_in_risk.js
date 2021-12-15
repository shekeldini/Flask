district_select = document.getElementById('district');
oo_select = document.getElementById('oo');
parallel_select = document.getElementById('parallel');
subject_select = document.getElementById('subject');


fetch('districts_for_schools_in_risk').then(function(response){
                response.json().then(function(data) {
                        optionHTML = '';
                        for (district of data.districts) {
                                optionHTML += '<option value="' + district.id+'">' + district.name + '</option>'
                        }
                        district_select.innerHTML = optionHTML;
			if (district_select.length == 1){
				district_select.defaultSelected = district_select[0];
				district_select.onchange();
			}
			else{
				district_select.value = "";
			}
                });
});


district_select.onchange = function(){
        parallel_select.innerHTML = "";
        subject_select.innerHTML = "";
        district = district_select.value;
        fetch('oo_for_schools_in_risk/' + district).then(function(response){
                response.json().then(function(data) {
                        optionHTML = '';
                        for (oo of data.oo) {
                                optionHTML += '<option value="' + oo.id+'">' + oo.name + '</option>'
                        }
                        oo_select.innerHTML = optionHTML;
			if (oo_select.length == 1){
                                oo_select.defaultSelected = oo_select[0];
                                oo_select.onchange();
                        }
                        else{
                                 oo_select.value = "";
                        }

                });
        });
};

oo_select.onchange = function(){
        subject_select.innerHTML = "";
	district = district_select.value;
        oo = oo_select.value;
        if (oo == "all" && district != "all"){
               fetch('parallels_by_district_for_schools_in_risk/' + district_select.value).then(function(response){
                        response.json().then(function(data) {
                                optionHTML = '';
                                for (parallel of data.parallels) {
                                        optionHTML += '<option value="' + parallel.id+'">' + parallel.name + '</option>'
                                }
                                parallel_select.innerHTML = optionHTML;
                                parallel_select.value = "";
                        });
                });
        }
	if (district == "all"){
		fetch('all_parallels_for_schools_in_risk/').then(function(response){
                        response.json().then(function(data) {
                                optionHTML = '';
                                for (parallel of data.parallels) {
                                        optionHTML += '<option value="' + parallel.id+'">' + parallel.name + '</option>'
                                }
                                parallel_select.innerHTML = optionHTML;
                                parallel_select.value = "";
                        });
                });

	}
	if(oo != "all"){
                fetch('parallels_by_oo_for_schools_in_risk/' + oo).then(function(response){
                        response.json().then(function(data) {
                                optionHTML = '';
                                for (parallel of data.parallels) {
                                        optionHTML += '<option value="' + parallel.id+'">' + parallel.name + '</option>'
                                }
                                parallel_select.innerHTML = optionHTML;
                                parallel_select.value = "";
                        });
                });
        }

};

parallel_select.onchange = function(){
        oo = oo_select.value;
        district = district_select.value;
	parallel = parallel_select.value;

        if (oo == "all" && district != "all"){
                 fetch('sbj_by_district_for_schools_in_risk/' + district + '/' + parallel).then(function(response){
                        response.json().then(function(data) {
                                optionHTML = '';
                                for (subject of data.subjects) {
                                        optionHTML += '<option value="' + subject.id+'">' + subject.name + '</option>'
                                }
                                subject_select.innerHTML = optionHTML;
                                subject_select.value = "";
                        });
                });
        }if (district == "all"){
		fetch('all_subject_for_schools_in_risk/').then(function(response){
                        response.json().then(function(data) {
                                optionHTML = '';
                                for (subject of data.subjects) {
                                        optionHTML += '<option value="' + subject.id+'">' + subject.name + '</option>'
                                }
                                subject_select.innerHTML = optionHTML;
                                subject_select.value = "";
                        });
                });

	}
	if (oo != "all"){
                fetch('sbj_by_oo_for_schools_in_risk/' + oo + '/' + parallel).then(function(response){
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

function draw_report(json_data){
	if (json_data.type == "oo"){
		let content_text = json_data.plot_settings.content;
	        let sub_content = json_data.plot_settings.sub_content
       		let title_text = json_data.plot_settings.title;
        	let x_axis = json_data.plot_settings.x_axis;
        	let y_axis = json_data.plot_settings.y_axis;
        	draw_report_type_3_for_oo(json_data, content_text, sub_content, title_text, x_axis, y_axis);
		createTable_type_3_for_oo(json_data);
	}
	if (json_data.type == "district"){
		createTable_type_3_for_district(json_data);
	}
};


function draw_report_type_3_for_oo(json_data, content_text, sub_content_list, title_text, x_axis, y_axis){
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
                                'rgba(237, 216, 26, 0.7)'];
                let lables_list = json_data.plot_settings.lables;
                for (let lable in lables_list){
                        plot.data.labels.push(lables_list[lable]);
                }
		let i = 0
		let labels = ["Оценки за прошлый семестр", "Оценки поулченные за ВПР"]
		for (key of ["last_semester_results", "vpr_results"]){
			let values = json_data.values[key]
			plot.data.datasets[i] = {};
                	plot.data.datasets[i].data = [];
               		plot.data.datasets[i].backgroundColor = [];
			plot.data.datasets[i].label = labels[i]
			for (mark of [2, 3, 4, 5]){
				plot.data.datasets[i].data.push(values[mark]);
				plot.data.datasets[i].backgroundColor.push(colors[i]);
			}
		 	plot.data.datasets[i].borderColor = ['rgba(255, 0, 0, 1);'];
                 	plot.data.datasets[i].borderWidth = 1
			i += 1
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

function createTable_type_3_for_oo(jsonObj){
  let fieldTitles = jsonObj.table_settings.titles;
  let fields = jsonObj.table_settings.fields;

  let body = document.getElementById('report_container');
  let div = document.createElement('div');
  div.className = "TwoPage__wrapper";
  let title = document.createElement('h3');
  title.className = "TwoPage__wrapper_title";

  let btn = document.createElement('button');
  btn.className = "upload mdi mdi-download";

  let text = document.createTextNode(jsonObj.table_settings.content);
  let tbl = document.createElement('table');
  let tbdy = document.createElement('tbody');

  var tr = document.createElement('tr');
  for (var i=0; i<3; i++){
         var td = document.createElement('td');
         td.rowSpan = "2";
         td.appendChild(document.createTextNode(jsonObj.table_settings.titles[i]));
         tr.appendChild(td);

  }

  var td = document.createElement('td');
  td.colSpan = "4"
  td.appendChild(document.createTextNode("Отметка по школе"))
  tr.appendChild(td);

  var td = document.createElement('td');
  td.colSpan = "4"
  td.appendChild(document.createTextNode("Отметка по ВПР"))
  tr.appendChild(td);

  tbdy.appendChild(tr);

  var tr = document.createElement('tr');
  for (var i=3; i<jsonObj.table_settings.titles.length; i++){
         var td = document.createElement('td');
	 td.style.textAlign = "center";
	 td.style.paddingLeft = "5px";

         td.appendChild(document.createTextNode(jsonObj.table_settings.titles[i]));
         tr.appendChild(td);

  }
  tbdy.appendChild(tr);
  var tr = document.createElement('tr');

  var td = document.createElement('td');
  td.appendChild(document.createTextNode(jsonObj.values.district_name));
  tr.appendChild(td);

  var td = document.createElement('td');
  td.appendChild(document.createTextNode(jsonObj.values.school_name));
  tr.appendChild(td);

  var td = document.createElement('td');
  td.appendChild(document.createTextNode(jsonObj.values.count_of_students));
  tr.appendChild(td);

  for (key of ["last_semester_results", "vpr_results"]){
    let val = jsonObj.values[key]
    for (mark of fields){
      var td = document.createElement('td');
      td.appendChild(document.createTextNode(val[mark]));
      tr.appendChild(td);
    }
  }
  tbdy.appendChild(tr);

  title.appendChild(text);
  div.appendChild(title);
  tbl.appendChild(tbdy);
  div.appendChild(tbl);
  div.appendChild(btn);
  body.appendChild(div);
  return tbl;
};


function createTable_type_3_for_district(jsonObj){
  let fieldTitles = jsonObj.table_settings.titles;
  let body = document.getElementById('report_place');
  let section = document.createElement('section');
  section.className = "TwoPage";
  section.id = "report_section";
  let container = document.createElement('div');
  container.className = "container";
  container.id = "report_container";

  let div = document.createElement('div');
  div.className = "TwoPage__wrapper";
  let title = document.createElement('h3');
  title.className = "TwoPage__wrapper_title";

  let btn = document.createElement('button');
  btn.className = "upload mdi mdi-download";


  let text = document.createTextNode(jsonObj.table_settings.content);
  let tbl = document.createElement('table');
  let thr = document.createElement('tr');
  let tbdy = document.createElement('tbody');



  var tr = document.createElement('tr');

  fieldTitles.forEach((fieldTitle) => {
  	var td = document.createElement('td');
	td.appendChild(document.createTextNode(fieldTitle));
  	tr.appendChild(td);
  });
  tbdy.appendChild(tr);

  for([key, school_list] of Object.entries(jsonObj.values)){
        for (school of school_list){
        var tr = document.createElement('tr');

                var td = document.createElement('td');
                td.appendChild(document.createTextNode(key));
                tr.appendChild(td);

                var td = document.createElement('td');
                td.style.textAlign = "left";
	        td.style.paddingLeft = "20px";
                td.appendChild(document.createTextNode(school));
                tr.appendChild(td);
	        tbdy.appendChild(tr);
        }
  }

  title.appendChild(text);
  div.appendChild(title);
  tbl.appendChild(tbdy);
  div.appendChild(tbl);
  div.appendChild(btn);
  container.appendChild(div);
  section.appendChild(container);
  body.appendChild(section);
  return tbl;
};


$(document).ready(function(){
        $("#submit_btn").click(function(){

                var id_district = $('#district').val();
                var id_oo = $('#oo').val();
                var id_parallel = $('#parallel').val();
                var id_subject = $('#subject').val();
                var id_report = 3;


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
                                'id': id_parallel,
                                "name": $( "#parallel option:selected" ).text()
                        },

                subject: {
                        'id': id_subject,
                        "name": $( "#subject option:selected" ).text()
                         },
                report: {
                        'id': id_report,
                        "name": "Школы в зоне риска"
                        }
                };
        $(".error").remove();
        if(id_district == null || id_oo == null || id_parallel == null || id_subject == null) {
               if (id_district == null){
                district_select.style.border = "2px solid red"

	       } else {
                    district_select.style.border = "2px solid #7ecd7e"

               }
	       if (id_oo == null){
 		oo_select.style.border = "2px solid red"

               } else {
                    oo_select.style.border = "2px solid #7ecd7e"

               }
	       if (id_parallel == null){
		parallel_select.style.border = "2px solid red"

               } else {
                    parallel_select.style.border = "2px solid #7ecd7e"

               }
	       if (id_subject == null) {
		subject_select.style.border = "2px solid red"

               } else {
                    subject_select.style.border = "2px solid #7ecd7e"

               }
        }else {
		district_select.style.border = "";
                oo_select.style.border = "";
                parallel_select.style.border = "";
                subject_select.style.border = "";
                $("#submit_btn").attr("disabled", true);
                $.ajax({
                type : 'POST',
                url : "/school_in_risk",
                contentType: "application/json; charset=utf-8",
                data: JSON.stringify(sendInfo),

                success: function(data){
                        marker = JSON.stringify(data);
                        var jsonObj = JSON.parse(marker);
                        $(".TwoPage").remove();
                        $("#submit_btn").attr("disabled", false);
			draw_report(jsonObj);


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
		district_select.style.border = "";
                oo_select.style.border = "";
                parallel_select.style.border = "";
                subject_select.style.border = "";
                parallel_select.innerHTML = "";
                subject_select.innerHTML = "";
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
