function onloadfunc(){
    var m, name, imagePath, d;
    d = new Date();
    m = d.getUTCMonth();
    m = ("0" + m).slice(-2);
    var y = d.getUTCFullYear();
    //name = y + '-' + m;
    name = '2018-02'
    imagePath = "images\/" + name + ".png";
    var imageInsert = '<img align="center" id="wordcloud"' + 'src=' + '"' + imagePath + '"' + 'OnError="this.src=\'images\/default.png\'\;"' + '>';
	$(wordcloud).html(imageInsert);
	jsondata(name);
}

function wrongyear(){
	alert("Please enter a date between May 2017 and February 2018.");
	location.reload();
}

function main(yearMonth) {
    var name, year;
    year = yearMonth.year.value;
    name = yearMonth.year.value + '-' + yearMonth.month.value;
	//var imageInsert = '<img id="wordcloud"'+'src='+"\""+'images\/'+name+'.png'+"\""+'OnError="this.src=\'images\/default.png\'\;"'+'>';
	var imageInsert = '<img id="wordcloud"'+'src='+"\""+'images\/'+name+'.png'+"\""+'OnError="wrongyear\(\)\;"'+'>';
    $(wordcloud).html(imageInsert);
	jsondata(name);
}

// This function mostly uses jQuery
function jsondata(name){
	//alert(name)
    var jsonPath;
    jsonPath = "https\:\/\/bioinfobot\.github\.io\/data\/" + name + ".json";
	$.getJSON(jsonPath, function(json) {
        var string, usersFreq, topWords, hashFreq, langFreq, hashArr, userArr, wordsArr, langArr;
        $(oneliner).html("Analytical results for <b>" + name + "</b> based on <b>" + json.TweetCount + "</b> tweets consisting of <b>" + json.TotalWords + "</b> total words with <b>" + json.UniqueWords + "</b> unique words.");

        usersFreq = json.UsersFreq;
        topWords = json.TopWords;
        hashFreq = json.HashFreq;
        langFreq = json.PopularLanguages;

        wordsArr = [];
        for (var i = 0; i < topWords.length; i++) {
            string = topWords[i][0] + " (" + topWords[i][1] + "), ";
            wordsArr.push(string);
        }
        $(tWords).html(wordsArr);

        userArr = [];
        for (var i = 0; i < usersFreq.length; i++) {
            string = '\<a href\=\"https\:\/\/twitter\.com\/' + usersFreq[i][0] + '"\>\@' + usersFreq[i][0] + "\<\/a\>" + " (" + usersFreq[i][1] + "), ";
            userArr.push(string);
        }
        $(uFreq).html(userArr);

        hashArr = [];
		for (var i=0; i<hashFreq.length; i++) {
			string='\<a href\=\"https\:\/\/twitter\.com\/hashtag\/'+hashFreq[i][0].slice(1)+'"\>'+hashFreq[i][0]+ "\<\/a\>"+" ("+hashFreq[i][1]+"), ";
			hashArr.push(string);
		}
		$(tHash).html(hashArr);

		langArr = [];
		for (var i=0; i<langFreq.length; i++){
		    string = langFreq[i][0] + " (" + langFreq[i][1] + "), ";
		    langArr.push(string);
        }
        $(pLang).html(langArr);

		string='\<a class\=\"downloadjson\" href\=\"https\:\/\/rohitfarmer\.github\.io\/bioinfobot\/data\/'+name+"\.json\"\>"+"Download data for "+name+" in Json format. \<\/a\>"
		$(downloadjson).html(string);
	});
}
