import $ from 'jquery';
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.css';
import flatpickr from 'flatpickr';
import { English, Russian } from "flatpickr/dist/l10n/ru.js";

var sel_date = new Date();
var sel_time = '00';

var min_date = sel_date;
var max_date = new Date();
max_date.setDate(min_date.getDate() + 3);
$("#min_date").text("От: " + min_date.toLocaleDateString())
$("#max_date").text("До: " + max_date.toLocaleDateString());

var pickr = flatpickr("#datetime", {
    dateFormat: "Y-m-d",
    defaultDate: sel_date,
    locale: Russian,
    onChange: function(selectedDates, dateStr, instance) {
        sel_date = dateStr;
        var datetime = new Date(`${sel_date}T${sel_time}:00:00Z`);
    }
});

pickr.set('minDate', min_date.toJSON().slice(0,10));
pickr.set('maxDate', max_date.toJSON().slice(0,10));

$("input[name='time']").change(function(){
    sel_time = $('input[name=time]:checked').val();
    var datetime = new Date(`${sel_date}T${sel_time}:00:00Z`);
});
