import React from 'react';

const News = (props) => {
  return (
    <div className="newsRow">
      <p><b>Source:</b> {props.source.name}</p>
      <p><b>Title:</b> <a href={props.url}> {props.title}</a></p>
      <p><b>Description:</b> {props.description}</p>
      <p><b>content:</b> {props.content}</p>
      <p><img src={props.urlToImage} alt="" /></p>

    </div>
  )
}

export default News;