import React from 'react';

const LocationCard = (props) => {
    console.log('props')
    console.log(props)
  return (
    <div className="ipRow">
      <p><b>IP:</b> {props.number}</p>
      <p><b>Country:</b> {props.country_name} <img src={props.country_flag} alt="" /> </p>
      <p><b>City:</b> {props.city}</p>
      <p><b>Region:</b> {props.region_name}</p>
      <p><b>Latitude:</b> {props.latitude}</p>
      <p><b>Longitude:</b> {props.longitude}</p>
    </div>
  )
}

export default LocationCard;