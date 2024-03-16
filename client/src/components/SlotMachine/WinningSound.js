// const rootElement = document.getElementById('root')
import './slotmachine.css'
function WinningSound() {
  return (
  <audio autoplay="autoplay" className="player" preload="false">
    <source src="https://andyhoffman.codes/random-assets/img/slots/winning_slot.wav" />
  </audio>  
  );
}

export default WinningSound;