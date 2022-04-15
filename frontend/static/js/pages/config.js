$(".adjustable").each(function() {
    $e = $(this);

    let up = $e.find(".up-arrow");
    let input = $e.find(":input");
    let down = $e.find(".down-arrow");

    up.on("click", function() {
        var currentSP = parseFloat(input.val());
        input.val(currentSP + 0.5);         
    })

    down.on("click", function() {
        var currentSP = parseFloat(input.val());
        input.val(currentSP - 0.5);         
    })
})
