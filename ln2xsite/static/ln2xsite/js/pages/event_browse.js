$('#filter input, #filter select').change(function() { // catch the form's input change event
    $(this).submit();
});
$('#filter button').click(function() { // catch the form's input change event
    $(this).submit();
});
$('#filter').submit(function() { // catch the form's input change event
    $.ajax({ // create an AJAX call...
        data: $(this).serialize() + '&querystring_key=entry_list', // get the form data
    type: $(this).attr('method'), // GET or POST
    url: $(this).attr('action'), // the file to call
    success: function(response) { // on success..
        $('#filter-result').slideUp( 400, function(){
            $(this).html(response);
        }); // update the DIV
    
    }
    });
    return false; // cancel original event to prevent form submitting
});

var targetNodes         = $("#filter-result");
var MutationObserver    = window.MutationObserver || window.WebKitMutationObserver;
var myObserver          = new MutationObserver (mutationHandler);
var obsConfig           = { childList: true, characterData: false, attributes: false, subtree: false };

//--- Add a target node to the observer. Can only add one node at a time.
targetNodes.each ( function () {
    myObserver.observe (this, obsConfig);
} );

function mutationHandler (mutationRecords) {
    targetNodes.hide().slideDown();
}
