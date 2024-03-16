import RepeatButton from "./Repeat";
import Spinner from "./Spinner";
import WinningSound from "./WinningSound";
import React from 'react';
import './slotmachine.css'
class App1 extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        winner: null
      }
      this.finishHandler = this.finishHandler.bind(this)
      this.handleClick = this.handleClick.bind(this);
    }  
  
    handleClick() { 
      this.setState({ winner: null });
      this.emptyArray();
      this._child1.forceUpdateHandler();
      this._child2.forceUpdateHandler();
      this._child3.forceUpdateHandler();
    }
  
    static loser = [
      'Not quite', 
      'Stop gambling', 
      'Hey, you lost!', 
      'Ouch! I felt that',      
      'Don\'t beat yourself up',
      'There goes the college fund',
      'I have a cat. You have a loss',
      'You\'re awesome at losing',
      'Coding is hard',
      'Don\'t hate the coder'
    ];
  
    static matches = [];
  
    finishHandler(value) {
      App1.matches.push(value);  
  
      if (App1.matches.length === 3) {
        const { winner } = this.state;
        const first = App1.matches[0];
        let results = App1.matches.every(match => match === first)
        this.setState({ winner: results });
      }
    }
  
    emptyArray() {
      App1.matches = [];
    }
  
    render() {
      const { winner } = this.state;
      const getLoser = () => {       
        return App1.loser[Math.floor(Math.random()*App1.loser.length)]
      }
      let repeatButton = null;
      let winningSound = null;
  
      if (winner !== null) {
        repeatButton = <RepeatButton onClick={this.handleClick} />
      }
      
      if (winner) {
        winningSound = <WinningSound />
      }
  
      return (
        <div>
          {winningSound}
          <h1 style={{ color: 'white'}}>
            <span>{winner === null ? 'Waiting…' : winner ? '🤑 Pure skill! 🤑' : getLoser()}</span>
          </h1>
  
          <div className={`spinner-container`}>
            <Spinner onFinish={this.finishHandler} ref={(child) => { this._child1 = child; }} timer="1000" />
            <Spinner onFinish={this.finishHandler} ref={(child) => { this._child2 = child; }} timer="1400" />
            <Spinner onFinish={this.finishHandler} ref={(child) => { this._child3 = child; }} timer="2200" />
            <div className="gradient-fade"></div>
          </div>
          {repeatButton}          
        </div>
      );
    }
  }  

  export default App1;