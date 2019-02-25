import React from 'react';

class Details extends React.Component {
    fetchIpInfo = event => {
        event.preventDefault();
        // const storeName = this.storeName.current.value;
        // this.props.history.push(`/store/${storeName}`);
        console.log('event')
        console.log(event)
        this.props.history.push(`/details/1`);
    }
    render() {
        console.log(this.props)
        return (
            <h2>Details</h2>
        )
    }
}

export default Details;




