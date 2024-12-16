$(function() {
  function serializeWithoutBlanks() {
    return $("form :input")
      .filter(function(index, element) {
        return $(element).val() != "";
      })
      .serialize();
  }

  function displayResult(result) {
    $("#apiOutput").text(JSON.stringify(result, null, 2));
    hljs.highlightBlock(document.getElementById("apiOutput"));
  }

  $("form").submit(function() {
    event.preventDefault();
    $("button").attr("disabled", true);
    $("button", this).html(
      '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span><span class="sr-only">Uploading...</span>'
    );
    $.ajax({
      url: "/api/stock-prices",
      type: "get",
      data: serializeWithoutBlanks(),
      success: function(result) {
        displayResult(result);
        $("form button").html("GET");
        $("button").removeAttr("disabled");
      }
    });
  });
});
