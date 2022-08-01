$(document).ready(function () {
  $('a.external').attr('target', '_blank');
  $('p:last').append(
    '<br><a href="https://www.flaticon.com/free-icons/comic-book" title="comic book icons">Comic book icons created by Freepik - Flaticon</a>'
  );
  $('.buttons p a').removeAttr('target');
});
