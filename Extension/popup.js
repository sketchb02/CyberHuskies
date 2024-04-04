document.addEventListener('DOMContentLoaded', function () {
    const scanHighlightButton = document.getElementById('scanHighlight');
    const scanRedactButton = document.getElementById('scanRedact');
    const highlightOptions = document.getElementById('highlightOptions');
    const redactOptions = document.getElementById('redactOptions');
    
    /*
    scanHighlightButton.addEventListener('click', function () {
        // Hide the redact options if they're showing
        redactOptions.style.display = 'none';
        // Show the highlight options
        highlightOptions.style.display = 'block';
    });
    */
   
    scanRedactButton.addEventListener('click', function () {
        // Hide the highlight options if they're showing
        highlightOptions.style.display = 'none';
        // Show the redact options
        redactOptions.style.display = 'block';
    });

    // Rest of your existing code...
    // You will need to adjust the rest of your event handlers to work with the new buttons
});
