import React, { useState,useEffect, useCallback } from "react";


import PropTypes from 'prop-types';
import Question from './Question';
import { CSSTransitionGroup } from 'react-transition-group';
import QuestionCount from './QuestionCount';
import AnswerOption from './AnswerOption';
import {makeStyles} from "@material-ui/core/styles";


import "./StyleQuiz.css";
import PHOTOS from './api/photos';
import QUIZPHOTOS from './api/quizPhotos';
import Masonry from "react-masonry-component";
import ImagePicker from 'react-image-picker'

import 'react-image-picker/dist/index.css'

import {Button, Grid} from "@material-ui/core";
import * as settings from "../../settings";
import axios from "axios";


// Masonry Options
const masonryOptions = {
  fitWidth: false,
  columnWidth: 300,
  gutter: 30,
  itemSelector: ".photo-item",
};

const area = document.getElementById("styles");

const imageList = ["https://storage.googleapis.com/linear-static-assets/414509.png",
    "https://storage.googleapis.com/linear-static-assets/414518.png",
    "https://storage.googleapis.com/linear-static-assets/414531.png"]

function Quiz(props) {
    // this if
    // const [images, setImages] = useState([])
    const [image, setImage] = useState([])
    const [img, setImg] = useState('')
    var tempList = [];
    // const [style, setStyle] = useState('')

    // function getStyles() {
    //     var tempList = [];
    //     images.forEach(item => tempList.push(...item.value))
    //     setStyle(tempList)
    // }
    const memoizedOnPick = useCallback(
        (image) => {
            setImage(image);
            // getStyles();
            tempList = [];
            // console.log(image)

            // This is for recording styles
            if (image && image.length>1) {
                // array and array.length are truthy
                // ⇒ probably OK to process array
                image.forEach(item => tempList.push(...item))
            }
            // area.value = tempList.toString()
            console.log(tempList);

            // setStyle(tempList)
            // console.log(style)
          // console.log(images.value)
          // setStyle(images.style);
          // console.log(style)
        },
        // [],
        [tempList], // Tells React to memoize regardless of arguments.
  );

    // // Import images regardless of file name
    // function importAll(r) {
    //
    //   return r.keys().map(r);
    // }
    // const images = importAll(require.context('./assets/', false, /\.(png|jpe?g|svg)$/));

    // {
    // images.map(
    //   (image, index) => <img key={index} src={image} alt="info"></img>
    // )
    // }
    // React hook state variable - Dimensions
    const [dimensions, setDimensions] = React.useState({
        sepal_length: 1,
        sepal_width: 1,
        petal_length: 1,
        petal_width: 1,
    });

    // React hook state variable - Prediction
    const [prediction, setPrediction] = React.useState(null)

    // Function to make the predict API call and update the state variable - Prediction
    const handlePredict = event => {
        // Submit Iris Flower measured dimensions as form data
        let irisFormData = new FormData();
        irisFormData.append("sepal length (cm)", dimensions.sepal_length);
        irisFormData.append("sepal width (cm)", dimensions.sepal_width);
        irisFormData.append("petal length (cm)", dimensions.petal_length);
        irisFormData.append("petal width (cm)", dimensions.petal_width);

        //Axios variables required to call the predict API
        // let headers = { 'Authorization': `Token ${props.token}` };
        let url = settings.API_SERVER + '/api/predict/';
        let method = 'post';
        let config = { method, url, data: image };

        //Axios predict API call
        axios(config).then(
            res => {setPrediction(res.data["Predicted Iris Species"])
            }).catch(
                error => {alert(error)})

    }

    function renderAnswerOptions(key) {
      return (
        <AnswerOption
          key={key.content}
          answerContent={key.content}
          answerType={key.type}
          answer={props.answer}
          questionId={props.questionId}
          onAnswerSelected={props.onAnswerSelected}
        />
      );
    }
    return (
    <CSSTransitionGroup
      className="container"
      component="div"
      transitionName="fade"
      transitionEnterTimeout={800}
      transitionLeaveTimeout={500}
      transitionAppear
      transitionAppearTimeout={500}
    >
      <div className="quiz">
          {/*<Masonry*/}
          {/*  className={"photo-list"}*/}
          {/*  elementType={"ul"}*/}
          {/*  options={masonryOptions}*/}
          {/*  disableImagesLoaded={false}*/}
          {/*  updateOnEachImageLoad={false}*/}
          {/*>*/}
          {/*  <div>*/}
          {/*      <ImagePicker*/}
          {/*        images={imageList.map((image, i) => ({src: image, value: i}))}*/}
          {/*        onPick={this.setImg.bind(this)}*/}
          {/*      />*/}
          {/*      <textarea rows="4" cols="100" value={this.state.image && JSON.stringify(this.state.image)} disabled/>*/}
          {/*  </div>*/}
            <div>
                <ImagePicker
                  // images={PHOTOS.map((photo) => ({src:photo.imageUrl, value: photo.style}
                  images={PHOTOS.slice(0,7).map((photo) => ({src:photo.imageUrl, value: "default"}
                    ))}
                  onPick={memoizedOnPick}
                  multiple
                />
                <textarea rows="4" cols="100" value={image && JSON.stringify(image)} disabled/>
                {/*<textarea rows="4" cols="100" value = {images.value && JSON.stringify(images.value)} disabled/>*/}
                {/*<textarea id="styles" rows="4" cols="100" disabled/>*/}
            </div>
            <div>
                <ImagePicker
                  // images={PHOTOS.map((photo) => ({src:photo.imageUrl, value: photo.style}
                  images={QUIZPHOTOS.slice(0,7).map((photo) => ({src:photo.imageUrl, value: "default"}
                    ))}
                  onPick={memoizedOnPick}
                  multiple
                />
                <textarea rows="4" cols="100" value={image && JSON.stringify(image)} disabled/>
                {/*<textarea rows="4" cols="100" value = {images.value && JSON.stringify(images.value)} disabled/>*/}
                {/*<textarea id="styles" rows="4" cols="100" disabled/>*/}
            </div>
            <div>
                <Button variant="contained" color="primary">
                    OK
                </Button>

            </div>
            <div>
                <div><h2>ML Prediction </h2></div>

                <Button variant="contained" color="primary" onClick={handlePredict}>
                    Predict
                </Button>

                <div><h2>{prediction}</h2></div>

            </div>
            {/*{PHOTOS.map((photo) => (*/}
            {/*  <li className={`photo-item`}>*/}
            {/*    <img src={photo.imageUrl} alt="" />*/}
            {/*  </li>*/}
            {/*))}*/}
          {/*</Masonry>*/}

          {/*C:\linear\frontend\react_app\src\components\Questions*/}
        {/*{images.map((photo) => (*/}
        {/*    <img src={photo.imageUrl} alt="" />*/}
        {/*))}*/}
        {/*<QuestionCount*/}
        {/*  counter={props.questionId}*/}
        {/*  total={props.questionTotal}*/}
        {/*/>*/}
        {/*<Question content={props.question} />*/}
        {/*<ul className="answerOptions">*/}
        {/*  {props.answerOptions.map(renderAnswerOptions)}*/}
        {/*</ul>*/}
      </div>
    </CSSTransitionGroup>
    );
}
//
// Quiz.propTypes = {
//     answer: PropTypes.string.isRequired,
//     answerOptions: PropTypes.array.isRequired,
//     counter: PropTypes.number.isRequired,
//     question: PropTypes.string.isRequired,
//     questionId: PropTypes.number.isRequired,
//     questionTotal: PropTypes.number.isRequired,
//     onAnswerSelected: PropTypes.func.isRequired
// };

export default Quiz;