import $ from 'jquery';
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.css';
import flatpickr from 'flatpickr';
import { English, Russian } from "flatpickr/dist/l10n/ru.js";

var addr = 'http://carto.geogr.msu.ru/wavecast/maps/';

var times = ["t00", "t03", "t06", "t09", "t12", "t15", "t18", "t21"]

var sel_image;
var datestr;
var min_date;
var max_date;
var sel_date;
var sel_time = '00';
var pickr;
var sel_var = 'Hs';
var sel_reg = 'all'

function update_image() {
  sel_image = `${addr}${datestr}/${sel_date}_${sel_time}/${sel_var}_${sel_reg}_${sel_date}_${sel_time}.png`;
  $("#image").attr("src", sel_image);
}

function reset_styles() {
  $('#min_date').removeClass("btn-outline-danger").addClass("btn-outline-secondary");
  $('#btn_prev').removeClass("btn-outline-danger").addClass("btn-outline-primary");
  $('#max_date').removeClass("btn-outline-danger").addClass("btn-outline-secondary");
  $('#btn_next').removeClass("btn-outline-danger").addClass("btn-outline-primary");

  var i;
  for (i = 0; i < 8; i++) {
      $(`input[id=${times[i]}]`).prop('disabled', false);
  }

}

function check_extremes(datetime) {
  reset_styles();
  if (datetime.getHours() == min_date.getHours() &&
      datetime.getDay() == min_date.getDay() &&
      datetime.getFullYear() == min_date.getFullYear() &&
      datetime.getMonth() == min_date.getMonth()){
    $('#min_date').removeClass("btn-outline-secondary").addClass("btn-outline-danger");
    $('#btn_prev').removeClass("btn-outline-primary").addClass("btn-outline-danger");
  } else if (datetime.getHours() == max_date.getHours() &&
      datetime.getDay() == max_date.getDay() &&
      datetime.getFullYear() == max_date.getFullYear() &&
      datetime.getMonth() == max_date.getMonth()){
    $('#max_date').removeClass("btn-outline-secondary").addClass("btn-outline-danger");
    $('#btn_next').removeClass("btn-outline-primary").addClass("btn-outline-danger");

    var i;
    var time = datetime.getHours() - 3;
    for (i = 0; i < 8; i++) {
      var curtime = parseInt(times[i].substring(1, 3));
      if (curtime > time) {
          $(`input[id=${times[i]}]`).prop('disabled', true);
      }
    }

  }
}

$("input[name='time']").click(function(){
    sel_time = $('input[name=time]:checked').val();
    var datetime = new Date(`${sel_date}T${sel_time}:00:00Z`);
    check_extremes(datetime);
    update_image();
});

function set_time(datetime) {
  if (datetime <= max_date && datetime >= min_date) {
    sel_date = datetime.toJSON().slice(0,10);
    sel_time = datetime.toJSON().slice(11,13);
    pickr.setDate(sel_date);
    $(`#t${sel_time}`).click();
  }
}

function delta_time(delta) {
  var datetime = new Date(`${sel_date}T${sel_time}:00:00Z`);
  datetime.setHours(datetime.getHours() + delta);
  set_time(datetime);
}

$.get({url: addr}).then(function(page) {
  var document = $(page);

  // find all links ending with .pdf
  var refs = []
  $.each(document.find("[href]"), function(i, el) {
    refs.push($(el).attr('href'))
  });

  var i;
  for (i = 0; i < refs.length; i++) {
    datestr = refs[i].match(/[0-9]{4}-[0-9]{2}-[0-9]{2}/g);
    if (datestr) {

      min_date = new Date(datestr);
      sel_date = datestr;
      max_date = new Date(min_date);
      max_date.setDate(max_date.getDate() + 3);

      $("#min_date").text("От: " + min_date.toLocaleDateString())
      $("#max_date").text("До: " + max_date.toLocaleDateString());

      pickr = flatpickr("#datetime", {
          dateFormat: "Y-m-d",
          defaultDate: sel_date,
          locale: Russian,
          onChange: function(selectedDates, dateStr, instance) {
              sel_date = dateStr;
              var datetime = new Date(`${sel_date}T${sel_time}:00:00Z`);
              set_time(datetime);
          }
      });

      pickr.set('minDate', min_date.toJSON().slice(0,10));
      pickr.set('maxDate', max_date.toJSON().slice(0,10));

      var datetime = new Date(`${sel_date}T${sel_time}:00:00Z`);
      set_time(datetime);

      break;
    }
  }
});

$('#variable').change(function(){
    sel_var = this.value;
    update_image();
});

$('#region').change(function(){
    sel_reg = this.value;
    update_image();
});

$('#min_date').on('click', function(event) {
  set_time(min_date);
});

$('#max_date').on('click', function(event) {
  set_time(max_date);
});

$('#btn_prev').on('click', function(event) {
  delta_time(-3);
});

$('#btn_next').on('click', function(event) {
  delta_time(3);
});
