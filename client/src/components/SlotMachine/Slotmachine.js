import React, { useState, useEffect, useRef } from 'react';
import './slotmachine.css'
const SlotMachine = () => {
  const [winner, setWinner] = useState(null);
  const [isRunning,setIsRunning] = useState(false)
  const loserMessages = [
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
  const matches = useRef([]);

  const RepeatButton = ({ onClick }) => (
    <button aria-label='Play again.' id='repeatButton' onClick={onClick}>Repeat</button>
  );

  const WinningSound = () => (
    <audio autoPlay className="player" preload="false">
      <source src="https://andyhoffman.codes/random-assets/img/slots/winning_slot.wav" />
    </audio>
  );

//   const Spinner = ({ onFinish, timer }) => {
//     const [position, setPosition] = useState(0);
//     const [timeRemaining, setTimeRemaining] = useState(timer);
//     const iconHeight = 80;
//     const multiplier = Math.floor(Math.random() * (4 - 1) + 1);
//     const start = ((Math.floor(Math.random() * 9)) * iconHeight) * -1;
//     const speed = iconHeight * multiplier;

//     const setStartPosition = () => start;

//     const moveBackground = () => {
//       setPosition(prevPosition => prevPosition - speed);
//       setTimeRemaining(prevTimeRemaining => prevTimeRemaining - 100);
//     };

//     const getSymbolFromPosition = () => {
//       const totalSymbols = 9;
//       const maxPosition = (iconHeight * (totalSymbols - 1) * -1);
//       let moved = (timer / 100) * multiplier;
//       let currentPosition = start;

//       for (let i = 0; i < moved; i++) {              
//         currentPosition -= iconHeight;

//         if (currentPosition < maxPosition) {
//           currentPosition = 0;
//         }      
//       }

//       onFinish(currentPosition);
//     };

//     const tick = () => {      
//       if (timeRemaining <= 0) {
//         clearInterval(timer);        
//         getSymbolFromPosition();    
//       } else {
//         moveBackground();
//       }      
//     };

//     useEffect(() => {
//       const timerId = setInterval(() => {
//         tick();
//       }, 100);

//       return () => clearInterval(timerId);
//     }, []);

//     useEffect(() => {
//       setPosition(setStartPosition());
//       setTimeRemaining(timer);
//     }, [timer]);

//     const reset = () => {
//       clearInterval(timer);
//       setPosition(setStartPosition());
//       setTimeRemaining(timer);
//       const timerId = setInterval(() => {
//         tick();
//       }, 1000);
//     };

//     return (  
//         <div>

//       <div 
//         style={{ backgroundPosition: '0px ' + position + 'px' }}
//         className={`icons`}          
//       />
//       <div onClick={reset}>stop</div>
//         </div>          
//     );
//   };

const Spinner = ({ onFinish, timer, isRunning }) => {
    const [position, setPosition] = useState(0);
    const [timeRemaining, setTimeRemaining] = useState(timer);
    const iconHeight = 80;
    const multiplier = Math.floor(Math.random() * (4 - 1) + 1);
    const start = ((Math.floor(Math.random() * 9)) * iconHeight) * -1;
    const speed = iconHeight * multiplier;
  
    const setStartPosition = () => start;
  
    const moveBackground = () => {
      setPosition(prevPosition => prevPosition - speed);
      setTimeRemaining(prevTimeRemaining => prevTimeRemaining - 100);
    };
  
    const getSymbolFromPosition = () => {
      const totalSymbols = 9;
      const maxPosition = (iconHeight * (totalSymbols - 1) * -1);
      let moved = (timer / 100) * multiplier;
      let currentPosition = start;
  
      for (let i = 0; i < moved; i++) {
        currentPosition -= iconHeight;
  
        if (currentPosition < maxPosition) {
          currentPosition = 0;
        }
      }
  
      onFinish(currentPosition);
    };
  
    const tick = () => {
      if (timeRemaining <= 0) {
        getSymbolFromPosition();
        setPosition(setStartPosition());
        // setTimeRemaining(timer);
      } else {
        moveBackground();
      }
    };
  
    useEffect(() => {
      if (isRunning) {
        const timerId = setInterval(() => {
          tick();
        }, 100);
  
        return () => clearInterval(timerId);
      }
    }, [isRunning, position]);
  
    return (
      <div>
        <div
          style={{ backgroundPosition: '0px ' + position + 'px' }}
          className={`icons`}
        />
      </div>
    );
  };
  
  
  const handleClick = () => {
    setWinner(null);
    matches.current = [];
    childRefs.forEach(ref => ref.current.reset());
  };

  const finishHandler = (value) => {
    matches.current.push(value);  

    if (matches.current.length === 3) {
      const first = matches.current[0];
      const results = matches.current.every(match => match === first);
      setWinner(results);
    }
  };

  const childRefs = [useRef(), useRef(), useRef()];

  return (
    <div>
      {winner && <WinningSound />}
      <h1 style={{ color: 'white'}}>
        <span>{winner === null ? 'Waiting…' : winner ? '🤑 Pure skill! 🤑' : loserMessages[Math.floor(Math.random() * loserMessages.length)]}</span>
      </h1>

      <div className={`spinner-container`}>
        {childRefs.map((ref, index) => (
          <Spinner key={index} isRunning={isRunning} onFinish={finishHandler}  ref={ref} timer={[1000, 1400, 2200][index]} />
        ))}
      </div>
       <div className='text-slate-100'>
        
        {/* {!isRunning ? ( */}
        <button onClick={()=>{setIsRunning((prev)=>!prev)}}>reset</button>
      {/* ) : ( */}
        {/* <button onClick={()=>{setIsRunning((prev)=>!prev)}}>Stop</button> */}
        
    {/* <button aria-label='Play again.' id='repeatButton' onClick={handleClick}></button> */}
      {/* )} */}
      </div>
      {winner !== null && <RepeatButton onClick={handleClick} />}          
    </div>
  );
};

export default SlotMachine;
