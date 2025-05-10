import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const backendUrl = import.meta.env.VITE_API_URL|| 'http://localhost:5000';

const Login = () => {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [loginCredentials, setLoginCredentials] = useState({ Username: "", Password: "" });
  const [isSignup, setIsSignup] = useState(false);
  const [signupCredentials, setSignupCredentials] = useState({ Name: "", Username: "", Password: "", Phone: "" });

  const signupCredentialsHandle = (e) => {
    setSignupCredentials({ ...signupCredentials, [e.target.name]: e.target.value });
  };

  const loginCredentialsHandle = (e) => {
    setLoginCredentials({ ...loginCredentials, [e.target.name]: e.target.value });
  };

  const handleSignupClick = () => setIsSignup(true);
  const handleLoginClick = () => setIsSignup(false);

  const signupHandle = async (e) => {
    e.preventDefault();
    const response = await fetch(`${backendUrl}/signup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: signupCredentials.Name,
        username: signupCredentials.Username,
        password: signupCredentials.Password,
        phone: signupCredentials.Phone
      }),
      credentials: 'include'
    });

    const json = await response.json();
    if (!json.success) {
      alert(json.error);
    } else {
      console.log(json);
      setSignupCredentials({ Name: "", Username: "", Password: "", Phone: "" });
      setIsSignup(false);
    }
  };

  const loginHandle = async (e) => {
    e.preventDefault();
    try {
       await login({ username: loginCredentials.Username,
        password: loginCredentials.Password})
      navigate('/')
    } catch (error) {
      alert(error.message);
    }
  };


  return (
    <div className="h-full flex items-center justify-center bg-gradient-to-br from-gray-900 to-blue-900 relative overflow-hidden">
      <div className="absolute inset-0 z-0">
        <div className="absolute inset-0 bg-black/60"></div>
        <img
          src="https://images.unsplash.com/photo-1494976388531-d1058494cdd8?ixlib=rb-1.2.1&auto=format&fit=crop&w=1920&q=80"
          alt="Car background"
          className="w-full h-full object-cover"
        />
      </div>

      <div className="relative z-10 w-full max-w-4xl mx-4 bg-white/10 backdrop-blur-lg rounded-xl shadow-2xl overflow-hidden border border-white/20">
        <div className={`flex transition-transform duration-500`}>
          {/* Signup Section */}
          <div className="min-w-[50%] p-12">
            <h2 className="text-3xl font-bold text-white mb-8">Create Account</h2>
            <form onSubmit={signupHandle} className="space-y-6">
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-white/80 mb-2">Full Name</label>
                  <input
                    type="text"
                    name="Name"
                    value={signupCredentials.Name}
                    onChange={signupCredentialsHandle}
                    className="w-full px-4 py-3 bg-white/5 rounded-lg text-white placeholder-white/50 border border-white/20 focus:border-blue-400 focus:ring-2 focus:ring-blue-400/30"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-white/80 mb-2">Phone Number</label>
                  <input
                    type="tel"
                    name="Phone"
                    value={signupCredentials.Phone}
                    onChange={signupCredentialsHandle}
                    className="w-full px-4 py-3 bg-white/5 rounded-lg text-white placeholder-white/50 border border-white/20 focus:border-blue-400 focus:ring-2 focus:ring-blue-400/30"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-white/80 mb-2">Username</label>
                  <input
                    type="text"
                    name="Username"
                    value={signupCredentials.Username}
                    onChange={signupCredentialsHandle}
                    className="w-full px-4 py-3 bg-white/5 rounded-lg text-white placeholder-white/50 border border-white/20 focus:border-blue-400 focus:ring-2 focus:ring-blue-400/30"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-white/80 mb-2">Password</label>
                  <input
                    type="password"
                    name="Password"
                    value={signupCredentials.Password}
                    onChange={signupCredentialsHandle}
                    className="w-full px-4 py-3 bg-white/5 rounded-lg text-white placeholder-white/50 border border-white/20 focus:border-blue-400 focus:ring-2 focus:ring-blue-400/30"
                  />
                </div>
              </div>
              <button
                type="submit"
                className="w-full py-3 px-6 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition-all duration-200 transform hover:scale-[1.02] shadow-lg"
              >
                Get Started
              </button>
            </form>
          </div>

          {/* Login Section */}
          <div className="min-w-[50%] p-12">
            <h2 className="text-3xl font-bold text-white mb-8">Welcome Back</h2>
            <form onSubmit={loginHandle} className="space-y-6">
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-white/80 mb-2">Username</label>
                  <input
                    type="text"
                    name="Username"
                    value={loginCredentials.Username}
                    onChange={loginCredentialsHandle}
                    className="w-full px-4 py-3 bg-white/5 rounded-lg text-white placeholder-white/50 border border-white/20 focus:border-blue-400 focus:ring-2 focus:ring-blue-400/30"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-white/80 mb-2">Password</label>
                  <input
                    type="password"
                    name="Password"
                    value={loginCredentials.Password}
                    onChange={loginCredentialsHandle}
                    className="w-full px-4 py-3 bg-white/5 rounded-lg text-white placeholder-white/50 border border-white/20 focus:border-blue-400 focus:ring-2 focus:ring-blue-400/30"
                  />
                </div>
              </div>
              <button
                type="submit"
                className="w-full py-3 px-6 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition-all duration-200 transform hover:scale-[1.02] shadow-lg"
              >
                Drive In →
              </button>
              <p className="text-center text-white/80 mt-4">
                New here?{' '}
                <button
                  type="button"
                  onClick={handleSignupClick}
                  className="text-blue-400 hover:text-blue-300 font-semibold underline underline-offset-2"
                >
                  Create account
                </button>
              </p>
            </form>
          </div>
        </div>

        {/* Sliding Overlay */}
        <div className={`absolute top-0 w-1/2 h-full transition-all duration-500 ease-in-out ${isSignup ? 'left-1/2' : 'left-0'}`}>
          <div className="relative w-full h-full bg-gradient-to-br from-gray-900/95 to-amber-600/90">
            <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1553440569-bcc63803a83d?ixlib=rb-1.2.1&auto=format&fit=crop&w=1920&q=80')] bg-cover bg-center mix-blend-overlay opacity-20"></div>

            <div className="absolute inset-0 flex flex-col items-center justify-center p-12 text-center">
              <h2 className="text-3xl font-bold text-white mb-4">
                {isSignup ? 'Already Member?' : 'New Here?'}
              </h2>
              <p className="text-white/80 mb-8">
                {isSignup ? 'Login to access your personalized car recommendations' : 'Sign up to unlock premium features'}
              </p>
              <button
                onClick={isSignup ? handleLoginClick : handleSignupClick}
                className="px-8 py-3 bg-amber-500/90 hover:bg-amber-400 text-gray-900 font-semibold rounded-lg transition-all transform hover:scale-105 shadow-lg"
              >
                {isSignup ? 'Sign In' : 'Create Account'}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;