import {Modal} from 'react-bootstrap';
import App1 from '../../../components/SlotMachine/Main';    
// import runApp from '../../../components/slotmachine/.Slotmachine';
function SlotMachineModal(props) {
    console.log(props);
    return (
      <Modal
        {...props}
        aria-labelledby="contained-modal-title-vcenter"
        // aria-labelledby="example-custom-modal-styling-title"
        centered
        // size="lg"
        dialogClassName="modal-90w"
      >
        {/* <Modal.Header closeButton>
          <Modal.Title id="contained-modal-title-vcenter">
            Slot machine
          </Modal.Title>
        </Modal.Header> */}
        <Modal.Body>
         <App1/>
        </Modal.Body>
      </Modal>
    );
  }


export default SlotMachineModal;