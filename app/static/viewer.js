
// let current_link = "http://127.0.0.1:5000/api/";
let current_id = 1;

function nextBook() {
  fetch('../../api/'+current_id)
    .then(res => newcontent = res.json())
    .then(res => {
      console.log(res);
      document.getElementById("author").innerHTML = res.author;
      document.getElementById("coverPage").src = res.coverpage;
      document.getElementById("detailInfomation").innerHTML = res.detail;
      document.getElementById("publishYear").innerHTML = res.publishyear;
      document.getElementById("fictionName").innerHTML = res.name;
      document.getElementById("fictionID").innerHTML = res.id;
      current_id++
    })
}
function preBook() {
  fetch('../../api/'+current_id)
    .then(res => newcontent = res.json())
    .then(res => {
      console.log(res);
      document.getElementById("author").innerHTML = res.author;
      document.getElementById("coverPage").src = res.coverpage;
      document.getElementById("detailInfomation").innerHTML = res.detail;
      document.getElementById("publishYear").innerHTML = res.publishyear;
      document.getElementById("fictionName").innerHTML = res.name;
      current_id--
    })
}


function viewChapterList() {
  document.getElementById("viewerContent").innerHTML = mainContent;
}

function preContent() {
  document.getElementById("viewerContent").innerHTML = "Nội dung chương trước";
}

function nextContent() {
  document.getElementById("viewerContent").innerHTML = "Nội dung chương sau";
}


const e = React.createElement;


class Fiction extends React.Component {
  constructor(props) {
    super(props);
    this.state = 1;    
  }

  render() {
    if (this.link) {
      return 'the link has not changed';
    }
    return e(
      'div', null, "current_link"
    );
  }
}

const newDomContainer = document.querySelector('#newthing');
ReactDOM.render(e(Fiction), newDomContainer);
