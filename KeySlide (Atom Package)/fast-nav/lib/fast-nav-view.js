'use babel';

export default class FastNavView {
  //element: null;

  constructor(serializedState) {
    // Create root element
    this.columnWidth = 12.05;
    this.rowHeight = 30;
    this.element = document.createElement('div');
    this.element.classList.add('fast-nav');
    this.element.textContent = "";
    this.element.style.background = "transparent";
    this.element.style.opacity = "0.85";
    this.element.style.width = (this.columnWidth) + "px";
    this.element.style.height = (this.rowHeight) + "px";
    this.element.style.position = "absolute";
    this.element.style.left = "50px";
    this.element.style.top = "50px";
    this.color = "red";

    if(atom.views.getView(atom.workspace).querySelector('.vertical .item-views .scroll-view')){
      this.parent = atom.views.getView(atom.workspace).querySelector('.vertical .item-views .scroll-view').firstChild;
      this.parent.appendChild(this.element);

      this.dimensions = [
        this.parent.offsetWidth,
        this.parent.offsetHeight
      ];
    }




    // Create message element
    //const message = document.createElement('div');
    //message.textContent = 'The FastNav package is Alive! It\'s ALIVE!';
    //message.classList.add('message');
    //this.element.appendChild(message);
    //(this.Parent = (atom.views.getView(atom.workspace)).querySelector('.vertical')).appendChild(this.element.el);
  }

  activateWord(word){
    var lines = this.parent.getElementsByClassName("line");

    var text;
    var found = false;
    var x;
    var y = 0;
    for(y in lines){
      text = lines[y].innerText;
      if(text){
        x = text.indexOf(word);
      }

      if(x > -1){
        found = true;
        break;
      }
    }

    const padding = 4
    x = parseInt(x);
    y = parseInt(y);
    if(found){
      this.element.style.visibility = "visible";
      this.element.style.left = (x*this.columnWidth - 1.5*padding) + "px";
      this.element.style.top = (y*this.rowHeight) + "px";
      this.element.style.width = (word.length*this.columnWidth + 3*padding) + "px";
      this.element.style.height = (this.rowHeight + padding) + "px";
      this.element.style["border-style"] = "solid";
      this.element.style["border-width"] = "4px";
      this.element.style["border-radius"] = "5px";
      this.element.style["border-color"] = "red";

      this.element.style.background = "transparent";
      this.element.style.opacity = 0.5;
    } else{
      this.element.style.visibility = "hidden";
      console.log('not found: ' + word)
    }
  }

  // Returns an object that can be retrieved when package is activated
  serialize() {}

  // Tear down any state and detach
  destroy() {
    this.element.remove();
  }

  getElement() {
    return this.element;
  }

  trainingActivate(position){
    this.element.style.visibility = "visible";
    this.element.style.left = position[1] + "px";
    this.element.style.top = position[0] + "px";
    this.element.style.background = this.color;
  }

  wait(){
    this.color = "blue";
    this.element.style.background = this.color;
  }

  stopWait(){
    this.color = "red";
    this.element.style.background = this.color;
  }

  deactivate(){
    this.element.style.visibility = "hidden";
  }

  getPageDimensions(){
    return this.dimensions;
  }

  trainingCompleted(){
    this.element.textContent = "Training Completed";
    this.element.style.width = "120px";
    this.element.style.height = "60px";
    this.element.style.top = "0px";
    this.element.style.left = "0px";
    this.element.style.opacity = "1";
    this.element.style.background = "#404040";
    this.element.style.color = "white";
  }

  testingCompleted(){
    this.element.textContent = "Testing Completed";
    this.element.style.width = "120px";
    this.element.style.height = "60px";
    this.element.style.top = "0px";
    this.element.style.left = "0px";
    this.element.style.opacity = "1";
    this.element.style.background = "#404040";
    this.element.style.color = "white";
  }
}
