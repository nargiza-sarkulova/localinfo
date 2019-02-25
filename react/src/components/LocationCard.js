import React from 'react';

const LocationCard = (props) => {
    return (
        <div className="ipRow">
            <p><b>IP:</b> <a href={ `/details/?ip=${props.number}` }>{props.number}</a> </p>
            <p><b>Country:</b> {props.country_name} <img src={props.country_flag} alt="" /> </p>
            <p><b>City:</b> {props.city}</p>
            <p><b>Region:</b> {props.region_name}</p>
            <p><b>Latitude:</b> {props.latitude}</p>
            <p><b>Longitude:</b> {props.longitude}</p>
        </div>
    )
}

export default LocationCard;