var fiction_id = document.getElementById("fictionID").getAttribute("data");
var fiction_list;
fetch("../../api/chapter_list_by_fiction/"+fiction_id)
.then (res => res.json())
.then (res => {
    fiction_list = res;
    console.log(fiction_list)
});


var current_order = document.getElementById("currentChapter").getAttribute("data");

function loadnewContent(chapter_order, fiction_id) {
    fetch("../../api/"+fiction_id+"/"+chapter_order)
    .then (res => res.json())
    .then (res => {
        document.getElementById("exampleModalLabel").innerHTML = res.name;
        window.scrollTo(0, 0);
        document.getElementById("viewerContent").innerHTML = res.content;
        document.getElementById('viewerContent').scroll({top:0,behavior:'smooth'});
        // document.getElementById("currentChapter").getAttribute("data")= res.id;

        console.log("success");
    })
}

function toNextChapter() {
    current_order=parseInt(current_order)+1;
    loadnewContent(current_order, fiction_id)


}
function toPreChapter() {
    current_order=parseInt(current_order)-1;
    loadnewContent(current_order, fiction_id)


}


function viewChapterList() {
    document.getElementById("viewerContent").innerHTML = mainContent;
}
