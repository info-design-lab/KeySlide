class FastNavAlgo {
    constructor()
    {
        this.keyPressedX = [];
        this.keyPressedY = [];
        this.time = [];
        this.cursorPos = null;
        this.latestCursorPos = null;
        this.slope = [];
        this.columnWidth = 0;
        this.rowHeight = 0;
        this.fastNavView = null;
        this.speed = 0.05;
        // keyboard positions of keys
        this.keyCoord = {"Tilda": {"x": 17.5, "y": 163.91}, "Digit1": {"x": 55.22, "y": 163.91}, "Digit2": {"x": 92.89, "y": 163.91}, "Digit3": {"x": 130.508, "y": 163.91}, "Digit4": {"x": 168.158, "y": 163.91}, "Digit5": {"x": 205.808, "y": 163.91}, "Digit6": {"x": 243.458, "y": 163.91}, "Digit7": {"x": 281.108, "y": 163.91}, "Digit8": {"x": 318.758, "y": 163.91}, "Digit9": {"x": 356.408, "y": 163.91}, "Digit0": {"x": 394.058, "y": 163.91}, "Minus": {"x": 431.708, "y": 163.91}, "Equal": {"x": 469.358, "y": 163.91}, "KeyQ": {"x": 74.033, "y": 127.15}, "KeyW": {"x": 111.722, "y": 127.15}, "KeyE": {"x": 149.372, "y": 127.15}, "KeyR": {"x": 187.022, "y": 127.15}, "KeyT": {"x": 224.672, "y": 127.15}, "KeyY": {"x": 262.322, "y": 127.15}, "KeyU": {"x": 299.972, "y": 127.15}, "KeyI": {"x": 337.622, "y": 127.15}, "KeyO": {"x": 375.272, "y": 127.15}, "KeyP": {"x": 412.922, "y": 127.15}, "BracketLeft": {"x": 450.572, "y": 127.15}, "BracketRight": {"x": 488.222, "y": 127.15}, "Backslash": {"x": 525.872, "y": 127.15}, "KeyA": {"x": 83.484, "y": 90.438}, "KeyS": {"x": 121.129, "y": 90.438}, "KeyD": {"x": 158.629, "y": 90.438}, "KeyF": {"x": 196.129, "y": 90.438}, "KeyG": {"x": 233.629, "y": 90.438}, "KeyH": {"x": 271.129, "y": 90.438}, "KeyJ": {"x": 308.629, "y": 90.438}, "KeyK": {"x": 346.129, "y": 90.438}, "KeyL": {"x": 383.629, "y": 90.438}, "Semicolon": {"x": 421.129, "y": 90.438}, "besideColon": {"x": 458.629, "y": 90.438}, "KeyZ": {"x": 102.293, "y": 54.345}, "KeyX": {"x": 139.793, "y": 54.345}, "KeyC": {"x": 177.293, "y": 54.345}, "KeyV": {"x": 214.793, "y": 54.345}, "KeyB": {"x": 252.293, "y": 54.345}, "KeyN": {"x": 289.793, "y": 54.345}, "KeyM": {"x": 327.293, "y": 54.345}, "Comma": {"x": 364.793, "y": 54.345}, "Period": {"x": 402.293, "y": 54.345}, "Slash": {"x": 439.793, "y": 54.345}}
    }

    setCursorPos(pos){
      this.cursorPos = pos;
    }

    setLatestCursorPos(pos){
      this.latestCursorPos = pos;
    }

    RegisterKeyPress(code)
    {
        if(this.time.length > 0){
            if(new Date() - this.time[this.time.length - 1] > 500){
                this.ClearData();
                this.cursorPos = this.latestCursorPos;
            }
        }
        this.keyPressedX.push(this.keyCoord[event.code].x);
        this.keyPressedY.push(this.keyCoord[event.code].y);
        this.time.push(new Date() - 0);
    }

    ClearData(){
      this.keyPressedX = [];
      this.keyPressedY = [];
      this.time = [];
      this.slope = [0, 0];
    }

    LenOfData()
    {
        return this.keyPressedX.length;
    }

    getCursorPosition(mode){
      const row = this.cursorPos.row;
      const col = this.cursorPos.column;
      if(mode == "primary"){
          if(this.keyPressedX.length > 1){
              const len = this.keyPressedX.length;
              const dx = this.keyPressedX[len - 1] - this.keyPressedX[len - 2];
              const dy = this.keyPressedY[len - 1] - this.keyPressedY[len - 2];

              if(this.dist(dx, dy) > 70){ // if consecutive keys are too far apart, then break the gesture
                this.setDataToLastValue();
              }
              else{
                const theta = Math.atan2(dy, dx)*180/Math.PI;
                if(theta < 1 && theta > -1){
                  return "right";
                }
                else if(theta > 179 || theta < -179){
                  return "left";
                }
                else if(theta < 145 && theta > 60){
                  return "up";
                }
                else if(theta > -145 && theta < -60){
                  return "down";
                }
              }
          }
      }
      else if(mode == "secondary"){
        if(this.keyPressedX.length > 1){
          const t = ((new Date()) - this.time[0]); // Current time - time when gesture started
          const M = this.getSlope();
          this.setSpeed();
          return [
                    Math.round(row - M[1]*t*this.speed/this.rowHeight),
                    Math.round(col + M[0]*t*this.speed/this.columnWidth)
                 ];
        }
      }

      return [row, col];
    }

    getSlope(){
        const len = this.keyPressedX.length;

        if(len > 1){
          return this.slopeOptimization()

          /*
          const Mx = this.keyPressedX[len - 1] - this.keyPressedX[0];
          const My = this.keyPressedY[len - 1] - this.keyPressedY[0];
          const norm = Math.sqrt(Mx*Mx + My*My);
          return [Mx/norm, My/norm];
          */
        }

        return [0, 0];
    }

    slopeOptimization(){
      var thetas = [];
      var weights = [];
      for(var i = 1; i < this.keyPressedX.length; i++){
        thetas.push(Math.atan2(this.keyPressedY[i] - this.keyPressedY[0], this.keyPressedX[i] - this.keyPressedX[0]));
        weights.push(i/this.keyPressedX.length);
      }

      var num = 0;
      var denom = 0;
      for(var i in thetas){
        num += thetas[i]*weights[i];
        denom += weights[i]
      }

      var t = num/denom;
      return [Math.cos(t), Math.sin(t)]
    }

    setDataToLastValue(){
      if(this.keyPressedX.length > 0){
        const x = this.keyPressedX[this.keyPressedX.length - 1];
        const y = this.keyPressedY[this.keyPressedY.length - 1];
        this.keyPressedX = [];
        this.keyPressedX.push(x);
        this.keyPressedY = [];
        this.keyPressedY.push(y);
      } else{
        this.keyPressedX = [];
        this.keyPressedY = [];
      }
      this.time = [];
      this.time.push(new Date() - 0);
    }

    getKeyData(){
      return [this.keyPressedX, this.keyPressedY, this.time]
    }

    setSpeed(){
      var ti = [];
      var wi = [];
      for(var i = 0; i < this.time.length - 1; i++){
        ti.push(this.time[i + 1] - this.time[i]);
        wi.push(0.3/this.dist(this.keyPressedX[i + 1] - this.keyPressedX[i], this.keyPressedY[i + 1] - this.keyPressedY[i]));
      }

      var num = 0;
      var denom = 0;
      for(var i in ti){
        num += ti[i]*wi[i];
        denom += wi[i];
      }

      const t = num/denom;
      this.speed = 12683.8*(t)**(-2.1751)/2; // from best fit values
    }

    setColumnWidth(w){
      this.columnWidth = w;
    }

    setRowHeight(h){
      this.rowHeight = h;
    }

    dist(dx, dy){
      return Math.sqrt(dx*dx + dy*dy);
    }

    sumList(list){
      var sum = 0;
      for(var i in list){
        sum += list[i];
      }
      return sum;
    }
}

module.exports = FastNavAlgo;
