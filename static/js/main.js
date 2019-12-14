// 'use strict'
console.log('Main JS is connected successfully');

console.log('test')
// Elements
const search_input = $("#search-field-text");
const search_field_button = $('#search-field-button');
const search_group = $('#search-field-text, #search-field-button');

const filter_refresh_button = $('#filter-refresh-button')
const clear_button = $('#clear_button');


const cardblock_div = $('#replaceable-cardblock');
const paginator_button = $('#paginatorButton1');






const deposit_slider_jqobj = $("#deposit-js-range-slider");
const bonus_slider_jqobj = $("#bonus-js-range-slider");
const wager_slider_jqobj = $("#wager-js-range-slider");

let deposit_range_input_from = $('#deposit_range_input_from');
let deposit_range_input_to = $('#deposit_range_input_to');

let bonus_range_input_from = $('#bonus_range_input_from');
let bonus_range_input_to = $('#bonus_range_input_to');

let wager_range_input_from = $('#wager_range_input_from');
let wager_range_input_to = $('#wager_range_input_to');





const type_select = $('#type_select');
const sorting_select = $('#sorting-select')


let check_buttons = {
    'nodep' : $('#customCheck1'),
};


let filter_result = {
    sorting : 'bon_min_to_max',

// Checkbuttons
    checkbuttons : {
        nodep : false,
        license : false,
        safe : false,
        fresh : false,
        season : false,
    },
    

    type : 'all',

// Ranges
    dep_range : {'from': 0, 'to': 10000},
    bon_range : {'from': 0, 'to': 2000},
    wager_range : {'from': 0, 'to': 60},


    refresh : function () {
        //Code here
        console.log('Refrashing your filters')
    }

}





// Variable for AJAX pagianton mechanism
let current_page = 2;



// For AJAX Search
const delay_by_in_ms = 700
let scheduled_function = false

//Endpoints
const paginator_endpoint = '/';
const search_endpoint = 'ajax-search/';




// console.log(search_input);


// Sliders' initialization




deposit_slider_jqobj.ionRangeSlider({
    skin: "flat",    
    type: "double",
    
    // Pass in vars below data from a server
    min: 0,
    // max: 10000,
    // 
    
    // Pass into vars velow data from inputs
    from: 0,
    // to: 10000,



    // grid: true,





});

let deposit_slider = $("#deposit-js-range-slider").data("ionRangeSlider");


bonus_slider_jqobj.ionRangeSlider({
    skin: "flat",
    type: "double",
    min: 0,
    // max: 5000,
    from: 0,
    // to: 5000,
});


wager_slider_jqobj.ionRangeSlider({
    skin: "flat",
    type: "double",
    min: 0,
    // max: 50,
    from: 0,
    // to: 50,
});




// Handling filter form
let ajax_call = function (search_endpoint, request_parameters) {
    $.getJSON(search_endpoint, request_parameters)
    .done(response => {
            console.log(response)
            console.log(request_parameters)
            // fade out the artists_div, then:
            cardblock_div.fadeTo('slow', 0).promise().then(() => {
                // replace the HTML contents
                cardblock_div.html(response['html_from_view'])
                // fade-in the div with new contents
                cardblock_div.fadeTo('slow', 1)
                // stop animating search icon
                // search_icon.removeClass('blink')
            })
        })
}


$('#filter-form').on('submit', function(event){
    event.preventDefault()
    form_data = $(this).serializeArray();
    console.log(form_data);
    ajax_call(search_endpoint, {'filter': true, 'form_data': JSON.stringify(form_data)})

})







clear_button.on('click', function(e) {
    e.preventDefault();
    search_input.val('');
    ajax_call(search_endpoint, {'q':''});

})

// 

// Input argument takes JQuery obj of input element

let takeInput = function(input_element) {
    console.log(input_element.val());
    }
    

    const range_sliders = [
    {'slider': deposit_slider_jqobj, 'input_from': deposit_range_input_from, 'input_to': deposit_range_input_to },
    {'slider': bonus_slider_jqobj, 'input_from': bonus_range_input_from, 'input_to': bonus_range_input_to },
    {'slider': wager_slider_jqobj, 'input_from': wager_range_input_from, 'input_to': wager_range_input_to },
]




