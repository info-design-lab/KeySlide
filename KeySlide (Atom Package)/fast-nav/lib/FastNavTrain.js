class FastNavTrain{
  constructor(testingSequence){
    this.windowDimensions = [0, 0];
    this.columnWidth = 0;
    this.rowHeight = 0;
    this.targetC = null; //target cursor position
    this.index = 1;
    this.testingData = testingSequence;
    this.recordData = [];
  }

  setColumnWidth(w){
    this.columnWidth = w;
  }

  setRowHeight(h){
    this.rowHeight = h;
  }

  setDimensions(D){
    this.windowDimensions = D;
  }

  trainComplete(){
    if(this.testingData[this.index]){
      return false;
    }
    return true;
  }

  targetCursorPosition(){
    const s = this.testingData[this.index];
    return [
      s.row, s.column
    ];
  }

  getMarkerPosition(){ //cursor position in pixels
    const s = this.testingData[this.index];
    const D = this.windowDimensions;
    return [
      s.row*this.rowHeight, (s.column - 0.5)*this.columnWidth
    ];
  }

  nextIndex(){
    this.index += 1;
  }

  reachedLocation(){
      this.index += 1;
  }

  testComplete(){
    if(this.testingData[this.index]){
      return false;
    }
    return true;
  }
}

module.exports = FastNavTrain;
