import React from 'react';
import Gallery from './Gallery';
import './JourneyDetails.css'; // Import your CSS file
import PostInfoTable from './TiLePost';
import { faMotorcycle, faCar, faBus, faBicycle,faTag } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

const JourneyDetails = ({ journey, pictures, tags }) => {
  const formatCurrency = (value) => {
    return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(value);
  };
  const formatDate = (dateString) => {
    const options = { day: '2-digit', month: '2-digit', year: 'numeric' };
    return new Date(dateString).toLocaleDateString('vi-VN', options);
  };
  const getVehicleIcon = (vehicleType) => {
    switch (vehicleType) {
      case 'xe may':
        return faMotorcycle;
      case 'oto':
        return faCar;
      case 'xe buyt':
        return faBus;
      case 'xe dap':
        return faBicycle;
      default:
        return null;
    }
  };
  return (
    <div className="card card-body journey-details">
      <div className="container mt-3">
        <div className="row">
          <div className="col-md-6">
            <h2>Thông tin chi tiết về hành trình</h2>
            <hr />
            <div className="card mb-3">
              <div className="card-header">
                <h5>
                  <i className="fas fa-money-bill-wave money-icon"></i>
                  <span className="chi-phi">Chi phí: {formatCurrency(journey.chiPhi)}</span>
                </h5>
              </div>
            </div>
            {journey.id_tuyenDuong && (
              <div>
                <h5>Địa điểm xuất phát dự kiến</h5>
                <ul className="list-group">
                  {journey.id_tuyenDuong.id_noiDi && (
                    <li className="list-group-item">
                      <i className="fas fa-map-marker-alt location-icon"></i>
                      Điểm đi: {journey.id_tuyenDuong.id_noiDi.diaChi} - Ngày xuất phát: {formatDate(journey.ngayDi)}
                    </li>
                  )}
                  {journey.stoplocal && journey.stoplocal.length > 0 && (
                          <>
                            <h5>Địa điểm ghé qua</h5>
                            {journey.stoplocal.map((stop, index) => (
                              <li key={index} className="list-group-item">
                                <i className="fas fa-map-marker-alt location-icon-stop"></i>
                                Điểm dừng: {stop.id_DiaDiem.diaChi} - Thời gian đến dự kiến: {formatDate(stop.thoiGianDung)}
                              </li>
                            ))}
                          </>
                        )}
                 <h5>Địa điểm kết thúc dự kiến</h5>
                  {journey.id_tuyenDuong.id_noiDen && (
                    
                    <li className="list-group-item">
                      <i className="fas fa-map-marker-alt location-icon"></i>
                      Điểm kết thúc: {journey.id_tuyenDuong.id_noiDen.diaChi} - Ngày kết thúc: {formatDate(journey.ngayDen)}
                    </li>
                  )}
                </ul>
              </div>
            )}
            {journey.id_PhuongTien && (
              <div className="card mt-3">
                <div className="card-header">
                 <h5>
                    <FontAwesomeIcon icon={getVehicleIcon(journey.id_PhuongTien.loai)} /> Phương tiện: {journey.id_PhuongTien.loai}
                  </h5>
                </div>
              </div>
            )}
            {tags && tags.length > 0 && (
              <div className="mt-3">
                <h5><FontAwesomeIcon className='tag-badge' icon={faTag} /> Tags</h5>

                <ul className="list-inline">
                  {tags.map(tag => (
                    <li key={tag.id} className="list-inline-item">
                      <span className="badge bg-secondary">{tag.name}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      </div>
        <h5 style={{'margin-left': "10px"}}>Pictures</h5>
        {pictures && pictures.length > 0 && (
          
          
          <Gallery pictures={pictures}/>
        )}

    </div>
  );
};

export default JourneyDetails;
