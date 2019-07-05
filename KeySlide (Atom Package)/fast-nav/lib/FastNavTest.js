class FastNavTest{
  constructor(testingSequence){
    this.index = 1;
    this.testingData = testingSequence;
    this.recordData = [];
  }

  nextIndex(){
    this.index += 1;
  }

  testComplete(){
    if(this.testingData[this.index]){
      return false;
    }
    return true;
  }

  getWord(){
    if(!this.testComplete()){
      return this.testingData[this.index]["word"];
    }
    return " ";
  }

  getReplacement(){
    return this.testingData[this.index]["replacement"];
  }

  testText(text){
    var word = " " + this.getReplacement() + " ";
      if(text){
          if(text.indexOf(word) > -1){
          this.nextIndex();
      }
    }
  }

  record(event, data){
    this.recordData.push([event, data, new Date() - 0]);
  }

  getRecordedData(){
    return this.recordData;
  }
}

module.exports = FastNavTest;