let slidersEventInit = function (slider, from_input, to_input) {
    from_input.on('keyup', function() {
        console.log($(this).val());
        slider.data("ionRangeSlider").update({from : $(this).val()});
    })
    
    to_input.on('keyup', function (){
        console.log($(this).val());
        slider.data("ionRangeSlider").update({to : $(this).val()});
    })
    
    slider.on('change', function() {
        let slider_values = $(this).val().split(';');
    from_input.val(slider_values[0]);
    to_input.val(slider_values[1]);
    
})
}

for (e = 0; e < range_sliders.length; e++) {
    slidersEventInit(range_sliders[e].slider, range_sliders[e].input_from, range_sliders[e].input_to); 
}


filter_refresh_button.on('click', function(e){
    e.preventDefault();
    document.getElementById('filter-form').reset();

    for (e = 0; e < range_sliders.length; e++) {
        range_sliders[e].slider.data("ionRangeSlider").reset();    
    }    

})


// OLD SLIDER RANGER&INPUTS EVENT HANDER INITIALIZATION CODE IS COMMENTED BELOW, IT IS CRUFT



// slidersEventInit(bonus_slider_jqobj, bonus_range_input_from, bonus_range_input_to);

// // Range input event handler
// deposit_range_input_from.on('keyup', function (){
    //     console.log($(this).val());
//     deposit_slider.update({from: $(this).val()});
// })

// deposit_range_input_to.on('keyup', function (){
    //     console.log($(this).val());
//     deposit_slider.update({
//         to: $(this).val(),
//     });
// })


// // Trying to synchronizate range slider and input
// deposit_slider_jqobj.on('change', function() {
//     let slider_values = $(this).val().split(';');
//     deposit_range_input_from.val(slider_values[0]);
//     deposit_range_input_to.val(slider_values[1]);
    
// })











// Checkbox event handler 
$("#customCheck1").change(function() {
    console.log('checkbutton event happens');
    if(this.checked) {
        //Do stuff
        console.log("DEPOSIT BONUS IS ON");
    }
});



// Sorting handler
sorting_select.on('change', function () {
    console.log('Sorting result ' + $(this).val());

})


// App type handler
type_select.on('change', function() {
    console.log('just typing .... ' + $(this).val());



    switch($(this).val()){
        case 'casino':
            console.log('ИЩЕМ КАЗИНО');
            break;
        case 'betting':
            console.log('ИЩЕМ BETTIGN');
            break;
        case 'all':
            console.log('ALLL');
            break;        
        default:
            console.log('DEFUALT');
            break;
    }





})




// Search handler

search_input.on('keyup', function () {
    // console.log('KEY UP!!!')
    const request_parameters = {
        q: $(this).val() // value of user_input: the HTML element with ID user-input
    }
    // console.log(request_parameters['q'])
    
    
    
    //Отдельно потом разобрать код ниже
    // Узнать почему сервер будет hammered если он будет отсутствовать 
    
    // if scheduled_function is NOT false, cancel the execution of the function
    if (scheduled_function) {
        clearTimeout(scheduled_function)
    }
    // ajax_call(endpoint, request_parameters)
    // setTimeout returns the ID of the function to be executed
    scheduled_function = setTimeout(ajax_call, delay_by_in_ms, search_endpoint, request_parameters)
    
})


// Paginaton
paginator_button.on('click', function() {
    console.log('Paginator buttons works!!!');
    const cardblock_content = $('.cardBlock')
    
    const request_parameters = {
        'super_secret' : 124125125,
        'paginator_enabled' : true,
        'page' : current_page,
    };
    


    let ajax_handler = $.getJSON( paginator_endpoint, request_parameters)
        .done( response =>  {
            // console.log("success");

            if (response.paginator_hiding) {
                paginator_button.remove();
            }
            
            //Takes html of cardblock div from server response 
            let content_to_show = $(response.html_from_view).filter(".cardBlock").html();
            // console.log(content_to_show)
            
            //Adding response cardblock to current cardblock
            $(cardblock_content[0]).append(content_to_show);


            // console.log(current_page);
            // console.log(response.page);
            // console.log(response.num_pages);
            
            current_page++;
        })
        .fail(function() {
          console.log( "error" );
        })





})