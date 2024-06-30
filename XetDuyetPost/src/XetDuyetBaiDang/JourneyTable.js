import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUser, faSignOutAlt, faTag } from '@fortawesome/free-solid-svg-icons';
import JourneyDetails from './JourneyDetails';
import APIs, { authApi, endpoints } from '../configs/APIs';
import PostInfoTable from './TiLePost';
import { Modal, Button, Form } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

const JourneyTable = ({ user }) => {
  const navigate = useNavigate();
  const [currentJourney, setCurrentJourney] = useState(null);
  const [journeys, setJourneys] = useState([]);
  const [postInfo, setPostInfo] = useState(null);
  const [showCancelModal, setShowCancelModal] = useState(false);
  const [cancelNote, setCancelNote] = useState('');
  const [selectedJourney, setSelectedJourney] = useState(null);

  const handleLogout = () => {
    navigate('/login');
  };

  const loadPostXetDuyet = async () => {
    try {
      const res = await authApi(localStorage.getItem("access-token")).get(endpoints['xetDuyet'](user.id));
      console.log(res.data.results);
      setJourneys(res.data.results);
    } catch (error) {
      console.error('Error fetching journeys:', error);
    }
  };

  const viewDetails = (journey) => {
    if (currentJourney && currentJourney.id === journey.id) {
      setCurrentJourney(null);
    } else {
      setCurrentJourney(journey);
    }
  };
  const sendEmail=(title,ghiChu,email)=>{
   let res= console.log(title,ghiChu,email)
     APIs.post(endpoints['apiEmail'],{
      'title':title,// chỗ này mai mốt lấy id user của bên chi tiết bài đăng
      'emailClient':email,
      "ghiChu":ghiChu
    })
  }
  const approveJourney = async (journey) => {
    try {
      console.log(journey.title);
      console.log("Approving journey:", journey);
      const res = await authApi(localStorage.getItem("access-token")).patch(endpoints['approveJourney'](journey.id), {
        state: "Publish",
      });
      console.log('Journey approved successfully:', res.data);
      loadPostXetDuyet();
       sendEmail(journey.title,"Bài viết đã xét duyệt thành công",journey.user)
    } catch (error) {
      console.error('Error approving journey:', error);
    }
  };

  const checkBaiViet = async (journeyId) => {
    try {
      const res = await authApi(localStorage.getItem("access-token")).get(endpoints['xetDuyetPost'](journeyId));
      console.log('Sensitive content probabilities:', res.data.sensitive_content_probabilities);
      setPostInfo(res.data);
    } catch (error) {
      console.error('Error checking post:', error);
    }
  };

  const cancelApproval = async () => {
    try {
      if (!selectedJourney) return;
      const res = await authApi(localStorage.getItem("access-token")).patch(endpoints['cancelApproval'](selectedJourney.id), {
        state: "Reject",
        note: cancelNote,
      });
      let note= "Bài viết của bạn đã bị hủy!!!" +"\n Lí do:"+ cancelNote
      sendEmail(selectedJourney.title,note,selectedJourney.user)

      console.log('Approval canceled successfully:', res.data);
      setShowCancelModal(false);
      setCancelNote('');
      loadPostXetDuyet();
    } catch (error) {
      console.error('Error canceling approval:', error);
    }
  };

  const handleCancel = (journey) => {
    setSelectedJourney(journey);
    setShowCancelModal(true);
  };

  useEffect(() => {
    loadPostXetDuyet();
  }, []);

  return (
    <div className="container">
      <h1>SHARE JOURNEY</h1>
      {user && (
        <div className="d-flex align-items-center mb-3">
          <FontAwesomeIcon icon={faUser} size="lg" className="mr-2" />
          <span>Welcome, {user.username}</span>
          <button className="btn btn-link ml-2" onClick={handleLogout}>
            <FontAwesomeIcon icon={faSignOutAlt} size="lg" />
          </button>
        </div>
      )}
      <table className="table table-bordered">
        <thead>
          <tr>
            <th>Title</th>
            <th>Content</th>
            <th>Created Date</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {journeys.map(journey => (
            <React.Fragment key={journey.id}>
              <tr>
                <td>{journey.title}</td>
                <td>{journey.content}</td>
                <td>{new Date(journey.created_date).toLocaleString('en-GB')}</td>
                <td className="align-middle">
                  <div className="d-flex gap-1">
                    <button
                      className="btn btn-primary me-1"
                      type="button"
                      onClick={() => viewDetails(journey)}
                    >
                      Xem chi tiết
                    </button>
                    <button
                      className="btn btn-primary me-2"
                      type="button"
                      onClick={() => checkBaiViet(journey.id)}
                    >
                      Kiểm tra tự động bài viết
                    </button>
                    <button
                      className="btn btn-success me-1"
                      type="button"
                      onClick={() => approveJourney(journey)}
                    >
                      Đồng ý xét duyệt
                    </button>
                    <button
                      className="btn btn-danger"
                      type="button"
                      onClick={() => handleCancel(journey)}
                    >
                      Hủy xét duyệt
                    </button>
                  </div>
                </td>
              </tr>
              <tr>
                <td colSpan="4">
                  <div className={currentJourney && currentJourney.id === journey.id ? 'collapse show' : 'collapse'} id={`collapse${journey.id}`}>
                    {currentJourney && currentJourney.id === journey.id && (
                      <JourneyDetails journey={journey.journey} pictures={journey.pic} tags={journey.tags} />
                    )}
                  </div>
                </td>
              </tr>
            </React.Fragment>
          ))}
        </tbody>
      </table>
      {postInfo && (
        <div className="container mt-4">
          <PostInfoTable
            title={postInfo.title}
            content={postInfo.content}
            sensitiveContentProbabilities={postInfo.sensitive_content_probabilities}
          />
        </div>
      )}

      <Modal show={showCancelModal} onHide={() => setShowCancelModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Cancel Approval</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group controlId="formCancelNote">
              <Form.Label>Note</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter your note"
                value={cancelNote}
                onChange={(e) => setCancelNote(e.target.value)}
              />
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowCancelModal(false)}>
            Close
          </Button>
          <Button variant="danger" onClick={cancelApproval}>
            Cancel Approval
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default JourneyTable;
