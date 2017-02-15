function getCookie(c_name) {
    if (document.cookie.length > 0) {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1) {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1)
                c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start, c_end));
        }
    }
    return "";
}

// Helper funciton for both loadUrls and loadProcessedUrls
function processUrl(url) {
    var o = typeof url == 'string' ? {key: url, url: url} : url;
    if (!o.key){
        o.key = o.url;
    }
    var rtn = {};
    for (var key in o){
        rtn[key] = o[key];
    }
    return rtn;
}

// Loads the data from a list of urls and callas the callback with the results
function loadUrls(callback, urls, results) {
    this.loadProcessedUrls(callback,
        urls.filter(function(url) {
            return url;
        }) // filter undefined urls out
        .map(processUrl), // make a 2d array
        results);
}

function loadProcessedUrls(callback, urls, results) {
    // a list of triples of the url key name, data handling function and the next url that should be requested on
    var counter = 0;
    results = results || {};

    function loadUrl(url){
        counter++;
        if (url.data){ // folowing block is for cleaning up the url so it does't slow down when paginating
            function removeDuplicate(key, value){
                var tmp = {};
                tmp[key] = value;
                url.url = url.url.replace($.param(tmp), '');
            }
            if (url.data.constructor === Array){
                url.data.forEach(function(d){
                    removeDuplicate(d.name, d.value);
                });
            } else {
                Object.keys(url.data).forEach(function(key){
                    removeDuplicate(key, url.data[key]);
                });
            }
            url.url = url.url.replace(/&{2,}/g, '');
            url.url = url.url.replace('?&', '?');
        }
        $.get(
            url.url,
            url.data,
            function(data) {
                if (data.results) { //must be a list view
                    if (results[url.key]) { // pushes all of the data elements into our results, note this assumes other data is going to be the same
                        Array.prototype.push.apply(results[url.key].results, data.results);
                    } else { // if this is the first page then it won't be in the results yet
                        results[url.key] = data;
                    }
                } else { //handle the detail view
                    results[url.key] = data;
                }

                url.url = data.next;
                if (!url.url) { // finished the pages for the first url
                    if (url.responseHandler) { // checks if has function associated with the url
                        var extraUrls = url.responseHandler(results[url.key]); //calls the function with the data recieved fromt that url
                        if (extraUrls) { //if any new urls, add them
                            extraUrls.forEach(function(extraUrl){loadUrl(processUrl(extraUrl));});
                        }
                    }
                } else {
                    loadUrl(url);
                }

                counter--;
                if (counter === 0){
                    callback(results);
                }
        });
    }

    urls.forEach(loadUrl);
}
