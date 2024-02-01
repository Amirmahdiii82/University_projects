$(document).on('click','.add-todo',function(){
var todoInputData=$(this).siblings('input').val();
var todoListData=`<div class="row-parent">
  <div class="list-row">
  <div class="list-num">&#x261B;</div>
  <div class="list-data">`+ todoInputData+`</div>
  <div class="edit-todo">&#9998;</div>
  <div class="remove-todo">&#x1F5D1;</div>
  </div>
  <div class="list-error"></div></div>`;

if($.trim(todoInputData)=='')
{
$(this).parents('.todo-content').find('.error').text('You must enter something!');
}
else{
$(this).parents('.todo-content').find('.todo-list').append(todoListData);
$(this).parents('.todo-content').find('.error').empty();
}
$(this).siblings('input').val('')
});

$(document).keydown(function (event) { 
     if (event.which == 13) { 
         event.preventDefault();
         $('.add-todo').click(); 
     } 
});

$(document).on('click','.remove-todo',function(){
 $(this).parent('.list-row').remove();
})

$(document).on('click','.edit-todo',function(){
 $(this).attr('class','update-todo');
 $(this).html('&#x2713;');
 var listText= $(this).parent('.list-row').find('.list-data').html();
 var listDataHeight=$(this).parent('.list-row').find('.list-data').innerHeight();
 $(this).parent('.list-row').find('.list-data').attr('class','update-data');

 if(listDataHeight>50){
  $(this).parent('.list-row').find('.update-data').html('<textarea style="height:'+listDataHeight+'px">'+listText+'</textarea>');
 }else{
  $(this).parent('.list-row').find('.update-data').html('<textarea style="height:'+listDataHeight+'px">'+listText+'</textarea>');
 }

});

$(document).on('click','.update-todo',function(){
 var listText= $(this).parent('.list-row').find('textarea').val();
 if($.trim(listText)=='')
  {
   $(this).parents('.row-parent').find('.list-error').text('You must enter something!');
  }else{
   $(this).attr('class','edit-todo');
   $(this).html('&#9998;');
   $(this).parent('.list-row').find('.update-data').attr('class','list-data');
   var listText= $(this).parent('.list-row').find('.list-data').html(listText);
   $(this).parents('.row-parent').find('.list-error').empty();
}
});

$(document).on('click','.list-data',function(){
 $(this).toggleClass('line-through');
});