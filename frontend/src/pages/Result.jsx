import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
 const convertPrice = (price) => {
  if (!price) return 'N/A';
  if (typeof price === 'number') return price.toFixed(2);
  const match = price.match(/(\d+\.?\d*)/);
  return match ? parseFloat(match[1]).toFixed(2) : 'N/A';
};

const ResultsPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const cars = location.state?.cars || [];

  const handleCardClick = (car) => {
    navigate('/specs', { state: { car } });
  };


  return (
    <div className="min-h-screen bg-gray-900 p-8">
      <h1 className="text-3xl font-bold text-white mb-8 text-center">
        Recommended Cars ({cars.length})
      </h1>
      
      <div className="space-y-6 max-w-7xl mx-auto">
  {cars.map((car, index) => {
    const specs = car.specs || {};
    const baseSpecs = car.base_specs || {};
    const keySpecs = specs['Key Specifications'] || {};
    const fuelPerformance = specs['Fuel & Performance'] || {};
    const dimensions = specs['Dimensions & Capacity'] || {};

    return (
      <div 
        key={index} 
        onClick={() => handleCardClick(car)}
        className="bg-gray-800 rounded-xl p-6 shadow-lg border border-gray-700 flex flex-col md:flex-row gap-6 cursor-pointer hover:border-blue-500 transition-all"
      >
        {/* Image Section */}
        <div className="md:w-1/3">
          <img 
            src={car.media?.image || 'https://via.placeholder.com/300'} 
            alt={baseSpecs.model}
            className="w-full h-48 object-cover rounded-lg"
          />
        </div>

        {/* Specs Section */}
        <div className="md:w-2/3 space-y-4">
          {/* Main Title Section */}
          <div className="border-b border-gray-700 pb-4">
            <h2 className="text-2xl font-bold text-white">{baseSpecs.model}</h2>
            <div className="flex items-center gap-4 mt-2">
              <span className="text-xl font-semibold text-emerald-400">
                ₹{baseSpecs.price} 
              </span>
              <div className="flex items-center">
                {[...Array(5)].map((_, i) => (
                  <svg
                    key={i}
                    className={`w-5 h-5 ${i < (specs.Rating || 0) ? 'text-yellow-400' : 'text-gray-600'}`}
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                ))}
              </div>
            </div>
          </div>

          {/* Key Specs Grid */}
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4 text-gray-300">
            <div>
              <p className="text-sm text-gray-400">Fuel Type</p>
              <p className="font-medium">{fuelPerformance['Fuel Type'] || 'N/A'}</p>
            </div>
            <div>
              <p className="text-sm text-gray-400">Transmission</p>
              <p className="font-medium">{car.specs["Engine & Transmission"]["Transmission Type"] || 'N/A'}</p>
            </div>
            <div>
              <p className="text-sm text-gray-400">Seating</p>
              <p className="font-medium">{dimensions['Seating Capacity'] || 'N/A'}</p>
            </div>
            <div>
              <p className="text-sm text-gray-400">{car.ev ? 'Range' : 'Mileage'}</p>
              <p className="font-medium">
                {car.ev ? keySpecs.Range : keySpecs.Mileage}
              </p>
            </div>
            <div>
              <p className="text-sm text-gray-400">Power</p>
              <p className="font-medium">{keySpecs.Power}</p>
            </div>
            <div>
              <p className="text-sm text-gray-400">Boot Space</p>
              <p className="font-medium">{car.specs["Dimensions & Capacity"]["Boot Space"]}</p>
            </div>
          </div>

          {/* Features */}
          <div className="pt-4 border-t border-gray-700">
            <h3 className="font-semibold text-white mb-2">Top Features:</h3>
            <div className="flex flex-wrap gap-2">
              {specs['Top Features']?.Features?.split(', ')?.map((feature, index) => (
                <span 
                  key={index}
                  className="px-3 py-1 bg-gray-700 rounded-full text-sm text-emerald-400"
                >
                  {feature}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>
    )
  })}
</div>

      {cars.length === 0 && (
        <div className="text-center text-gray-400 text-xl mt-12">
          No cars found matching your criteria
        </div>
      )}
    </div>
  );
};

export default ResultsPage;