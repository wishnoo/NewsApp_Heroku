// <------- Sending data to flask when a title is clicked------->
$(document).ready(function(){
  $('a#newsLink').click(function(){
    // console.log('Description:',document.getElementById('hiddenDesc').value);
    console.log('link:',this.href);
    console.log('title:',$(this).text());
    console.log('index:',$(this).data("index"));
    var index = $(this).data("index");
    console.log('source:',$('#divloop_' + index).find('a.divloop_source').text());
    // console.log('article date:',typeof($('#divloop_' + index).find('a.divloop_time').data("value")));
    console.log('article date:',$('#divloop_' + index).find('a.divloop_time').data("value"));
    console.log('author:',$('#divloop_' + index).find('a.divloop_author').text().trim());
    console.log('content:',$('#divloop_' + index).find('div.divloop_content').text().trim());
    console.log('description:',$('#divloop_' + index).find('input.divloop_description').data("value"));

    var data = this.href;
    var title = $(this).text();
    var source = $('#divloop_' + index).find('a.divloop_source').text().trim();
    var articleDate = $('#divloop_' + index).find('a.divloop_time').data("value");
    var author = $('#divloop_' + index).find('div.divloop_author').text().trim();
    var content = $('#divloop_' + index).find('div.divloop_content').text().trim();
    var description = $('#divloop_' + index).find('input.divloop_description').data("value");

    $.ajax({
        type: "POST",
        url: "/receiver",
        contentType: "application/json",
        data: JSON.stringify({data: data, title: title, source: source, articleDate: articleDate, author: author, content: content, description: description}),
        dataType: "json",
        success: function(response) {
          // var response = JSON.parse(data);
          if(response.status == true){
            console.log("inside success function");
            console.log(response.status);
            $('input[name=relevant]').attr('checked',false);     //to reset the stars on each load
            $('input[name=like]').attr('checked',false);
            $('input[name=novelty]').attr('checked',false);
            $('input[name=readability]').attr('checked',false);
            $('input[name=authority]').attr('checked',false);
            $('#exampleModalCenter').modal('show');             // this is the bootstrap modal code to show

            startTimer();
            // window.addEventListener('focus', stopTimer);
            $(window).one("focus", stopTimer); // executes the focus handler only once in this success body
            console.log(response.status);
          }
        },
        error: function(err) {
            console.log(err);
        }
    });
  });
});

// <----- Function to show the modal ----->
function invokeModal(){
  $('#exampleModalCenter').modal('show');         // this is the bootstrap modal code to show
}

//timer to track the time the tab was inactive
function startTimer() {
console.log('blur');
myInterval = window.setInterval(timerHandler, 1000);
}
// Stop timer
function stopTimer() {
window.clearInterval(myInterval);
console.log(count);
updateTimer(count);
count = 0;
}
// handler related to the timer
function timerHandler() {
count++;
// document.getElementById("seconds").innerHTML = count;
// console.log(count);
}

function updateTimer(count) {
  $.ajax({
              type: "POST",
              url: "/timer",
              contentType: "application/json",
              data: JSON.stringify({count: count}),
              dataType: "json",
              success: function(response) {

                console.log(response.status);
              },
              error: function(err) {
                  console.log(err);
              }
  });
}


// function to load the divs which are hidden by default
$(document).ready(function() {
  size_div = $("div.apiData").length;
  console.log("the no of div with class apiData",size_div);
  // $('div.apiData:lt('+x+')').show();
  // $("div.apiData").slice(0, 50).show();
  // $("div:hidden").slice(0,50).show();
  // $('#moreButton').click(function () {
    // x= (x+50 <= size_div) ? x+50 : size_div;
    // console.log('x:',x);
    // $("div:hidden").slice(0,50).show();
    // $('div#apiData :lt('+x+')').show();
    // if(x == size_div){
    //     $('#moreButton').hide();
    // }
  //   if ($("#div:hidden").length == 0) {
  //     $("#moreButton").fadeOut('slow');
  //   }
  // });
  var count = $('.counter_length').data("value")
  console.log("count:",count);
  console.log("type of count:",typeof(count));
  // var x =10;
  if ($('#divloop_1').length){
    console.log("div loop exists");
  }
  // $("#divloop_1").show();
  // document.getElementById('divloop_1').style.display='block';

  xyz = 0
  if(count > 10){
    for(i=1; i<11; i++){
      $('#divloop_' + i).show();
      xyz+=1
    }
  } else if(xyz < count) {
    for(i=xyz; i<=count-xyz; i++){
      $('#divloop_' + i).show();
      xyz+=1
    }
  }
  if(count == xyz){
    $('#moreButton').hide();
  }
  console.log("No of divs on the screen:",xyz);

  // Execute when the moreButton is clicked
  $('#moreButton').click(function () {
    if(count - xyz >10){
      for(i=xyz+1; i<xyz+11; i++){
        $('#divloop_' + i).show();
        xyz+=1
      }
    } else if(xyz < count) {
      d = (count-xyz) + xyz
      console.log("Test");
      console.log("d:",d);
      console.log("xyz:",xyz);
      for(i=xyz+1; i<d+1; i++){
        $('#divloop_' + i).show();
        // $('#divloop_' + i).show();
        xyz+=1
      }
    }
    if(count == xyz){
      $('#moreButton').hide();
    }
    console.log("No of divs on the screen:",xyz);
  });

});
