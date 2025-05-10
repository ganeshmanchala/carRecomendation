import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Find = () => {
  const navigate = useNavigate();
  const [carType, setCarType] = useState('fuel');
  const [formData, setFormData] = useState({
    min_price: '0',
    max_price: '1000',
    brand: '',
    transmission: '',
    seats: '',
    safety_rating: '',
    drivetrain: '',
    boot_space: '',
    // Fuel-specific
    fuel_type: 'any',
    mileage: '',
    power: '',
    // EV-specific
    battery_capacity: '',
    range: ''
  });

  const fuelTypes = [
    { value: 'any', label: 'Any Fuel Type' },
    { value: 'electric', label: 'Electric' },
    { value: 'petrol', label: 'Petrol' },
    { value: 'diesel', label: 'Diesel' },
    { value: 'cng', label: 'CNG' }
  ];

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    if (name === 'min_price' || name === 'max_price') {
        if (value === '' || /^\d*\.?\d*$/.test(value)) {
          setFormData(prev => ({ ...prev, [name]: value }));
        }
      } else {
        setFormData(prev => ({ ...prev, [name]: value }));
      }
   

    if (name === 'fuel_type') {
      setCarType(value === 'electric' ? 'ev' : 'fuel');
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Create cleaned data object
    const cleanedData = Object.entries(formData).reduce((acc, [key, value]) => {
      if (value !== '' && value !== null && value !== undefined) {
         acc[key] = value;
      }
      return acc;
    }, {});
  
    // Include ev flag if fuel_type is electric
    const requestData = {
      ...cleanedData,
      ev: cleanedData.fuel_type === 'electric'
    };
  
    // Remove ev flag if fuel_type was 'any'
    if (formData.fuel_type === 'any') {
      delete requestData.ev;
    }
    console.log(requestData)
    // Send POST request
    const backendUrl = import.meta.env.REACT_APP_BACKEND_URL || 'http://127.0.0.1:5000';

    fetch(`${backendUrl}/recommend`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(requestData),
      credentials: 'include' // Send cookies with request
    })
  .then(response => response.json())
      .then(data => {
        // Navigate to results page with cars data
        console.log(data)
        navigate('/results', { state: { cars: data.cars } });
      })
      .catch(error => console.error('Error:', error));
  };

  return (
    <div className="h-full flex items-center justify-center p-4 bg-gradient-to-br from-gray-900 to-blue-900 relative overflow-hidden">
      <div className="absolute inset-0 z-0">
        <div className="absolute inset-0 bg-black/60"></div>
        <img 
          src="https://images.unsplash.com/photo-1493238792000-8113da705763?ixlib=rb-1.2.1&auto=format&fit=crop&w=1920&q=80"
          alt="Car background"
          className="w-full h-full object-cover object-center"
        />
      </div>

      <div className="relative z-10 w-full max-w-4xl mx-4 bg-white/5 backdrop-blur-lg rounded-xl shadow-2xl overflow-hidden border border-white/20">
        <div className="p-8">
          <h1 className="text-4xl font-bold text-white mb-8 text-center">
            <span className="text-blue-400">🚗</span> Find Your Perfect Car
          </h1>
          
          <form onSubmit={handleSubmit} className="space-y-8">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Left Column */}
              <div className="space-y-6">
                {/* Price Range */}
                <div className="bg-white/5 p-6 rounded-xl border border-white/10">
                  <h3 className="text-lg font-semibold text-white mb-4">Price Range (₹ Lakh)</h3>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <input
                        type="number"
                        name="min_price"
                        value={formData.min_price}
                        onChange={handleInputChange}
                        className="w-full px-4 py-3 bg-white/10 text-white rounded-lg border border-white/20 focus:ring-2 focus:ring-blue-400 focus:border-transparent"
                        placeholder="Min"
                      />
                    </div>
                    <div>
                      <input
                        type="number"
                        name="max_price"
                        value={formData.max_price}
                        onChange={handleInputChange}
                        className="w-full px-4 py-3 bg-white/10 text-white rounded-lg border border-white/20 focus:ring-2 focus:ring-blue-400 focus:border-transparent"
                        placeholder="Max"
                      />
                    </div>
                  </div>
                </div>

                {/* Brand & Transmission */}
                <div className="space-y-6">
                  <div>
                    <label className="block text-sm font-semibold text-white/80 mb-3">Brand</label>
                    <input
                      type="text"
                      name="brand"
                      value={formData.brand}
                      onChange={handleInputChange}
                      className="w-full px-4 py-3 bg-white/10 text-white rounded-lg border border-white/20 focus:ring-2 focus:ring-blue-400 focus:border-transparent"
                      placeholder="Enter brand (e.g., Maruti, Hyundai)"
                    />
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-semibold text-white/80 mb-3">Transmission</label>
                      <select
                        name="transmission"
                        value={formData.transmission}
                        onChange={handleInputChange}
                        className="w-full px-4 py-3 bg-white/10 text-white rounded-lg border border-white/20 focus:ring-2 focus:ring-blue-400 focus:border-transparent"
                      >
                        <option value="" className=" text-white/50 ">Select Transmission</option>
                        <option className='bg-gray-800' value="manual">Manual</option>
                        <option className='bg-gray-800' value="automatic">Automatic</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-semibold text-white/80 mb-3">Fuel Type</label>
                      <select
                        name="fuel_type"
                        value={formData.fuel_type}
                        onChange={handleInputChange}
                        className="w-full px-4 py-3 bg-white/10 text-white rounded-lg border border-white/20 focus:ring-2 focus:ring-blue-400 focus:border-transparent"
                      >
                        {fuelTypes.map((type) => (
                          <option key={type.value} value={type.value} className="bg-gray-800">
                            {type.label}
                          </option>
                        ))}
                      </select>
                    </div>
                  </div>
                </div>
              </div>

              {/* Right Column */}
              <div className="space-y-6">
                {/* Seating & Safety */}
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-semibold text-white/80 mb-3">Seats</label>
                    <select
                      name="seats"
                      value={formData.seats}
                      onChange={handleInputChange}
                      className="w-full px-4 py-3 bg-white/10 text-white rounded-lg border border-white/20 focus:ring-2 focus:ring-blue-400 focus:border-transparent"
                    >
                      <option value="" className="text-white/50">Any Seats</option>
                      {[4, 5, 6, 7].map((num) => (
                        <option key={num} value={num} className="bg-gray-800">
                          {num} Seats
                        </option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-white/80 mb-3">Safety Rating</label>
                    <select
                      name="safety_rating"
                      value={formData.safety_rating}
                      onChange={handleInputChange}
                      className="w-full px-4 py-3 bg-white/10 text-white rounded-lg border border-white/20 focus:ring-2 focus:ring-blue-400 focus:border-transparent"
                    >
                      <option value="" className="text-white/50">Any Rating</option>
                      {[3, 4, 5].map((num) => (
                        <option key={num} value={num} className="bg-gray-800">
                          {'★'.repeat(num)}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>

                {/* Drivetrain & Boot Space */}
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-semibold text-white/80 mb-3">Drivetrain</label>
                    <select
                      name="drivetrain"
                      value={formData.drivetrain}
                      onChange={handleInputChange}
                      className="w-full px-4 py-3 bg-white/10 text-white rounded-lg border border-white/20 focus:ring-2 focus:ring-blue-400 focus:border-transparent"
                    >
                      <option value="" className="text-white/50 bg-gray-800">Select Drivetrain</option>
                      <option className='bg-gray-800' value="fwd">FWD</option>
                      <option className='bg-gray-800' value="rwd">RWD</option>
                      <option className='bg-gray-800' value="awd">AWD</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-white/80 mb-3">Boot Space (L)</label>
                    <input
                      type="number"
                      name="boot_space"
                      value={formData.boot_space}
                      onChange={handleInputChange}
                      className="w-full px-4 py-3 bg-white/10 text-white rounded-lg border border-white/20 focus:ring-2 focus:ring-blue-400 focus:border-transparent"
                      placeholder="Enter capacity"
                    />
                  </div>
                </div>

                {/* Dynamic Fields */}
                <div className="bg-white/5 p-6 rounded-xl border border-white/10">
                  {carType === 'ev' ? (
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-semibold text-white/80 mb-3">Battery (kWh)</label>
                        <input
                          type="number"
                          name="battery_capacity"
                          value={formData.battery_capacity}
                          onChange={handleInputChange}
                          className="w-full px-4 py-3 bg-white/10 text-white rounded-lg border border-white/20 focus:ring-2 focus:ring-blue-400 focus:border-transparent"
                          placeholder="Enter capacity"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-semibold text-white/80 mb-3">Range (km)</label>
                        <input
                          type="number"
                          name="range"
                          value={formData.range}
                          onChange={handleInputChange}
                          className="w-full px-4 py-3 bg-white/10 text-white rounded-lg border border-white/20 focus:ring-2 focus:ring-blue-400 focus:border-transparent"
                          placeholder="Enter range"
                        />
                      </div>
                    </div>
                  ) : (
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-semibold text-white/80 mb-3">Mileage (kmpl)</label>
                        <input
                          type="number"
                          name="mileage"
                          value={formData.mileage}
                          onChange={handleInputChange}
                          className="w-full px-4 py-3 bg-white/10 text-white rounded-lg border border-white/20 focus:ring-2 focus:ring-blue-400 focus:border-transparent"
                          placeholder="Enter mileage"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-semibold text-white/80 mb-3">Power (bhp)</label>
                        <input
                          type="number"
                          name="power"
                          value={formData.power}
                          onChange={handleInputChange}
                          className="w-full px-4 py-3 bg-white/10 text-white rounded-lg border border-white/20 focus:ring-2 focus:ring-blue-400 focus:border-transparent"
                          placeholder="Enter power"
                        />
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>

            <div className="flex justify-center mt-10">
              <button
                type="submit"
                className="w-full lg:w-1/2 py-4 px-8 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl transition-all duration-300 transform hover:scale-105 shadow-xl flex items-center justify-center space-x-3"
              >
                <span>Find My Car</span>
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                </svg>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Find;
