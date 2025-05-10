import React from "react";

const Logo = () => {
  return (
    <svg
      width="200"
      height="60"
      viewBox="0 0 200 60"
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* Import a rounded, bold sans-serif font (Rubik) from Google Fonts */}
      <style>
        {`
          @import url('https://fonts.googleapis.com/css2?family=Rubik:wght@700&display=swap');
          .saveit-text {
            font-family: 'Rubik', sans-serif;
            font-weight: 700;
            font-size: 40px;
            fill: #1a42b9; /* Vibrant purple color */
            // text-transform: lowercase;
          }
        `}
      </style>

      {/* SVG text element for the logo wordmark */}
      <text x="0" y="40" className="saveit-text">
        FavWheel
      </text>
    </svg>
  );
};

export default Logo;
