$(".adjustable").each(function() {
    $e = $(this);

    let up = $e.find(".up-arrow");
    let input = $e.find(":input");
    let down = $e.find(".down-arrow");

    if (input.prop("type") === "text") {
        up.on("click", function() {
            var currentSP = parseFloat(input.val());
            input.val(currentSP + 0.5);         
        })

        down.on("click", function() {
            var currentSP = parseFloat(input.val());
            input.val(currentSP - 0.5);         
        })
    } else if (input.prop("type") === "time") {
        up.on("click", function() {
            input[0].stepUp(15);
        })

        down.on("click", function() {
            input[0].stepDown(15);
        })
    }
})
