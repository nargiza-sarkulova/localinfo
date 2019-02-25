import React from 'react';

const Weather = (props) => {
  return (
    <div className="weatherRow">
      <p><b>Description:</b> {props.description}</p>
      <p><b>Temperature:</b> {props.temperature} </p>
      <p><b>Pressure:</b> {props.pressure}</p>
      <p><b>Humidity:</b> {props.humidity}</p>
      <p><b>Wind_speed:</b> {props.wind_speed}</p>
    </div>
  )
}

export default Weather;