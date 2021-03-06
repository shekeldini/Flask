year_select = document.getElementById('year');
district_select = document.getElementById('district');
oo_select = document.getElementById('oo');
parallel_select = document.getElementById('parallel');
subject_select = document.getElementById('subject');
report_select = document.getElementById('report');

fetch('api/select/get_year/').then(function(response){
                response.json().then(function(data) {
                        optionHTML = '';
                        for (year of data.year) {
                                optionHTML += '<option value="' + year.id+'">' + year.name + '</option>'
                        }
                        year_select.innerHTML = optionHTML;

                        if (year_select.length == 1){
                                year_select.defaultSelected = year_select[0];
                                year_select.onchange();
                        }
                        else{
                                year_select.value = "";
                        }

                });
});

year_select.onchange = function(){
    district_select.innerHTML = "";
    oo_select.innerHTML = "";
    parallel_select.innerHTML = "";
    subject_select.innerHTML = "";
    report_select.innerHTML = "";
    year = year_select.value;
    fetch('api/select/get_districts/?filter_year_id=' + year).then(function(response){
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
};


district_select.onchange = function(){
        parallel_select.innerHTML = "";
        subject_select.innerHTML = "";
        report_select.innerHTML = "";
        year = year_select.value;
        district = district_select.value;
        fetch('api/select/get_oo/?filter_year_id=' + year + "&filter_district_id=" + district).then(function(response){
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
        report_select.innerHTML = "";
        year = year_select.value;
        district = district_select.value;
        oo = oo_select.value;
        fetch('api/select/get_parallels/?filter_year_id='+ year + "&filter_district_id="+ district + "&filter_oo_id=" + oo).then(function(response){
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
        year = year_select.value;
        district = district_select.value;
        oo = oo_select.value;
        parallel = parallel_select.value;

        fetch('api/select/get_subjects/?filter_year_id='+ year + '&filter_district_id=' + district + '&filter_oo_id=' + oo + '&filter_parallel_id=' + parallel).then(function(response){
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
fetch('api/select/vpr_analysis/get_reports').then(function(response){
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
  container.className = "container_report";
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

  let btn = document.createElement('a');
  btn.className = "upload mdi mdi-download";

  let btn_url = "/api/export/?" + "filter_report_id=" + report_select.value  + "&filter_report_name=" + $( "#report option:selected" ).text() + "&filter_district_id=" + district_select.value +
  "&filter_district_name=" + $( "#district option:selected" ).text() + "&filter_oo_id=" + oo_select.value + "&filter_oo_name=" + $( "#oo option:selected" ).text() + "&filter_parallel_id=" + parallel_select.value +
  "&filter_parallel_name=" +  $( "#parallel option:selected" ).text() + "&filter_subject_id=" + subject_select.value + "&filter_subject_name=" + $( "#subject option:selected" ).text() + 
  "&filter_year_id=" + year_select.value + "&filter_year_name=" + $( "#year option:selected" ).text();

  btn.setAttribute("href", btn_url);
  let text = document.createTextNode('?????????????? ??????????????????????:');
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
  div.appendChild(btn);
  body.appendChild(div);
  window.getComputedStyle(div).opacity;
  div.className +=" in";
  return tbl;
};

function draw_report(report_type, json_data){
        if (report_type == 0){
                draw_report_type_0(json_data);
                createTable_type_0(json_data);
        }
        if (report_type == 1){
	        let content_text = json_data.plot_settings.content;
	       	let title_text = json_data.plot_settings.title;
	        let x_axis = json_data.plot_settings.x_axis;
	        let y_axis = json_data.plot_settings.y_axis;

                let index = 0;
                if (Object.keys(json_data.percents).length > 1){
                        draw_report_type_1_all(json_data, content_text, title_text, x_axis, y_axis);
                        index += 1;
                }
		if (Object.keys(json_data.percents).length <= 2){
                	for([key, sub_content_list] of Object.entries(json_data.plot_settings.sub_content)){
                        	if( key != "all"){
                        	draw_report_type_1(json_data, content_text, title_text, x_axis, y_axis, key, sub_content_list, index);
                        	createTable_type_1(json_data, key, index);
                        	index += 1;
                        	}
                	}
		}else{
			 let key = "oo";
			 let sub_content_list = json_data.plot_settings.sub_content[key];
			 draw_report_type_1(json_data, content_text, title_text, x_axis, y_axis, key, sub_content_list, index);
                         createTable_type_1(json_data, key, index);
                         index += 1;
		}
        }
        if (report_type == 2){
		createTable_type_2(json_data);
        }
}

function draw_report_type_1_all(json_data, content_text, title_text, x_axis, y_axis){
  let sub_content_list = json_data.plot_settings.sub_content.all
  let body = document.getElementById('report_place');
  let section = document.createElement('section');
  section.className = "TwoPage";
  section.id = "report_section";
  let container = document.createElement('div');
  container.className = "container_report";
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
                let col_names = ["????????????????", "??????????????????????", "????????????????"]
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
        container.className = "container_report";
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

                plot.data.datasets[0].data.push(key_value.value["????????????????"]["%"]);
                plot.data.datasets[0].backgroundColor.push(colors[0]);
                plot.data.datasets[0].data.push(key_value.value["??????????????????????"]["%"]);
                plot.data.datasets[0].backgroundColor.push(colors[1]);
                plot.data.datasets[0].data.push(key_value.value["????????????????"]["%"]);
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

  let btn = document.createElement('a');
  btn.className = "upload mdi mdi-download";

  let btn_url = "/api/export/?" + "filter_report_id=" + report_select.value  + "&filter_report_name=" + $( "#report option:selected" ).text() + "&filter_district_id=" + district_select.value +
  "&filter_district_name=" + $( "#district option:selected" ).text() + "&filter_oo_id=" + oo_select.value + "&filter_oo_name=" + $( "#oo option:selected" ).text() + "&filter_parallel_id=" + parallel_select.value +
  "&filter_parallel_name=" +  $( "#parallel option:selected" ).text() + "&filter_subject_id=" + subject_select.value + "&filter_subject_name=" + $( "#subject option:selected" ).text() + "&filter_table_type=" + key + "&filter_year_id=" + year_select.value + 
  "&filter_year_name=" + $( "#year option:selected" ).text(); 
  btn.setAttribute("href", btn_url);

  let text = document.createTextNode('?????????????? ??????????????????????:');
  let tbl = document.createElement('table');
  let thr = document.createElement('tr');
  let tbdy = document.createElement('tbody');

  fieldTitles.forEach((fieldTitle) => {
    let th = document.createElement('td');
    th.appendChild(document.createTextNode(fieldTitle));
    thr.appendChild(th);
  });
  tbdy.appendChild(thr);
  let row_names = ["????????????????", "??????????????????????", "????????????????", "??????????"];
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
  div.appendChild(btn);
  body.appendChild(div);
  window.getComputedStyle(div).opacity;
  div.className +=" in";
  return tbl;
};

function createTable_type_2(jsonObj){

  let fieldTitles = jsonObj.table_settings.titles;
  let fields = jsonObj.table_settings.fields;
  let body = document.getElementById('report_place');
  let section = document.createElement('section');
  section.className = "TwoPage";
  section.id = "report_section";
  let container = document.createElement('div');
  container.className = "container_report";
  container.id = "report_container";

  let div = document.createElement('div');
  div.className = "TwoPage__wrapper";
  let title = document.createElement('h3');
  title.className = "TwoPage__wrapper_title";

  let btn = document.createElement('a');
  btn.className = "upload mdi mdi-download";

  let btn_url = "/api/export/?" + "filter_report_id=" + report_select.value  + "&filter_report_name=" + $( "#report option:selected" ).text() + "&filter_district_id=" + district_select.value +
  "&filter_district_name=" + $( "#district option:selected" ).text() + "&filter_oo_id=" + oo_select.value + "&filter_oo_name=" + $( "#oo option:selected" ).text() + "&filter_parallel_id=" + parallel_select.value +
  "&filter_parallel_name=" +  $( "#parallel option:selected" ).text() + "&filter_subject_id=" + subject_select.value + "&filter_subject_name=" + $( "#subject option:selected" ).text() + "&filter_year_id=" + year_select.value + 
  "&filter_year_name=" + $( "#year option:selected" ).text();
  btn.setAttribute("href", btn_url);


  let text = document.createTextNode(jsonObj.content);
  let tbl = document.createElement('table');
  let thr = document.createElement('tr');
  let tbdy = document.createElement('tbody');
  var tr = document.createElement('tr');
  let description_div = document.createElement('div');
  description_div.className = "table-wrapper";
  let quality_p = document.createElement('p');
  quality_p.appendChild(document.createTextNode("???????????????? ?????????????????????? ??? ?????? ???????????????????????? ???????????????????????? ???????????? ???????????? ???? ??????????????????, ???????????????????????????????? ???????????????????? ???????????? ?? ???????????? ??????????????."));
  quality_p.className = "table-wrapper__descr";
  let quality_div = document.createElement('div');
  quality_div.appendChild(document.createTextNode("???????????????? ?????????????????????? = "));
  quality_div.className = "table-wrapper__calc";
  let quality_span = document.createElement('span');
  quality_span.appendChild(document.createTextNode('(??????-???? "5" + ??????-???? "4") / ?????????? ???????????????????? ????????????????'));
  quality_div.appendChild(quality_span);

  let performance_p = document.createElement('p');
  performance_p.appendChild(document.createTextNode("???????????????????????? ?????????????????? ???? ?????????? ?????????? ???????????????? ?? ???????????????????????????? ??????????????????."));
  performance_p.className = "table-wrapper__descr";
  let performance_div = document.createElement('div');
  performance_div.appendChild(document.createTextNode("???????????????????????? = "));
  performance_div.className = "table-wrapper__calc";
  let performance_span = document.createElement('span');
  performance_span.appendChild(document.createTextNode('(??????-???? "5" + ??????-???? "4" + ??????-???? "3") / ?????????? ???????????????????? ????????????????'));
  performance_div.appendChild(performance_span);

  let description_title = document.createElement('h3');
  description_title.appendChild(document.createTextNode('???????????????? ??????????????:'));

  description_div.appendChild(description_title);
  description_div.appendChild(quality_p);
  description_div.appendChild(quality_div);
  description_div.appendChild(performance_p);
  description_div.appendChild(performance_div);


  for (var i=0; i<2; i++){
	 var td = document.createElement('td');
 	 td.rowSpan = "2";
 	 td.appendChild(document.createTextNode(jsonObj.table_settings.titles[i]));
 	 tr.appendChild(td);

  }
  var td = document.createElement('td');
  td.colSpan = "4";
  td.appendChild(document.createTextNode("?????????????????????????? ?????????????? ?? %"));
  tr.appendChild(td);
  for (var i=6; i<jsonObj.table_settings.titles.length; i++){
         var td = document.createElement('td');
         td.rowSpan = "2";
         td.appendChild(document.createTextNode(jsonObj.table_settings.titles[i]));
         tr.appendChild(td);

  }

  tbdy.appendChild(tr);
  var tr = document.createElement('tr');
  for (var i=2; i<6; i++){
         var td = document.createElement('td');
         td.style.textAlign = "center";
         td.style.paddingLeft = "5px";

         td.appendChild(document.createTextNode(jsonObj.table_settings.titles[i]));
         tr.appendChild(td);

  }
  tbdy.appendChild(tr);

  if (Object.keys(jsonObj.table_settings.values).length == 3){
        let keys = ["all_districts", "district", "oo"];
        for (key of keys){
                let tr = document.createElement('tr');
                var td = document.createElement('td');
                td.appendChild(document.createTextNode(jsonObj.table_settings.values[key].name));
                tr.appendChild(td);
                for (field of fields){
                        var td = document.createElement('td');
                        td.appendChild(document.createTextNode(jsonObj.table_settings.values[key].value[field]));
                        tr.appendChild(td);
			}
                tbdy.appendChild(tr);
        }
  }

  if (Object.keys(jsonObj.table_settings.values).length == 2){
        let keys = ["all_districts", "district"];
        for (key of keys){
                let tr = document.createElement('tr');
                var td = document.createElement('td');
                td.appendChild(document.createTextNode(jsonObj.table_settings.values[key].name));
                tr.appendChild(td);
                for (field of fields){
                        var td = document.createElement('td');
                        td.appendChild(document.createTextNode(jsonObj.table_settings.values[key].value[field]));
                        tr.appendChild(td);
                }
                tbdy.appendChild(tr);
        }
        for ([key, dict_values] of Object.entries(jsonObj.table_settings.values.district.schools)){
                let tr = document.createElement('tr');
                var td = document.createElement('td');
                td.appendChild(document.createTextNode(key));
                tr.appendChild(td);
                for (field of fields){
                        var td = document.createElement('td');
                        td.appendChild(document.createTextNode(dict_values[field]));
                        tr.appendChild(td);
                }
                tbdy.appendChild(tr);
        }
  }
  if (Object.keys(jsonObj.table_settings.values).length == 1){
        let keys = ["all_districts"];
        for (key of keys){
                let tr = document.createElement('tr');
                var td = document.createElement('td');
                td.appendChild(document.createTextNode(jsonObj.table_settings.values[key].name));
                tr.appendChild(td);
                for (field of fields){
                        var td = document.createElement('td');
                        td.appendChild(document.createTextNode(jsonObj.table_settings.values[key].value[field]));
                        tr.appendChild(td);
                }
                tbdy.appendChild(tr);
        }
	
let items = Object.keys(jsonObj.table_settings.values.all_districts.districts)

function predicate_1(item) {
    return item.indexOf('??????????') >= 0;
}

function predicate_2(item) {
    return item.indexOf('????????') >= 0;
}

function predicate_3(item) {
    return item.indexOf('??.') >= 0;
}

const result_1 = items.reduce((res, item) => {
    res[predicate_1(item) ? 'a' : 'b'].push(item);
    return res;
}, { a: [], b: [] });

const result_2= result_1.b.reduce((res, item) => {
    res[predicate_2(item) ? 'a' : 'b'].push(item);
    return res;
}, { a: [], b: [] });

const result_3 = result_2.b.reduce((res, item) => {
    res[predicate_3(item) ? 'a' : 'b'].push(item);
    return res;
}, { a: [], b: [] });

let result = []
result = result.concat(result_1.a.sort(), result_2.a.sort(), result_3.b.sort(), result_3.a.sort())

        //for ([key, dict_values] of Object.entries(jsonObj.table_settings.values.all_districts.districts)){
	for (key of result) {
                let tr = document.createElement('tr');
                var td = document.createElement('td');
                td.appendChild(document.createTextNode(key));
                tr.appendChild(td);
let dict_values = jsonObj.table_settings.values.all_districts.districts[key];
                for (field of fields){
                        var td = document.createElement('td');
                        td.appendChild(document.createTextNode(dict_values[field]));
                        tr.appendChild(td);
                }
                tbdy.appendChild(tr);
        }
  }
  title.appendChild(text);
  div.appendChild(title);
  tbl.appendChild(tbdy);
  div.appendChild(tbl);
  div.appendChild(btn);
  div.appendChild(description_div);
  container.appendChild(div);
  section.appendChild(container);
  body.appendChild(section);
  window.getComputedStyle(div).opacity;
  div.className +=" in";
  return tbl;
};


$(document).ready(function(){
        $("#submit_btn").click(function(){
                var id_year = $('#year').val();
                var id_district = $('#district').val();
                var id_oo = $('#oo').val();
                var id_oo_parallels = $('#parallel').val();
                var id_oo_parallels_subjects = $('#subject').val();
                var id_report = $('#report').val();


                var sendInfo = {
                year: {
                        'id': year,
                        "name": $( "#year option:selected" ).text()
                        },
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
    if(id_year == null || id_district == null || id_oo == null || id_oo_parallels == null || id_oo_parallels_subjects == null || id_report == null) {
               if (id_year == null){
                year_select.style.border = "2px solid red"
               } else {
                    year_select.style.border = "2px solid #7ecd7e"

               }
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

               if (id_oo_parallels == null){
                       parallel_select.style.border = "2px solid red"
               } else {
                    parallel_select.style.border = "2px solid #7ecd7e"

               }


               if (id_oo_parallels_subjects == null){
                       subject_select.style.border = "2px solid red"
               } else {
                    subject_select.style.border = "2px solid #7ecd7e"

               }

               if (id_report == null){
                       report_select.style.border = "2px solid red"
               } 
        }else {
        district_select.style.border = "";
                oo_select.style.border = "";
                parallel_select.style.border = "";
                subject_select.style.border = "";
                report_select.style.border = "";
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
                        draw_report(id_report, jsonObj);
                        $("#submit_btn").attr("disabled", false);

        },
        error:function(){
                        alert("???????????? ??????????????");
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
                district_select.style.border = ""
                oo_select.style.border = ""
                parallel_select.style.border = ""
                subject_select.style.border = ""
                report_select.style.border = ""
                district_select.innerHTML = "";
                oo_select.innerHTML = "";
                parallel_select.innerHTML = "";
                subject_select.innerHTML = "";
                report_select.innerHTML = "";
                year_select.innerHTML = "";

                fetch('api/select/get_year/').then(function(response){
                    response.json().then(function(data) {
                        optionHTML = '';
                        for (year of data.year) {
                                optionHTML += '<option value="' + year.id+'">' + year.name + '</option>'
                        }
                        year_select.innerHTML = optionHTML;

                        if (year_select.length == 1){
                                year_select.defaultSelected = year_select[0];
                                year_select.onchange();
                        }
                        else{
                                year_select.value = "";
                        }
                    });
                });
        });
});
