import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';


const Specs = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const car = location.state?.car;

  if (!car) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center text-white">
        No car details found
      </div>
    );
  }


  const flattenSpecs = (specs) => {
    const flattened = {};
    for (const [category, values] of Object.entries(specs)) {
      if (typeof values === 'object' && values !== null) {
        for (const [key, value] of Object.entries(values)) {
          if (value && value !== 'No') {
            flattened[`${category}_${key}`] = value;
          }
        }
      }
    }
    return flattened;
  };
  const carSpecs = car?.specs ? flattenSpecs(car.specs) : {};
const groupedSpecs = Object.entries(carSpecs).reduce((acc, [key, value]) => {
  const [category, ...featureParts] = key.split('_');
  const feature = featureParts.join(' ');
  
  if (!acc[category]) {
    acc[category] = [];
  }
  
  if (feature && value) {
    acc[category].push({ feature, value });
  }
  
  return acc;
}, {});

  return (
    <div className="min-h-screen bg-gray-900 p-8">
      <button
        onClick={() => navigate(-1)}
        className="mb-8 text-blue-500 hover:text-blue-400 flex items-center"
      >
        <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        Back to Results
      </button>

      <div className="max-w-7xl mx-auto bg-gray-800 rounded-xl p-6 shadow-lg border border-gray-700">
        {/* Main Header */}
        <div className="flex flex-col md:flex-row gap-6 mb-8">
          <img 
            src={car.specs.Image} 
            alt={car.specs['Overview Title']} 
            className="w-full md:w-1/3 h-64 object-cover rounded-lg"
          />
          <div className="flex-1">
            <h1 className="text-3xl font-bold text-white mb-2">{car.specs['Overview Title']}</h1>
            <div className="flex items-center gap-4 mb-4">
              <span className="text-2xl font-semibold text-emerald-400">
                ₹{car.specs.Price} Lakh
              </span>
              <div className="flex items-center">
                {[...Array(5)].map((_, i) => (
                  <svg
                    key={i}
                    className={`w-6 h-6 ${i < car.specs.Rating ? 'text-yellow-400' : 'text-gray-600'}`}
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                ))}
              </div>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4 text-gray-300">
              <div>
                <p className="text-sm text-gray-400">Fuel Type</p>
                <p className="font-medium">{car.specs["Fuel & Performance"]["Fuel Type"]}</p>
              </div>
              <div>
                <p className="text-sm text-gray-400">Transmission</p>
                <p className="font-medium">{car.specs["Engine & Transmission"]["Transmission Type"]}</p>
              </div>
              <div>
                <p className="text-sm text-gray-400">Seating</p>
                <p className="font-medium">{car.specs["Dimensions & Capacity"]["Seating Capacity"]} People</p>
              </div>
            </div>
          </div>
        </div>

        {/* Grouped Specifications */}
        {Object.entries(groupedSpecs).map(([category, specs]) => (
          <div key={category} className="mb-8">
            <h2 className="text-xl font-semibold text-white mb-4 border-b border-gray-700 pb-2">
              {category.replace(/([A-Z])/g, ' $1').trim()}
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {specs.map(({ feature, value }, index) => (
                <div key={index} className="bg-gray-700 p-4 rounded-lg">
                  <p className="text-sm text-gray-400 mb-1">{feature}</p>
                  <p className="font-medium text-white">{value}</p>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Specs;