import React from 'react';
import './slotmachine.css'
class Spinner extends React.Component {  
    constructor(props){
      super(props);
      console.log(props)
      this.forceUpdateHandler = this.forceUpdateHandler.bind(this);
    };
  
    forceUpdateHandler(){
      this.reset();
    }; 
  
    reset() {
      if (this.timer) { 
        clearInterval(this.timer); 
      }  
  
      this.start = this.setStartPosition();
  
      this.setState({
        position: this.start,
        timeRemaining: this.props.timer        
      });
  
      this.timer = setInterval(() => {
        this.tick()
      }, 100);      
    }
  
    state = { 
      position: 0,
      lastPosition: null
    }
    static iconHeight = 188;
    multiplier = Math.floor(this.props.pos*(4-1)+1);
  
    start = this.setStartPosition();
    speed = Spinner.iconHeight * this.multiplier;    
  
    setStartPosition() {
      console.log(this.props.pos)
      return ((Math.floor((this.props.pos*9))) * Spinner.iconHeight)*-1;
    }
  
    moveBackground() {
      this.setState({ 
        position: this.state.position - this.speed,
        timeRemaining: this.state.timeRemaining - 100
      })
    }
  
    getSymbolFromPosition() {
      const { results } = this.props;
      //console.log(results)
      let { position } = this.state;
      const totalSymbols = 9;
      const maxPosition = (Spinner.iconHeight * (totalSymbols-1)*-1);
      let moved = (this.props.timer/100) * this.multiplier
      let startPosition = this.setStartPosition();
      let currentPosition = startPosition;    
  
      for (let i = 0; i < moved; i++) {              
        currentPosition -= Spinner.iconHeight;
  
        if (currentPosition < maxPosition) {
          currentPosition = 0;
        }      
      }
  
      this.props.onFinish(currentPosition);
    }
  
    tick() {      
      if (this.state.timeRemaining <= 0) {
        clearInterval(this.timer);        
        this.getSymbolFromPosition();    
  
      } else {
        this.moveBackground();
      }      
    }
  
    componentDidMount() {
      clearInterval(this.timer);
  
      this.setState({
        position: this.start,
        timeRemaining: this.props.timer
      });
  
      this.timer = setInterval(() => {
        this.tick()
      }, 100);
    }
  
    render() {
      let { position, current } = this.state;   
  
      return (            
        <div 
          style={{backgroundPosition: '0px ' + position + 'px'}}
          className={`icons`}          
        />
      )
    }
  }

  export default Spinner;