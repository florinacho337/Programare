function colectData(){
    return [$("#producator").find('option:selected').text(),
        $("#procesor").find('option:selected').text(),
        $("#memorie").find('option:selected').text(),
        $("#capacitateHdd").find('option:selected').text(),
        $("#placaVideo").find('option:selected').text(),
        $("#diagonala").find('option:selected').text(),
    ]
}

function showContent(){
    $.ajax({
        type : "GET",
        url : "server.php",
        data: {items :colectData()},
        success: function(data) {
            $("#myTable").html(data);
        }
    });
}

$(document).ready(function(){
    showContent();

    $('select').change(function(){
        showContent();
    });
});
