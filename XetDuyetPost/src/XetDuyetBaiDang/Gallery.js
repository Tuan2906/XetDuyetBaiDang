import React from 'react';
import 'lightbox2/dist/js/lightbox.min.js';

const Gallery = ({ pictures }) => {
    const scrollGallery = (galleryId, direction) => {
        const gallery = document.getElementById(galleryId);
        const scrollDistance = direction === 'left' ? -200 : 200;
        gallery.scrollBy({
            left: scrollDistance,
            behavior: 'smooth'
        });
    };

    return (
        <div>
            <div className="overflow-auto p-3 mb-3 bg-light gallery" style={{ maxWidth: '100%', maxHeight: '500px' }} id="gallery">
                {pictures.map((picture, index) => (
                    <a href={picture.picture} data-lightbox="gallery" data-title={`Image ${index + 1}`} key={index}>
                        <img src={picture.picture} alt={`Image ${index + 1}`} className="img-thumbnail m-2" style={{ width: '150px', height: '150px' }} />
                    </a>
                ))}
            </div>
            <div className="text-center mt-3">
                <button className="btn btn-primary me-2" onClick={() => scrollGallery('gallery', 'left')}>
                    Previous
                </button>
                <button className="btn btn-primary" onClick={() => scrollGallery('gallery', 'right')}>
                    Next
                </button>
            </div>
        </div>
    );
};

export default Gallery;
