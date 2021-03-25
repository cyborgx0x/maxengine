let db;
const download = document.querySelector('#downloadDiv');
download.addEventListener("click", downloadFiction)
function downloadFiction() {
    let fiction = indexedDB.open('fictiondb',1);
    fiction.onsuccess = function() {
        console.log('Database opened succesfully');
        db = fiction.result;
        addData(db);
      };
    download.textContent = "Đang tải về, đợi tí";

    fiction.onupgradeneeded = function(e) {
        var db = e.target.result;
        var fiction = db.createObjectStore('fiction', { autoIncrement: true });
        fiction.createIndex('name','name', {unique:false})
        fiction.createIndex('price','price', {unique:false})
        fiction.createIndex('description','description', {unique:false})
        fiction.createIndex('created','created', {unique:false})
    };
    function addData(event) {
        let tx = db.transaction(['fiction'],'readwrite');
        let store = tx.objectStore('fiction');
        let item = {
            name: 'sandwich',
            price: 4.99,
            description: 'a very tasty sandwich',
            created: new Date().getTime()
        };
        download.textContent = "Sắp xong rồi";
        download.textContent = "Downloaded";

        ;(async () => {
            const response = await fetch('http://127.0.0.1:5000/api/1/')
            const data = await response.json()
            console.log(data)
          })()
        store.add(item);
        return tx.complete;

    };
    
};

    


    // dbPromise.then(function(db) {
    //     var tx = db.transaction('store', 'readonly');
    //     var store = tx.objectStore('store');
    //     return store.get('sandwich');
    // }).then(function(val) {
    //     console.dir(val);
    // })




